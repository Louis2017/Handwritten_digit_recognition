# coding:utf-8
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

def new_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def new_biases(length):
    return tf.Variable(tf.constant(0.1, shape=length))


mnist = input_data.read_data_sets("data/", one_hot=True)


x = tf.placeholder(tf.float32, [None, 784])
Wb = {"weights": new_weights([784, 10]),
             "biases": new_weights([10])}

y = tf.nn.softmax(tf.matmul(x, Wb["weights"]) + Wb["biases"])

y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y)))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
print('start training...')

for _ in range(10000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))  # 0.9185
savew_W = Wb["weights"].eval()
saveb_b = Wb["biases"].eval()
np.save("./paras/softmax_W.npy", savew_W)
np.save("./paras/softmax_b.npy", saveb_b)
