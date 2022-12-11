# download MNIST dataset
import tensorflow as tf
from tensorflow.keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
import numpy as np
import multiprocessing as mp
import time

def augment_data_parallel(x_train, y_train, x_test, y_test):
    # Creating a new array with the same shape as the original array, but with an extra dimension.
    x_train_shifted = np.zeros((x_train.shape[0], x_train.shape[1], x_train.shape[2], 2))
    x_test_shifted = np.zeros((x_test.shape[0], x_test.shape[1], x_test.shape[2], 2))

    # Creating a pool of processes.
    # pool = mp.Pool(mp.cpu_count())
    pool = mp.Pool(1)

    x_train_shifted[:,:,:,0] = pool.starmap(np.roll, zip(x_train, [1]*x_train.shape[0], [0]*x_train.shape[0]))
    x_train_shifted[:,:,:,1] = pool.starmap(np.roll, zip(x_train, [1]*x_train.shape[0], [1]*x_train.shape[0]))
    x_test_shifted[:,:,:,0] = pool.starmap(np.roll, zip(x_test, [1]*x_test.shape[0], [0]*x_test.shape[0]))
    x_test_shifted[:,:,:,1] = pool.starmap(np.roll, zip(x_test, [1]*x_test.shape[0], [1]*x_test.shape[0]))

    return x_train_shifted, y_train, x_test_shifted, y_test

# augment MNIST dataset with pixel shifting
def augment_data(x_train, y_train, x_test, y_test):
    x_train_shifted = np.zeros((x_train.shape[0], x_train.shape[1], x_train.shape[2], 2))
    x_test_shifted = np.zeros((x_test.shape[0], x_test.shape[1], x_test.shape[2], 2))

    # print size of x_train_shifted
    print(x_train_shifted.shape)
    # print size of x_test_shifted
    print(x_test_shifted.shape)

    for i in range(x_train.shape[0]):
        x_train_shifted[i,:,:,0] = np.roll(x_train[i], 1, axis=0)
        x_train_shifted[i,:,:,1] = np.roll(x_train[i], 1, axis=1)

    for i in range(x_test.shape[0]):
        x_test_shifted[i,:,:,0] = np.roll(x_test[i], 1, axis=0)
        x_test_shifted[i,:,:,1] = np.roll(x_test[i], 1, axis=1)
    
        # print size of x_train_shifted
    print(x_train_shifted.shape)
    # print size of x_test_shifted
    print(x_test_shifted.shape)

    return x_train_shifted, y_train, x_test_shifted, y_test


if __name__ == '__main__':
    # start timer
    start = time.time()
    x_train_shifted, y_train, x_test_shifted, y_test = augment_data_parallel(x_train, y_train, x_test, y_test)

    # end timer and print time
    end = time.time()
    print(end - start)

    # save augmented MNIST dataset
    # np.savez_compressed('mnist_augmented.npz', x_train=x_train_shifted, y_train=y_train, x_test=x_test_shifted, y_test=y_test)

