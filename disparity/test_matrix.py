import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


def load_transformation_matrix(filename):
    with open(filename, 'rb') as f:
        matrix = json.load(f)
    return np.array(matrix)


def read_coordinate(filename):
    with open(filename, 'r') as f:
        coordinates = json.load(f)
    return coordinates


def predict_msx_by_dc(coordinates_dc, matrix):
    coordinates_predict = {}
    trans_matrix = matrix.T  # reshape to (3, 2)
    for tag, coordinate in coordinates_dc.items():
        coordinate.append(1)
        coordinate = np.reshape(coordinate, (1, 3))
        predict_result = np.dot(coordinate, trans_matrix).tolist()[0]
        coordinates_predict[tag] = list(map(int, predict_result))  # cast float type to int
    return coordinates_predict


def show_prediction(coordinate_dc, coordinate_msx, matrix):
    pass


if __name__ == '__main__':
    folder = 'datasets/'
    matrix_file = '276d2ee1-186c-4b66-a6be-95afefbecdf6'
    matrix = load_transformation_matrix(folder + matrix_file + '_matrix.json')

    pic_file = '17a391b7-257f-4adc-8bf2-3a242495e05b'
    pic_file = 'a5fb6082-d435-47e3-9663-fc3f3d07c5c1'
    coordinates = read_coordinate(folder + pic_file + '.json')
    coordinates_dc = coordinates['dc']
    coordinates_msx = coordinates['msx']
    coordinates_predict = predict_msx_by_dc(coordinates_dc, matrix)
    print(coordinates_msx)
    print(coordinates_predict)

    img_dc = Image.open(folder + pic_file + '_dcBitmap.png')
    img_msx = Image.open(folder + pic_file + '_msxBitmap.png')

    fig = plt.figure()

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    for tag, coordinate in coordinates_dc.items():
        ax1.scatter(coordinate[0], coordinate[1])
        ax1.annotate(tag, (coordinate[0], coordinate[1]), color='g')
    for tag, coordinate in coordinates_msx.items():
        ax2.scatter(coordinate[0], coordinate[1])
        ax2.annotate(tag, (coordinate[0], coordinate[1]), color='g')
    for tag, coordinate in coordinates_predict.items():
        ax2.scatter(coordinate[0], coordinate[1], color='b')

    ax1.set_title('dc_pic')
    ax1.imshow(img_dc)
    ax2.set_title('msx_pic')
    ax2.imshow(img_msx)

    plt.show()

    print(matrix)
