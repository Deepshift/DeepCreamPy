import tensorflow as tf
import tensorflow.contrib.layers as layers
import numpy as np
import random as rr
import math as mt
import cv2
from scipy import misc

def instance_norm(input, name="instance_norm"):
    with tf.variable_scope(name):
        depth = input.get_shape()[3]
        scale = tf.get_variable("scale", [depth], initializer=tf.random_normal_initializer(1.0, 0.02, dtype=tf.float32))
        offset = tf.get_variable("offset", [depth], initializer=tf.constant_initializer(0.0))
        mean, variance = tf.nn.moments(input, axes=[1,2], keep_dims=True)
        epsilon = 1e-5
        inv = tf.rsqrt(variance + epsilon)
        normalized = (input-mean)*inv
        return scale*normalized + offset

def make_sq_mask(size, m_size, batch_size):

    start_x = rr.randint(0, size - m_size-1)
    start_y = rr.randint(0, size - m_size-1)

    temp = np.ones([batch_size, size, size, 3])

    temp[:, start_x:start_x + m_size, start_y:start_y + m_size, 0:3] *= 0

    return temp, start_x, start_y

def softmax(input):

    k = tf.exp(input - 3)
    k = tf.reduce_sum(k, 3, True)
    # k = k - num * tf.ones_like(k)

    ouput = tf.exp(input - 3) / k

    return ouput

def reduce_var(x, axis=None, keepdims=False):
    """Variance of a tensor, alongside the specified axis.

    # Arguments
        x: A tensor or variable.
        axis: An integer, the axis to compute the variance.
        keepdims: A boolean, whether to keep the dimensions or not.
            If `keepdims` is `False`, the rank of the tensor is reduced
            by 1. If `keepdims` is `True`,
            the reduced dimension is retained with length 1.

    # Returns
        A tensor with the variance of elements of `x`.
    """
    m = tf.reduce_mean(x, axis=axis, keepdims=True)
    devs_squared = tf.square(x - m)
    return tf.reduce_mean(devs_squared, axis=axis, keepdims=keepdims)

def reduce_std(x, axis=None, keepdims=False):
    """Standard deviation of a tensor, alongside the specified axis.

    # Arguments
        x: A tensor or variable.
        axis: An integer, the axis to compute the standard deviation.
        keepdims: A boolean, whether to keep the dimensions or not.
            If `keepdims` is `False`, the rank of the tensor is reduced
            by 1. If `keepdims` is `True`,
            the reduced dimension is retained with length 1.

    # Returns
        A tensor with the standard deviation of elements of `x`.
    """
    return tf.sqrt(reduce_var(x, axis=axis, keepdims=keepdims))

def l2_norm(v, eps=1e-12):
    return v / (tf.reduce_sum(v ** 2) ** 0.5 + eps)

def ff_mask(size, b_zise, maxLen, maxWid, maxAng, maxNum, maxVer, minLen = 20, minWid = 15, minVer = 5):

    mask = np.ones((b_zise, size, size, 3))

    num = rr.randint(3, maxNum)

    for i in range(num):
        startX = rr.randint(0, size)
        startY = rr.randint(0, size)
        numVer = rr.randint(minVer, maxVer)
        width = rr.randint(minWid, maxWid)
        for j in range(numVer):
            angle = rr.uniform(-maxAng, maxAng)
            length = rr.randint(minLen, maxLen)

            endX = min(size-1, max(0, int(startX + length * mt.sin(angle))))
            endY = min(size-1, max(0, int(startY + length * mt.cos(angle))))

            if endX >= startX:
                lowx = startX
                highx = endX
            else:
                lowx = endX
                highx = startX
            if endY >= startY:
                lowy = startY
                highy = endY
            else:
                lowy = endY
                highy = startY

            if abs(startY-endY) + abs(startX - endX) != 0:

                wlx = max(0, lowx-int(abs(width * mt.cos(angle))))
                whx = min(size - 1,  highx+1 + int(abs(width * mt.cos(angle))))
                wly = max(0, lowy - int(abs(width * mt.sin(angle))))
                why = min(size - 1, highy+1 + int(abs(width * mt.sin(angle))))

                for x in range(wlx, whx):
                    for y in range(wly, why):

                        d = abs((endY-startY)*x - (endX -startX)*y - endY*startX + startY*endX) / mt.sqrt((startY-endY)**2 + (startX -endX)**2)

                        if d <= width:
                            mask[:, x, y, :] = 0

            wlx = max(0, lowx-width)
            whx = min(size - 1, highx+width+1)
            wly = max(0, lowy - width)
            why = min(size - 1, highy + width + 1)

            for x2 in range(wlx, whx):
                for y2 in range(wly, why):

                    d1 = (startX - x2) ** 2 + (startY - y2) ** 2
                    d2 = (endX - x2) ** 2 + (endY - y2) ** 2

                    if np.sqrt(d1) <= width:
                        mask[:, x2, y2, :] = 0
                    if np.sqrt(d2) <= width:
                        mask[:, x2, y2, :] = 0
            startX = endX
            startY = endY

    return mask

def ff_mask_batch(size, b_size, maxLen, maxWid, maxAng, maxNum, maxVer, minLen = 20, minWid = 15, minVer = 5):

    mask = None
    temp = ff_mask(size, 1, maxLen, maxWid, maxAng, maxNum, maxVer, minLen=minLen, minWid=minWid, minVer=minVer)
    temp = temp[0]
    for ib in range(b_size):
        if ib == 0:
            mask = np.expand_dims(temp, 0)
        else:
            mask = np.concatenate((mask, np.expand_dims(temp, 0)), 0)

        temp = cv2.rotate(temp, cv2.ROTATE_90_CLOCKWISE)
        if ib == 3:
            temp = cv2.flip(temp, 0)

    return mask

def spectral_norm(w, name, iteration=1):
    w_shape = w.shape.as_list()
    w = tf.reshape(w, [-1, w_shape[-1]])

    u = tf.get_variable(name+"u", [1, w_shape[-1]], initializer=tf.truncated_normal_initializer(), trainable=False)

    u_hat = u
    v_hat = None
    for i in range(iteration):
        """
        power iteration
        Usually iteration = 1 will be enough
        """
        v_ = tf.matmul(u_hat, tf.transpose(w))
        v_hat = l2_norm(v_)

        u_ = tf.matmul(v_hat, w)
        u_hat = l2_norm(u_)

    sigma = tf.matmul(tf.matmul(v_hat, w), tf.transpose(u_hat))
    w_norm = w / sigma

    with tf.control_dependencies([u.assign(u_hat)]):
        w_norm = tf.reshape(w_norm, w_shape)

    return w_norm

def convolution_SN(tensor, output_dim, kernel_size, stride, name):
    _, h, w, c = [i.value for i in tensor.get_shape()]

    w = tf.get_variable(name=name + 'w', shape=[kernel_size, kernel_size, c, output_dim], initializer=layers.xavier_initializer())
    b = tf.get_variable(name=name + 'b', shape=[output_dim], initializer=tf.constant_initializer(0.0))

    output = tf.nn.conv2d(tensor, filter=spectral_norm(w, name=name + 'w'), strides=[1, stride, stride, 1], padding='SAME') + b

    return output

def dense_SN(tensor, output_dim, name):
    _, h, w, c = [i.value for i in tensor.get_shape()]

    w = tf.get_variable(name=name + 'w', shape=[h, w, c, output_dim], initializer=layers.xavier_initializer())
    b = tf.get_variable(name=name + 'b', shape=[output_dim], initializer=tf.constant_initializer(0.0))

    output = tf.nn.conv2d(tensor, filter=spectral_norm(w, name=name + 'w'), strides=[1, 1, 1, 1], padding='VALID') + b

    return output

def dense_RED_SN(tensor, name):
    sn_w = None

    _, h, w, c = [i.value for i in tensor.get_shape()]
    h = int(h)
    w = int(w)
    c = int(c)

    weight = tf.get_variable(name=name + '_w', shape=[h*w, 1, c, 1], initializer=layers.xavier_initializer())
    b = tf.get_variable(name=name + '_b', shape=[1, h, w, 1], initializer=tf.constant_initializer(0.0))

    for it in range(h*w):
        w_pixel = weight[it:it+1, :, :, :]
        sn_w_pixel = spectral_norm(w_pixel, name=name + 'w_%d' %it)

        if it == 0:
            sn_w = sn_w_pixel
        else:
            sn_w = tf.concat([sn_w, sn_w_pixel], axis=0)

    w_rs = tf.reshape(sn_w, [h, w, c, 1])
    w_rs_t = tf.transpose(w_rs, [3, 0, 1, 2])

    output_RED = tf.reduce_sum(tensor*w_rs_t + b, axis=3, keepdims=True)

    return output_RED