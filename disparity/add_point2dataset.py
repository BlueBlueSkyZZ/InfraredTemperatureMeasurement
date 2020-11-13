import matplotlib.pyplot as plt
from PIL import Image
import json

global x, y, add_flag, pic_type, result
add_flag = True
result = {'dc': {}, 'msx': {}}


def on_press(event):
    global add_flag, x, y, pic_type
    pic_type = 'dc'
    x = int(event.xdata)
    y = int(event.ydata)
    add_flag = False


def on_press_msx(event):
    global add_flag, x, y, pic_type
    pic_type = 'msx'
    x = int(event.xdata)
    y = int(event.ydata)
    add_flag = False


def press_keyboard(event):
    global add_flag, x, y, result, pic_type
    if len(event.key) == 1:
        print(pic_type + ' ' + 'add success ' + event.key)
        result[pic_type][event.key] = [x, y]
        add_point(event, x, y, event.key)
        add_flag = True
    elif event.key == 'escape':
        print('exit')
        save2file()
        exit(0)


def add_point(event, x_coordinate, y_coordinate, tag=None):
    # refresh pic and show the location of point to judge if the point needs to be added
    plt.plot(x_coordinate, y_coordinate, 'o', color='r')
    if tag is not None:
        plt.annotate(tag, (x_coordinate, y_coordinate), color='g')
    event.inaxes.figure.canvas.draw()  # refresh the canvas


def save2file():
    global result
    # create a file and save the coordinate into json format
    suffix = filename_dc.split('_')[0]
    with open(folder + suffix+'.json', 'w') as f:
        json.dump(result, f)


folder = 'datasets/'

fig = plt.figure()
filename_dc = '17a391b7-257f-4adc-8bf2-3a242495e05b_dcBitmap.png'
img_dc = Image.open(folder + filename_dc)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('key_press_event', press_keyboard)
plt.imshow(img_dc, animated=True)


filename_msx = '17a391b7-257f-4adc-8bf2-3a242495e05b_msxBitmap.png'
img_msx = Image.open(folder + filename_msx)
fig2 = plt.figure()
plt.imshow(img_msx)
fig2.canvas.mpl_connect('button_press_event', on_press_msx)
fig2.canvas.mpl_connect('key_press_event', press_keyboard)

plt.show()

