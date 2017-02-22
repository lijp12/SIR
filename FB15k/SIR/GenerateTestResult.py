import PureNeuralNetwork as PureNN
import tensorflow as tf
import numpy as np
import time
import argparse

__already_recovered = False
__inference_op = None
__x = None
__sess = None


def recover_model():

    # set None as set_up_model's parameter, to represent inference
    x, _, y, _ = PureNN.set_up_model(None)  # do not care about embedding and y_ in this stage
    # loss function

    inference_op = tf.nn.softmax(y)

    # limit GPU memory allocation
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = False
    sess = tf.InteractiveSession(config=config)

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


def main(_):

    if tf.gfile.Exists(PureNN.output_data_dir):
        tf.gfile.DeleteRecursively(PureNN.output_data_dir)  # should be deleted on the startup
    tf.gfile.MakeDirs(PureNN.output_data_dir)

    entity_num = PureNN.default_embedding.shape[0]
    total = entity_num * (entity_num - 1)
    connected = 0
    start_time = time.time()

    PureNN.load_input_data()
    recover_model()

    assert __already_recovered is True
    assert __inference_op is not None
    assert __sess is not None
    assert __x is not None

    print(PureNN.test_data_0)
    print(PureNN.test_data_1)

    inference_val = __sess.run(__inference_op, feed_dict={__x: PureNN.test_data_0[:, 0:2]})
    np.savetxt(PureNN.output_data_dir + "prediction_for_label0.txt", inference_val, fmt='%.15f')

    inference_val = __sess.run(__inference_op, feed_dict={__x: PureNN.test_data_1[:, 0:2]})
    np.savetxt(PureNN.output_data_dir + "prediction_for_label1.txt", inference_val, fmt='%.15f')


if __name__ == '__main__':

    tf.app.run()

