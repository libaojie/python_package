import tensorflow as tf


class TFDemo5(object):
    """
    Session 是 Tensorflow 为了控制,和输出文件的执行的语句. 运行 session.run() 可以获得你要得知的运算结果,
    或者是你所要运算的部分，有两种使用Session的方式，我们可以从下面的例子中看出来,但在实际中，我们更推荐后者
    """

    def main(self):
        matrix1 = tf.constant([[3, 3]])
        matrix2 = tf.constant([[2], [2]])

        product = tf.matmul(matrix1, matrix2)

        sess = tf.Session()
        result = sess.run(product)
        print(result)
        sess.close()

        with tf.Session() as sess:
            result2 = sess.run(product)
            print(result2)
        pass


tfDemo = TFDemo5()
tfDemo.main()
