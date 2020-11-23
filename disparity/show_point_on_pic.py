import matplotlib.pyplot as plt
from PIL import Image
import json
import numpy as np
import pandas as pd
import cv2


def read_coordinate(filename):
    with open(filename, 'r') as f:
        coordinates = json.load(f)
    return coordinates


def transformation_matrix(coordinates_dc, coordinates_msx):
    source, target = reshape_coordinate(coordinates_dc, coordinates_msx)
    transformation = cv2.estimateAffine2D(source, target, False)
    return transformation


def save_matrix2file(folder, filename, matrix):
    print(matrix)
    # with open(folder + filename + '.npy', 'wb') as f:
        # np.save(f, matrix)
    pd.Series(list(matrix)).to_json(folder + filename + '_matrix.json', orient='values')

def reshape_coordinate(coordinates_dc, coordinates_msx):
    source = []
    target = []
    for tag, coordinate in coordinates_dc.items():
        source.append(coordinate)
        target.append(coordinates_msx[tag])
    source = np.reshape(source, (-1, 2))
    target = np.reshape(target, (-1, 2))
    return source, target


def show_pic():
    folder = 'datasets/'
    suffix = '17a391b7-257f-4adc-8bf2-3a242495e05b'
    suffix = '276d2ee1-186c-4b66-a6be-95afefbecdf6'
    # suffix = '25629260-2b35-4450-bf66-eb0b57bbb29f'
    # suffix = 'a3cd8ecc-e8fa-4ae2-9f7f-690c080ed827'
    # suffix = 'a5fb6082-d435-47e3-9663-fc3f3d07c5c1'

    coordinates = read_coordinate(folder + suffix + '.json')
    coordinates_dc = coordinates['dc']
    coordinates_msx = coordinates['msx']

    trans_matrix = transformation_matrix(coordinates_dc, coordinates_msx)
    save_matrix2file(folder, suffix, trans_matrix[0])
    # print(trans_matrix)
    calculate_loss(trans_matrix, coordinates_dc, coordinates_msx)

    img_dc = Image.open(folder + suffix + '_dcBitmap.png')
    img_msx = Image.open(folder + suffix + '_msxBitmap.png')

    fig = plt.figure()

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    for tag, coordinate in coordinates_dc.items():
        ax1.scatter(coordinate[0], coordinate[1])
        ax1.annotate(tag, (coordinate[0], coordinate[1]), color='g')
    for tag, coordinate in coordinates_msx.items():
        ax2.scatter(coordinate[0], coordinate[1])
        ax2.annotate(tag, (coordinate[0], coordinate[1]), color='g')

    ax1.set_title('dc_pic')
    ax1.imshow(img_dc)
    ax2.set_title('msx_pic')
    ax2.imshow(img_msx)

    plt.show()


def calculate_loss(transformation, coordinates_dc, coordinates_msx):
    trans_matrix = transformation[0]
    trans_matrix = trans_matrix.T
    for tag, coordinate in coordinates_dc.items():
        coordinate.append(1)
        coordinate = np.reshape(coordinate, (1, 3))
        coordinate_predict = np.dot(coordinate, trans_matrix)
        # print(coordinate, coordinate_predict, coordinates_msx[tag])


if __name__ == '__main__':
    show_pic()

