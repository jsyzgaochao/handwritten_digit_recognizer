import tensorflow as tf

class TfPredict():
    def __init__(self):
        self.input = tf.placeholder(tf.float32, shape=[None, 784])
        self.output = tf.nn.softmax(self.model(self.input))
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.InteractiveSession(config=config)
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        self.saver.restore(self.sess, 'ckpt/mnist.ckpt')
        pass

    def model(self, x):
        x = tf.reshape(x, shape=[-1, 28, 28, 1])
        x = tf.layers.conv2d(x, filters=6, kernel_size=5, strides=1, padding='SAME', activation=tf.nn.relu)
        x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)
        x = tf.layers.conv2d(x, filters=16, kernel_size=5, strides=1, padding='VALID', activation=tf.nn.relu)
        x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)
        x = tf.layers.conv2d(x, filters=32, kernel_size=5, strides=1, padding='VALID', activation=tf.nn.relu)
        x = tf.reshape(x, shape=[-1, 32])
        x = tf.layers.dense(x, units=64, activation=tf.nn.relu)
        x = tf.layers.dense(x, units=10)
        return x

    def predict(self, x):
        result = self.sess.run(self.output, feed_dict={self.input: x})
        return result
