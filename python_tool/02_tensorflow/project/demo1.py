import tensorflow as tf
from lbj_common.log_tool import LogTool


class TFDemo(object):

    def main(self):
        # self.add()
        self.add_view()

    def add(self):
        a = tf.constant([1.0, 2.0], name='a')
        b = tf.constant([2.0, 3.0], name='b')
        c = tf.constant([3.0, 4.0], name='c')
        result = a + b + c
        LogTool.print(result)

        with tf.Session() as sess:
            LogTool.print(sess.run(result))

    def add_view(self):
        a = tf.constant([1.0, 2.0], name='a')
        b = tf.constant([2.0, 3.0], name='b')
        v_add = tf.add(a, b)
        with tf.Session() as sess:
            print(sess.run(v_add))
