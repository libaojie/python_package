import tensorflow as tf


class TFDemo7(object):
    """
    placeholder 是 Tensorflow 中的占位符，暂时储存变量.
    Tensorflow 如果想要从外部传入data, 那就需要用到 tf.placeholder(), 然后以这种形式传输数据 sess.run(***, feed_dict={input: **}).
    """

    def main(self):
        input1 = tf.placeholder(dtype=tf.float32)
        input2 = tf.placeholder(dtype=tf.float32)

        output = tf.multiply(input1, input2)

        with tf.Session() as sess:
            print(sess.run(output, feed_dict={input1: [3.], input2: [5]}))
        pass


tfDemo = TFDemo7()
tfDemo.main()
