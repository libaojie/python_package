import os

import tensorflow as tf

# 用于忽略级别 2 及以下的消息（级别 1 是提示，级别 2 是警告，级别 3 是错误）
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class TFDemo2(object):

    def main(self):
        message = tf.constant("welcome !!!")
        with tf.Session() as sess:
            print(sess.run(message).decode())
