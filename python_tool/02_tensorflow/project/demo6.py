import tensorflow as tf


class TFDemo6(object):
    """
    在 Tensorflow 中，定义了某字符串是变量，它才是变量，这一点是与 Python 所不同的。定义语法： state = tf.Variable().
    如果你在 Tensorflow 中设定了变量，那么初始化变量是最重要的！！
    所以定义了变量以后, 一定要定义 init = tf.global_variables_initializer().到这里变量还是没有被激活，
    需要再在 sess 里, sess.run(init) , 激活 init 这一步.
    """

    def main(self):
        # 定义变量，给定初始值和name
        state = tf.Variable(0, name="counter")
        # counter:0
        print(state.name)

        one = tf.constant(1)

        new_value = tf.add(state, one)
        update = tf.assign(state, new_value)

        # 这里只是定义，必须用session.run来执行
        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            for _ in range(3):
                sess.run(update)
                print(sess.run(state))
        pass


tfDemo = TFDemo6()
tfDemo.main()
