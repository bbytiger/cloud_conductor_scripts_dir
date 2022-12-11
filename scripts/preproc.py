from tensorflow.keras.datasets import mnist
import numpy as np
from scipy.ndimage.interpolation import shift
import time

def shift_image(image, dx, dy):
    image = image.reshape((28, 28))
    shifted_image = shift(image, [dy, dx], cval=0, mode="constant")
    return shifted_image


# for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
#      for image, label in zip(x_train, y_train):
#              X_train_augmented.append(shift_image(image, dx, dy))
#              y_train_augmented.append(label)


# run above for loop in parallel

import multiprocessing as mp

def run_with_ncpu(ncpu, X_train_augmented):
    pool = mp.Pool(ncpu)
    # start timer
    start = time.time()
    # with mp.Pool() as pool:
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [1]*x_train.shape[0], [0]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [-1]*x_train.shape[0], [0]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [0]*x_train.shape[0], [1]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [0]*x_train.shape[0], [-1]*x_train.shape[0]))
    

    X_train_augmented += pool.starmap(shift_image, zip(x_train, [2]*x_train.shape[0], [0]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [-2]*x_train.shape[0], [0]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [0]*x_train.shape[0], [2]*x_train.shape[0]))
    X_train_augmented += pool.starmap(shift_image, zip(x_train, [0]*x_train.shape[0], [-2]*x_train.shape[0]))
    # end timer
    end = time.time()
    print(end - start)
    return end - start

# apply shift image function to each image in x_train in parallel
# https://towardsdatascience.com/improving-accuracy-on-mnist-using-data-augmentation-b5c38eb5a903

if __name__ == '__main__':
    max_cpu = 8
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    print("finished loading mnist")
    X_train_augmented = [image for image in x_train]
    y_train_augmented = [image for image in y_train]
    X_train_augmented = np.array(X_train_augmented)
    y_train_augmented = np.array(y_train_augmented)

    print("starting results collection")
    results = []
    for i in range(1, max_cpu+1):
        results.append(run_with_ncpu(i, X_train_augmented))
    print(results)