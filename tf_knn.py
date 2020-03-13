import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np


def knn_tensorflow():
    """ tensorflow conduct knn
    :return None
    """
    mnist = input_data.read_data_sets("./data/", one_hot=True)

    train_x, train_y = mnist.train.next_batch(60000)
    test_x, test_y = mnist.test.next_batch(10000)

    train_x_p = tf.placeholder(tf.float32, [None, 784])
    test_x_p = tf.placeholder(tf.float32, [784])


    # L2 dis：dist = sqrt(sum(|X1-X2|^2))
    dist_l2 = tf.sqrt(tf.reduce_sum(tf.square(tf.abs(train_x_p + tf.negative(test_x_p))), reduction_indices=1))

    prediction = tf.arg_min(dist_l2, 0)

    accuracy = 0.

    init_op = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init_op)
        for i in range(len(test_x)):
            nn_index = sess.run(prediction, feed_dict={train_x_p: train_x, test_x_p: test_x[i, :]})
            print("Test set : No. %d. True: %d. Predict：%d" % (i, np.argmax(test_y[i]), np.argmax(train_y[nn_index])))
            if np.argmax(test_y[i]) == np.argmax(train_y[nn_index]):
                accuracy += 1. / len(test_x)
        print("Acc：%f " % accuracy)

    return None

if __name__ == '__main__':
    knn_tensorflow()

