import numpy as np
from chainer import Variable
from sequential import Sequential
import link
import function
import util

# Linear test
x = np.random.normal(scale=1, size=(2, 28*28)).astype(np.float32)
x = Variable(x)

seq = Sequential(weight_initializer="GlorotNormal", weight_init_std=0.05)
seq.add(link.Linear(28*28, 500))
seq.add(link.BatchNormalization(500))
seq.add(link.Linear(500, 500))
seq.add(function.Activation("clipped_relu"))
seq.add(link.Linear(500, 500, use_weightnorm=True))
seq.add(function.Activation("crelu"))	# crelu outputs 2x 
seq.add(link.BatchNormalization(1000))
seq.add(link.Linear(1000, 500))
seq.add(function.Activation("elu"))
seq.add(link.Linear(500, 500, use_weightnorm=True))
seq.add(function.Activation("hard_sigmoid"))
seq.add(link.BatchNormalization(500))
seq.add(link.Linear(500, 500))
seq.add(function.Activation("leaky_relu"))
seq.add(link.Linear(500, 500, use_weightnorm=True))
seq.add(function.Activation("relu"))
seq.add(link.BatchNormalization(500))
seq.add(link.Linear(500, 500))
seq.add(function.Activation("sigmoid"))
seq.add(link.Linear(500, 500, use_weightnorm=True))
seq.add(function.Activation("softmax"))
seq.add(link.BatchNormalization(500))
seq.add(link.Linear(500, 500))
seq.add(function.Activation("softplus"))
seq.add(link.Linear(500, 500, use_weightnorm=True))
seq.add(function.Activation("tanh"))
seq.add(link.Linear(500, 10))
seq.build()

y = seq(x)
print y.data

# Conv test
x = np.random.normal(scale=1, size=(2, 3, 96, 96)).astype(np.float32)
x = Variable(x)

seq = Sequential(weight_initializer="GlorotNormal", weight_init_std=0.05)
seq.add(link.Convolution2D(3, 64, ksize=4, stride=2, pad=0))
seq.add(link.BatchNormalization(64))
seq.add(function.Activation("relu"))
seq.add(link.Convolution2D(64, 128, ksize=4, stride=2, pad=0))
seq.add(link.BatchNormalization(128))
seq.add(function.Activation("relu"))
seq.add(link.Convolution2D(128, 256, ksize=4, stride=2, pad=0))
seq.add(link.BatchNormalization(256))
seq.add(function.Activation("relu"))
seq.add(link.Convolution2D(256, 512, ksize=4, stride=2, pad=0))
seq.add(link.BatchNormalization(512))
seq.add(function.Activation("relu"))
seq.add(link.Convolution2D(512, 1024, ksize=4, stride=2, pad=0))
seq.add(link.BatchNormalization(1024))
seq.add(function.Activation("relu"))
seq.add(function.reshape_1d())
seq.add(link.Linear(None, 10, use_weightnorm=True))
seq.add(function.softmax())
seq.build()

y = seq(x)
print y.data

# Deconv test
x = np.random.normal(scale=1, size=(2, 100)).astype(np.float32)
x = Variable(x)

image_size = 96
# compute projection width
input_size = util.get_in_size_of_deconv_layers(image_size, num_layers=3, ksize=4, stride=2)
# compute required paddings
paddings = util.get_paddings_of_deconv_layers(image_size, num_layers=3, ksize=4, stride=2)

seq = Sequential(weight_initializer="GlorotNormal", weight_init_std=0.05)
seq.add(link.Linear(100, 64 * input_size ** 2))
seq.add(link.BatchNormalization(64 * input_size ** 2))
seq.add(function.Activation("relu"))
seq.add(function.reshape((-1, 64, input_size, input_size)))
seq.add(link.Deconvolution2D(64, 32, ksize=4, stride=2, pad=paddings.pop(0)))
seq.add(link.BatchNormalization(32))
seq.add(function.Activation("relu"))
seq.add(link.Deconvolution2D(32, 16, ksize=4, stride=2, pad=paddings.pop(0)))
seq.add(link.BatchNormalization(16))
seq.add(function.Activation("relu"))
seq.add(link.Deconvolution2D(16, 3, ksize=4, stride=2, pad=paddings.pop(0)))
seq.build()

y = seq(x)
print y.data.shape