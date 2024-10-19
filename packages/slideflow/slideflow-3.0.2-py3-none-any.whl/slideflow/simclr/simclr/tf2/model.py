# coding=utf-8
# Copyright 2020 The SimCLR Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific simclr governing permissions and
# limitations under the License.
# ==============================================================================
"""Model specification for SimCLR."""

import math

import tensorflow.compat.v2 as tf
from . import data_util
from . import lars_optimizer
from . import resnet


def build_optimizer(learning_rate, optimizer, momentum, weight_decay):
  """Returns the optimizer."""
  if optimizer == 'momentum':
    return tf.keras.optimizers.SGD(learning_rate, momentum, nesterov=True)
  elif optimizer == 'adam':
    return tf.keras.optimizers.Adam(learning_rate)
  elif optimizer == 'lars':
    return lars_optimizer.LARSOptimizer(
        learning_rate,
        momentum=momentum,
        weight_decay=weight_decay,
        exclude_from_weight_decay=[
            'batch_normalization', 'bias', 'head_supervised'
        ])
  else:
    raise ValueError('Unknown optimizer {}'.format(optimizer))


def add_weight_decay(model, optimizer, weight_decay, adjust_per_optimizer=True):
  """Compute weight decay."""
  if adjust_per_optimizer and 'lars' in optimizer:
    # Weight decay are taking care of by optimizer for these cases.
    # Except for supervised head, which will be added here.
    l2_losses = [
        tf.nn.l2_loss(v)
        for v in model.trainable_variables
        if 'head_supervised' in v.name and 'bias' not in v.name
    ]
    if l2_losses:
      return weight_decay * tf.add_n(l2_losses)
    else:
      return 0

  # TODO(srbs): Think of a way to avoid name-based filtering here.
  l2_losses = [
      tf.nn.l2_loss(v)
      for v in model.trainable_weights
      if 'batch_normalization' not in v.name
  ]
  loss = weight_decay * tf.add_n(l2_losses)
  return loss


def get_train_steps(num_examples, train_steps, train_epochs, train_batch_size):
  """Determine the number of training steps."""
  return train_steps or (
      num_examples * train_epochs // train_batch_size + 1)


class WarmUpAndCosineDecay(tf.keras.optimizers.schedules.LearningRateSchedule):
  """Applies a warmup schedule on a given learning rate decay schedule."""

  def __init__(
    self,
    learning_rate,
    num_examples,
    *,
    warmup_epochs=10,
    train_batch_size=512,
    learning_rate_scaling='linear',
    train_steps=0,
    train_epochs=100,
    name=None
  ):
    super(WarmUpAndCosineDecay, self).__init__()
    self.base_learning_rate = learning_rate
    self.num_examples = num_examples
    self._name = name
    self.warmup_epochs = warmup_epochs
    self.train_batch_size = train_batch_size
    self.learning_rate_scaling = learning_rate_scaling
    self.train_steps = train_steps
    self.train_epochs = train_epochs

  def __call__(self, step):
    with tf.name_scope(self._name or 'WarmUpAndCosineDecay'):
      warmup_steps = int(
          round(self.warmup_epochs * self.num_examples //
                self.train_batch_size))
      if self.learning_rate_scaling == 'linear':
        scaled_lr = self.base_learning_rate * self.train_batch_size / 256.
      elif self.learning_rate_scaling == 'sqrt':
        scaled_lr = self.base_learning_rate * math.sqrt(self.train_batch_size)
      else:
        raise ValueError('Unknown learning rate scaling {}'.format(
            self.learning_rate_scaling))
      learning_rate = (
          step / float(warmup_steps) * scaled_lr if warmup_steps else scaled_lr)

      # Cosine decay learning rate schedule
      total_steps = get_train_steps(self.num_examples, self.train_steps,
        self.train_epochs, self.train_batch_size)
      # TODO(srbs): Cache this object.
      cosine_decay = tf.keras.experimental.CosineDecay(
          scaled_lr, total_steps - warmup_steps)
      learning_rate = tf.where(step < warmup_steps, learning_rate,
                               cosine_decay(step - warmup_steps))

      return learning_rate

  def get_config(self):
    return {
        'base_learning_rate': self.base_learning_rate,
        'num_examples': self.num_examples,
    }


class LinearLayer(tf.keras.layers.Layer):

  def __init__(
    self,
    num_classes,
    use_bias=True,
    use_bn=False,
    name='linear_layer',
    **kwargs
  ):
    # Note: use_bias is ignored for the dense layer when use_bn=True.
    # However, it is still used for batch norm.
    super(LinearLayer, self).__init__(**kwargs)
    self.num_classes = num_classes
    self.use_bias = use_bias
    self.use_bn = use_bn
    self._name = name
    if self.use_bn:
      self.bn_relu = resnet.BatchNormRelu(relu=False, center=use_bias)

  def build(self, input_shape):
    # TODO(srbs): Add a new SquareDense layer.
    if callable(self.num_classes):
      num_classes = self.num_classes(input_shape)
    else:
      num_classes = self.num_classes
    self.dense = tf.keras.layers.Dense(
        num_classes,
        kernel_initializer=tf.keras.initializers.RandomNormal(stddev=0.01),
        use_bias=self.use_bias and not self.use_bn)
    super(LinearLayer, self).build(input_shape)

  def call(self, inputs, training):
    assert inputs.shape.ndims == 2, inputs.shape
    inputs = self.dense(inputs)
    if self.use_bn:
      inputs = self.bn_relu(inputs, training=training)
    return inputs


class ProjectionHead(tf.keras.layers.Layer):

  def __init__(
    self,
    proj_out_dim,
    proj_head_mode='nonlinear',
    num_proj_layers=3,
    ft_proj_selector=0,
    **kwargs
  ):
    self.linear_layers = []
    if proj_head_mode == 'none':
      pass  # directly use the output hiddens as hiddens
    elif proj_head_mode == 'linear':
      self.linear_layers = [
          LinearLayer(
              num_classes=proj_out_dim, use_bias=False, use_bn=True, name='l_0')
      ]
    elif proj_head_mode == 'nonlinear':
      for j in range(num_proj_layers):
        if j != num_proj_layers - 1:
          # for the middle layers, use bias and relu for the output.
          self.linear_layers.append(
              LinearLayer(
                  num_classes=lambda input_shape: int(input_shape[-1]),
                  use_bias=True,
                  use_bn=True,
                  name='nl_%d' % j))
        else:
          # for the final layer, neither bias nor relu is used.
          self.linear_layers.append(
              LinearLayer(
                  num_classes=proj_out_dim,
                  use_bias=False,
                  use_bn=True,
                  name='nl_%d' % j))
    else:
      raise ValueError('Unknown head projection mode {}'.format(
          proj_head_mode))
    super(ProjectionHead, self).__init__(**kwargs)

    self.proj_head_mode = proj_head_mode
    self.num_proj_layers = num_proj_layers
    self.ft_proj_selector = ft_proj_selector

  def call(self, inputs, training):
    if self.proj_head_mode == 'none':
      return inputs  # directly use the output hiddens as hiddens
    hiddens_list = [tf.identity(inputs, 'proj_head_input')]
    if self.proj_head_mode == 'linear':
      assert len(self.linear_layers) == 1, len(self.linear_layers)
      return hiddens_list.append(self.linear_layers[0](hiddens_list[-1],
                                                       training))
    elif self.proj_head_mode == 'nonlinear':
      for j in range(self.num_proj_layers):
        hiddens = self.linear_layers[j](hiddens_list[-1], training)
        if j != self.num_proj_layers - 1:
          # for the middle layers, use bias and relu for the output.
          hiddens = tf.nn.relu(hiddens)
        hiddens_list.append(hiddens)
    else:
      raise ValueError('Unknown head projection mode {}'.format(
          self.proj_head_mode))
    # The first element is the output of the projection head.
    # The second element is the input of the finetune head.
    proj_head_output = tf.identity(hiddens_list[-1], 'proj_head_output')
    return proj_head_output, hiddens_list[self.ft_proj_selector]


class SupervisedHead(tf.keras.layers.Layer):

  def __init__(self, num_classes, name='head_supervised', **kwargs):
    super(SupervisedHead, self).__init__(name=name, **kwargs)
    self.linear_layer = LinearLayer(num_classes)

  def call(self, inputs, training):
    inputs = self.linear_layer(inputs, training)
    inputs = tf.identity(inputs, name='logits_sup')
    return inputs


class SimCLR(tf.keras.models.Model):
  """Resnet model with projection or supervised layer."""

  def __init__(
    self,
    num_classes,
    resnet_depth=50,
    width_multiplier=1,
    sk_ratio=0.,
    se_ratio=0.,
    image_size=224,
    batch_norm_decay=0.9,
    train_mode='pretrain',
    lineareval_while_pretraining=True,
    fine_tune_after_block=-1,
    use_blur=True,
    proj_out_dim=128,
    proj_head_mode='nonlinear',
    num_proj_layers=3,
    ft_proj_selector=0,
    **kwargs
):
    super(SimCLR, self).__init__(**kwargs)
    self.resnet_model = resnet.resnet(
        train_mode=train_mode,
        width_multiplier=width_multiplier,
        resnet_depth=resnet_depth,
        cifar_stem=image_size <= 32,
        sk_ratio=sk_ratio,
        se_ratio=se_ratio,
        batch_norm_decay=batch_norm_decay,
        fine_tune_after_block=fine_tune_after_block
    )
    self._projection_head = ProjectionHead(
      proj_out_dim,
      proj_head_mode=proj_head_mode,
      num_proj_layers=num_proj_layers,
      ft_proj_selector=ft_proj_selector
    )
    if ((train_mode == 'finetune' or lineareval_while_pretraining) and num_classes):
      self.supervised_head = SupervisedHead(num_classes)
    self.train_mode = train_mode
    self.fine_tune_after_block = fine_tune_after_block
    self.use_blur = use_blur
    self.image_size = image_size
    self.lineareval_while_pretraining = lineareval_while_pretraining
    self.num_classes = num_classes

  def __call__(self, inputs, training):
    features = inputs
    if training and self.train_mode == 'pretrain':
      if self.fine_tune_after_block > -1:
        raise ValueError('Does not support layer freezing during pretraining,'
                         'should set fine_tune_after_block<=-1 for safety.')
    if inputs.shape[3] is None:
      raise ValueError('The input channels dimension must be statically known '
                       f'(got input shape {inputs.shape})')
    num_transforms = inputs.shape[3] // 3
    num_transforms = tf.repeat(3, num_transforms)
    # Split channels, and optionally apply extra batched augmentation.
    features_list = tf.split(
        features, num_or_size_splits=num_transforms, axis=-1)
    if self.use_blur and training and self.train_mode == 'pretrain':
      features_list = data_util.batch_random_blur(features_list,
                                                  self.image_size,
                                                  self.image_size)
    features = tf.concat(features_list, 0)  # (num_transforms * bsz, h, w, c)

    # Base network forward pass.
    hiddens = self.resnet_model(features, training=training)

    # Add heads.
    projection_head_outputs, supervised_head_inputs = self._projection_head(
        hiddens, training)

    if self.train_mode == 'finetune':
      supervised_head_outputs = self.supervised_head(supervised_head_inputs,
                                                     training)
      return None, supervised_head_outputs
    elif (self.train_mode == 'pretrain'
          and self.lineareval_while_pretraining
          and self.num_classes):
      # When performing pretraining and linear evaluation together we do not
      # want information from linear eval flowing back into pretraining network
      # so we put a stop_gradient.
      supervised_head_outputs = self.supervised_head(
          tf.stop_gradient(supervised_head_inputs), training)
      return projection_head_outputs, supervised_head_outputs
    else:
      return projection_head_outputs, None
