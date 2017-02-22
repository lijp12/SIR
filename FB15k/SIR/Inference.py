import PureNeuralNetwork as PureNN
import tensorflow as tf
import numpy as np
import time
import argparse

__already_recovered = False
__inference_op = None
__x = None
__sess = None

__FLAGS = None


def recover_model():

    # set None as set_up_model's parameter, to represent inference
    x, _, y, _ = PureNN.set_up_model(None)  # do not care about embedding and y_ in this stage
    # loss function

    inference_op = tf.nn.softmax(y)

    sess = tf.InteractiveSession()

    # restore variables
    saver = tf.train.Saver()

    latest_ckpt = tf.train.get_checkpoint_state(PureNN.checkpoint_dir)
    if latest_ckpt and latest_ckpt.model_checkpoint_path:
        saver.restore(sess, latest_ckpt.model_checkpoint_path)
        print('Variables restored from the latest checkpoint: %s' % latest_ckpt.model_checkpoint_path)
    else:
        print('fail to restore variables from the latest checkpoint')
        return

    list1 = tf.all_variables()
    list2 = tf.trainable_variables()
    list1 = list(set(list1).difference(set(list2)))

    print('\n\ntrainable variables:')

    for var in list2:
        print(var.name)

    print('\n\nuntrainable variables:')
    for var in list1:
        print(var.name)

    print('\n\n')

    global __already_recovered, __inference_op, __x, __sess
    __already_recovered = True
    __inference_op = inference_op
    __x = x
    __sess = sess


def is_connected(ent1, ent2, threshold=0.5):
    input_pair = np.ndarray(shape=(1, 2), dtype=np.int32, buffer=np.array([ent1, ent2], dtype=np.int32))

    assert __already_recovered is True
    assert __inference_op is not None
    assert __sess is not None
    assert __x is not None

    inference_val = __sess.run(__inference_op, feed_dict={__x: input_pair})

    # print(input_pair, inference_val)

    return inference_val[0, 1] > threshold


def main(_):

    if tf.gfile.Exists(PureNN.output_data_dir):
        tf.gfile.DeleteRecursively(PureNN.output_data_dir)  # should be deleted on the startup
    tf.gfile.MakeDirs(PureNN.output_data_dir)

    entity_num = PureNN.default_embedding.shape[0]
    total = entity_num * (entity_num - 1)
    connected = 0
    start_time = time.time()

    recover_model()

    step = __FLAGS.interval

    assert __already_recovered is True
    assert __inference_op is not None
    assert __sess is not None
    assert __x is not None

    connected_prediction = tf.reduce_sum(tf.argmax(__inference_op, 1), reduction_indices=0)

    for i in range(0, entity_num, step):

        if i % step == 0:
            if i + step > entity_num:
                end = entity_num
            else:
                end = i + step

            term = entity_num - 1
            s = time.time()
            input_data = np.ndarray(shape=((end - i) * term, 2), dtype=np.int32)

            for t in range(i, end):
                input_data[(t - i) * term: (t - i + 1) * term, 0] = t
                vals = range(entity_num)
                vals.pop(t)
                input_data[(t - i) * term: (t - i + 1) * term, 1] = vals

            # np.savetxt("data%d.txt" % i, input_data, fmt='%d')

            connected_val, inference_val = __sess.run([connected_prediction, __inference_op], feed_dict={__x: input_data})
            inference_val = __sess.run(__inference_op, feed_dict={__x: input_data})

            np.savetxt(PureNN.output_data_dir + "prediction_%d.txt" % i, inference_val, fmt='%.15f')
            # np.savetxt(PureNN.output_data_dir + "pairs_%d.txt" % i, input_data, fmt='%d')
            del input_data
            connected += connected_val
            e = time.time()

            print('start entity index: %s, current connected: %s, time usage: %d' % (i, connected, e - s))

    end_time = time.time()
    interval = (end_time - start_time) / 3600
    print('\n\n\n\ntime usage: %s hours' % interval)
    print('total: %s, connected: %s' % (total, connected))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'interval',
        type=int,
        help='number of different head entities'
    )

    __FLAGS = parser.parse_args()
    tf.app.run()

