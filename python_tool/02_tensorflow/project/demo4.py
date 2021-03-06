import unittest

import tensorflow as tf
import numpy as np


# tensorflow中大部分数据是float32
class TFDemo4(object):
    """
    想要预测的方程式y=0.1*x + 0.3,给定训练样本，通过梯度下降法来预测参数W和偏置b
    """

    def main(self):
        # create real data
        # 生成训练数据
        x_data = np.random.rand(100).astype(np.float32)
        y_data = x_data * 0.1 + 0.3

        ### create tensorflow structure start ###
        # 定义变量 Weights通过一个均匀分布随机产生，而bias则设置为0，同时二者的形状均为1维，因为就一个数嘛
        Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
        biases = tf.Variable(tf.zeros([1]))

        # 如何计算预测值
        y = Weights * x_data + biases

        # loss function
        loss = tf.reduce_mean(tf.square(y - y_data))

        # 梯度下降优化器，定义learning rate
        optimizer = tf.train.GradientDescentOptimizer(0.5)

        # 训练目标是loss最小化
        train = optimizer.minimize(loss)

        # 初始化变量，即初始化 Weights 和 biases
        init = tf.global_variables_initializer()

        # 创建session，进行参数初始化
        sess = tf.Session()
        sess.run(init)

        # 开始训练200步，每隔20步输出一下两个参数
        for step in range(201):
            sess.run(train)
            if step % 20 == 0:
                print(step, sess.run(Weights), sess.run(biases))
        pass


tfDemo4 = TFDemo4()
tfDemo4.main()
