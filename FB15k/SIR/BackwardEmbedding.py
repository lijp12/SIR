import PureNeuralNetwork as PureNN
import tensorflow as tf
import numpy as np
import math
import argparse


__FLAGS = None


__learning_rate = 1e-3
__max_epoch = 5
__summaries_dir = 'bp_event_logs/'
__batch_size = 0
# __checkpoint_duration = 0

# need to be calculated
__max_steps = 0
__test_duration = 0


def backward_embedding(use_data_from_checkpoint=True):

    # parse parameters
    global __max_steps
    global __test_duration
    global __batch_size
    # global __checkpoint_duration

    sess = tf.InteractiveSession()

    PureNN.load_input_data()  # load train and test data. This step should be before the assignment of __max_steps

    __batch_size = PureNN.train_data_1.shape[0]

    PureNN.set_batch_size(__batch_size)

    steps_per_epoch = int(math.ceil(PureNN.train_data.shape[0] / __batch_size))  # need train data loaded

    print('steps_per_epoch: %s' % steps_per_epoch)

    __max_steps = __max_epoch * steps_per_epoch
    __test_duration = steps_per_epoch
    # __checkpoint_duration = __max_steps // 5

    print('max_steps %s\n test duration %s' % (__max_steps, __test_duration))

    # set False as set_up_model's parameter, to represent backward embedding
    x, y_, y, embedding = PureNN.set_up_model(False)  # care about embedding in this stage

    # loss function
    with tf.name_scope('cross_entropy'):
        # The raw formulation of cross-entropy,
        #
        # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
        #                               reduction_indices=[1]))
        #
        # can be numerically unstable.
        #
        # So here we use tf.nn.softmax_cross_entropy_with_logits on the
        # raw outputs of the nn_layer above, and then average across
        # the batch.
        diff = tf.nn.softmax_cross_entropy_with_logits(y, y_)
        with tf.name_scope('total'):
            cross_entropy = tf.reduce_mean(diff)
        tf.scalar_summary('cross entropy', cross_entropy)

    # initialize
    # restore variables
    saver = tf.train.Saver()
    if not use_data_from_checkpoint:
        sess.run(tf.initialize_all_variables())
    else:
        latest_ckpt = tf.train.get_checkpoint_state(PureNN.checkpoint_dir)
        if latest_ckpt and latest_ckpt.model_checkpoint_path:
            saver.restore(sess, latest_ckpt.model_checkpoint_path)
            print('Variables restored from the latest checkpoint: %s' % latest_ckpt.model_checkpoint_path)
        else:
            print('fail to restore variables from the latest checkpoint')
            return

    original_var_list = tf.all_variables()

    # train
    with tf.name_scope('train'):
        train_step = tf.train.AdamOptimizer(__learning_rate).minimize(cross_entropy)
        # train_step = tf.train.GradientDescentOptimizer(__learning_rate).minimize(cross_entropy)

    augmented_var_list = tf.all_variables()

    vars_added = list(set(augmented_var_list).difference(set(original_var_list)))

    tf.initialize_variables(vars_added).run()

    # collect statistical information
    # This part only calculates the accuracy on a mini batch of train data or the total test data
    with tf.name_scope('accuracy'):
        with tf.name_scope('correct_prediction'):
            # argmax: Returns the index with the largest value across dimensions of a tensor.
            correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        with tf.name_scope('accuracy'):
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.scalar_summary('accuracy', accuracy)

    # Merge all the summaries and write them out to summaries_log dir
    merged = tf.merge_all_summaries()
    train_writer = tf.train.SummaryWriter(__summaries_dir + 'train', sess.graph)
    test_writer_0 = tf.train.SummaryWriter(__summaries_dir + 'test_0')
    test_writer_1 = tf.train.SummaryWriter(__summaries_dir + 'test_1')
    train_writer_0 = tf.train.SummaryWriter(__summaries_dir + 'train0')
    train_writer_1 = tf.train.SummaryWriter(__summaries_dir + 'train1')

    # list1 = tf.all_variables()
    # list2 = tf.trainable_variables()
    # list1 = list(set(list1).difference(set(list2)))
    #
    # print('\n\ntrainable variables:\n')
    #
    # for var in list2:
    #     print(var.name)
    #
    # print('\n\nuntrainable variables:\n')
    # for var in list1:
    #     print(var.name)
    #
    # print('\n\n')

    fake_max_steps = __max_steps + 1
    iteration_base = __FLAGS.current_run * fake_max_steps

    summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.feed_dict(False, x, y_))
    test_writer_1.add_summary(summary, iteration_base)
    print('\nAccuracy on positive test data before training, step %s: %s' % (iteration_base, acc))

    summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.feed_dict(None, x, y_))
    test_writer_0.add_summary(summary, iteration_base)
    print('Accuracy on negative test data before training, step %s: %s' % (iteration_base, acc))

    summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.whole_train_as_feed(True, x, y_))
    train_writer_1.add_summary(summary, iteration_base)
    print('\nAccuracy on positive train data at step %s: %s' % (iteration_base, acc))

    summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.whole_train_as_feed(False, x, y_))
    train_writer_0.add_summary(summary, iteration_base)
    print('Accuracy on negative train data at step %s: %s' % (iteration_base, acc))

    for i in range(1, fake_max_steps):

        # Record train set summaries, and train
        summary, _ = sess.run(
            [merged, train_step],
            feed_dict=PureNN.feed_dict(True, x, y_)
        )

        train_writer.add_summary(summary, i + iteration_base)

        # if i % __checkpoint_duration == 0 or i == __max_steps:
        #     # save all Variables
        #     save_path = saver.save(
        #         sess,
        #         PureNN.checkpoint_dir + 'variables.ckpt',
        #         global_step=i + __FLAGS.current_run * (__max_steps + 1)
        #     )
        #     print('\nVariables saved in %s at step %s' % (save_path, i + __FLAGS.current_run * __max_steps))

        if i % __test_duration == 0 or i == __max_steps:  # Record summaries and test-set accuracy

            summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.feed_dict(False, x, y_))
            test_writer_1.add_summary(summary, i + iteration_base)
            print('\nAccuracy on positive test data at step %s: %s' % (i + iteration_base, acc))

            summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.feed_dict(None, x, y_))
            test_writer_0.add_summary(summary, i + iteration_base)
            print('Accuracy on negative test data at step %s: %s' % (i + iteration_base, acc))

            summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.whole_train_as_feed(True, x, y_))
            train_writer_1.add_summary(summary, i + iteration_base)
            print('\nAccuracy on positive train data at step %s: %s' % (i + iteration_base, acc))

            summary, acc = sess.run([merged, accuracy], feed_dict=PureNN.whole_train_as_feed(False, x, y_))
            train_writer_0.add_summary(summary, i + iteration_base)
            print('Accuracy on negative train data at step %s: %s' % (i + iteration_base, acc))

    # save embedding
    embed_val = sess.run(embedding)
    np.savetxt(PureNN.input_data_dir + 'embedding.txt', embed_val)
    print('bp embedding saved!')

    train_writer.close()
    test_writer_0.close()
    test_writer_1.close()
    train_writer_0.close()
    train_writer_1.close()


def main(_):

    if __FLAGS.current_run == __FLAGS.total_run - 1:
        print('It\'s final run, we won\'t do bp embedding!')
    else:
        if tf.gfile.Exists(__summaries_dir) and __FLAGS.delete_event == 1:
            tf.gfile.DeleteRecursively(__summaries_dir)  # should be deleted on the startup
        if not tf.gfile.Exists(__summaries_dir):
            tf.gfile.MakeDirs(__summaries_dir)
        if not tf.gfile.Exists(PureNN.checkpoint_dir):
            tf.gfile.MakeDirs(PureNN.checkpoint_dir)

        global __max_epoch
        __max_epoch = __FLAGS.max_epoch
        print('max epoch %s' % __max_epoch)
        backward_embedding(True)  # args: use_data_from_checkpoint

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'current_run',
        type=int,
        help='specify which run is going on'
    )

    parser.add_argument(
        'total_run',
        type=int,
        help='specify total run'
    )

    parser.add_argument(
        'delete_event',
        type=int,
        help='specify whether to delete event logs'
    )

    parser.add_argument(
        'max_epoch',
        type=int,
        help='specify maximum epoch to go through train data'
    )

    __FLAGS = parser.parse_args()

    tf.app.run()
