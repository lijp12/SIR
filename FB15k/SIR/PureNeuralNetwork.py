# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================



from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import numpy as np


# things about data and directories
input_data_dir = 'result/'
output_data_dir = 'output_data/'
checkpoint_dir = 'checkpoint_log/'
train_data = None
test_data_0 = None
test_data_1 = None
train_data_0 = None
train_data_1 = None

# parameters initialized
__batch_index = 0
__epoch_completed = 0
__batch_size = 0


default_embedding = np.loadtxt(input_data_dir + 'embedding.txt', dtype=np.float64)


# things about architecture
__embedding_dim = 100  # dimension of embedding
__architecture = (__embedding_dim * 2, 400, 2)  # units of input layer, hidden layers, output layer, orderly


def set_batch_size(val):
    global __batch_size
    __batch_size = val


def load_input_data():
    global train_data, test_data_0, test_data_1, train_data_0, train_data_1

    train_data_0 = np.loadtxt(input_data_dir + 'train_data_0.txt', dtype=np.int32)
    train_data_1 = np.loadtxt(input_data_dir + 'train_data_1.txt', dtype=np.int32)

    train_data = np.row_stack((train_data_0, train_data_1))

    test_data_0 = np.loadtxt(input_data_dir + 'test_data_0.txt', dtype=np.int32)
    test_data_1 = np.loadtxt(input_data_dir + 'test_data_1.txt', dtype=np.int32)

    test_data_0 = test_data_0[:, 0:2]
    test_data_1 = test_data_1[:, 0:2]

    # fill zeros and ones in
    test_data_0 = np.column_stack((test_data_0, np.zeros(shape=(test_data_0.shape[0], 1), dtype=np.int32)))
    test_data_1 = np.column_stack((test_data_1, np.ones(shape=(test_data_1.shape[0], 1), dtype=np.int32)))

    perm = np.arange(train_data.shape[0])
    np.random.shuffle(perm)
    train_data = train_data[perm]
    print('start epoch 0, with train data shuffled!')


def whole_train_as_feed(is_positive, placeholder_x, placeholder_y_):

    if is_positive is True:
        train_batch_label = np.column_stack(
            (1 - train_data_1[:, 2: 3], train_data_1[:, 2: 3])
        )
        x = train_data_1[:, 0: 2]
    elif is_positive is False:
        train_batch_label = np.column_stack(
            (1 - train_data_0[:, 2: 3], train_data_0[:, 2: 3])
        )
        x = train_data_0[:, 0: 2]
    else:
        print('wrong parameter is_positive!')
        exit()

    return {
        placeholder_x: x,
        placeholder_y_: train_batch_label
    }


def feed_dict(is_train, placeholder_x, placeholder_y_):

    def next_batch():

        global __batch_index, train_data

        start = __batch_index
        __batch_index += __batch_size

        if __batch_index > train_data.shape[0]:

            diff = train_data.shape[0] - start
            assert 0 <= diff < __batch_size

            if diff == 0:  # reaches end of the data set
                global __epoch_completed
                __epoch_completed += 1
                perm = np.arange(train_data.shape[0])
                np.random.shuffle(perm)
                train_data = train_data[perm]

                # start next epoch
                start = 0
                __batch_index = __batch_size
                print('start epoch %d, with train data shuffled!\n' % __epoch_completed)
            else:
                __batch_index = train_data.shape[0]

        end = __batch_index

        train_batch_input = train_data[start: end, 0: 2]

        train_batch_label = np.column_stack(
            (1 - train_data[start: end, 2: 3], train_data[start: end, 2: 3])
        )

        assert train_batch_input[0][0] == train_data[start][0]
        assert train_batch_input[end - start - 1][1] == train_data[end - 1][1]
        return train_batch_input, train_batch_label

    """
    is_train == True  -->  train_data
    is_train == False  -->  test_data_1
    is_train == None  -->  test_data_0
    """
    if is_train is True:

        _train_batch_input, _train_batch_label = next_batch()

        return {
            placeholder_x: _train_batch_input,
            placeholder_y_: _train_batch_label
        }

    elif is_train is False:
        return {
            placeholder_x: test_data_1[:, 0: 2],
            placeholder_y_: np.column_stack((1 - test_data_1[:, 2: 3], test_data_1[:, 2: 3]))
        }
    else:
        return {
            placeholder_x: test_data_0[:, 0: 2],
            placeholder_y_: np.column_stack((1 - test_data_0[:, 2: 3], test_data_0[:, 2: 3]))
        }

# Create a multilayer model.
# We can't initialize these variables to 0 - the network will get stuck.


def __weight_variable(shape, trainable=True):
    """Create a weight variable with appropriate initialization."""
    initial = tf.truncated_normal(shape, stddev=1, dtype=tf.float64)
    return tf.Variable(initial, trainable=trainable)


def __bias_variable(shape, trainable=True):
    """Create a bias variable with appropriate initialization."""
    initial = tf.constant(0.1, shape=shape, dtype=tf.float64)
    return tf.Variable(initial, trainable=trainable)


def __variable_summaries(var, name):
    """Attach a lot of summaries to a Tensor."""
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.scalar_summary('mean/' + name, mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.scalar_summary('stddev/' + name, stddev)
        tf.scalar_summary('max/' + name, tf.reduce_max(var))
        tf.scalar_summary('min/' + name, tf.reduce_min(var))
        tf.histogram_summary(name, var)


def __nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu, trainable=True):
    """Reusable code for making a simple neural net layer.

    It does a matrix multiply, bias add, and then uses relu to nonlinearize.
    It also sets up name scoping so that the resultant graph is easy to read,
    and adds a number of summary ops.
    """
    # Adding a name scope ensures logical grouping of the layers in the graph.
    with tf.name_scope(layer_name):
        # This Variable will hold the state of the weights for the layer
        with tf.name_scope('weights'):
            weights = __weight_variable([input_dim, output_dim], trainable)
            __variable_summaries(weights, layer_name + '/weights')
        with tf.name_scope('biases'):
            biases = __bias_variable([output_dim], trainable)
            __variable_summaries(biases, layer_name + '/biases')
        with tf.name_scope('Wx_plus_b'):
            preactivate = tf.matmul(input_tensor, weights) + biases
            tf.histogram_summary(layer_name + '/pre_activations', preactivate)
        activations = act(preactivate, name='activation')
        tf.histogram_summary(layer_name + '/activations', activations)
    return activations


def set_up_model(three_valued_condition):

    if three_valued_condition is None:  # for inference
        embedding_trainable = False
        weights_trainable = False
        print('used for inference')
    elif three_valued_condition is True:  # for forward training
        embedding_trainable = False
        weights_trainable = True
        print('used for forward training of network weights and biases')
    else:  # for backward embedding
        embedding_trainable = True
        weights_trainable = False
        print('used for backward propagation of embedding')

    # input
    with tf.name_scope('input'):
        x = tf.placeholder(
            tf.int32,
            (None, 2),  # for two entity indices
            'x_input_entity_indices'
        )
        y_ = tf.placeholder(
            tf.float64,
            (None, __architecture[len(__architecture) - 1]),
            'y_input'
        )

    # embedding matrix
    embedding = tf.Variable(
        initial_value=tf.convert_to_tensor(default_embedding, tf.float64),
        trainable=embedding_trainable,
        name='embedding_matrix'
    )

    tf.histogram_summary('embedding', embedding)

    # lookup embedding matrix to form the input matrix for Neural Network
    input_matrix = tf.nn.embedding_lookup(embedding, x)
    # this tensor has shape(batch_size/test_data_size, 2, embedding_dim)
    # reshape
    reshaped_input_matrix = tf.reshape(input_matrix, shape=[tf.shape(input_matrix)[0], __architecture[0]])

    # hidden layer 1
    hidden1 = __nn_layer(
        reshaped_input_matrix,
        __architecture[0],
        __architecture[1],
        'hidden_layer1',
        trainable=weights_trainable
    )

    # output layer.
    y = __nn_layer(
        hidden1,
        __architecture[1],
        __architecture[len(__architecture) - 1],
        'output_layer',
        act=tf.identity,  # so that the caller can customize the usage of this output
        trainable=weights_trainable
    )

    return x, y_, y, embedding
