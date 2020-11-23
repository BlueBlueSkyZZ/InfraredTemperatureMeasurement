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
        save2file(filename)
        exit(0)


def add_point(event, x_coordinate, y_coordinate, tag=None):
    # refresh pic and show the location of point to judge if the point needs to be added
    plt.plot(x_coordinate, y_coordinate, 'o', color='r')
    if tag is not None:
        plt.annotate(tag, (x_coordinate, y_coordinate), color='g')
    event.inaxes.figure.canvas.draw()  # refresh the canvas


def save2file(filename):
    global result
    # create a file and save the coordinate into json format
    # suffix = filename_dc.split('_')[0]
    suffix = filename
    with open(folder + suffix+'.json', 'w') as f:
        json.dump(result, f)


folder = 'datasets/'

filename = '17a391b7-257f-4adc-8bf2-3a242495e05b'  # ok
filename = '276d2ee1-186c-4b66-a6be-95afefbecdf6'
filename = '25629260-2b35-4450-bf66-eb0b57bbb29f'
filename = 'a3cd8ecc-e8fa-4ae2-9f7f-690c080ed827'
filename = 'a5fb6082-d435-47e3-9663-fc3f3d07c5c1'
filename = 'b8321512-2212-4780-914e-05680d9744f5'  # bad case
filename = 'c23feefc-550e-4a28-b648-f1c0a7fbf15d'  # bad case
filename = 'db01f50b-0329-43f8-b649-c0a9d175b8e2'


fig = plt.figure()
img_dc = Image.open(folder + filename + '_dcBitmap.png')
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('key_press_event', press_keyboard)
plt.imshow(img_dc, animated=True)

fig2 = plt.figure()
img_msx = Image.open(folder + filename + '_msxBitmap.png')
fig2.canvas.mpl_connect('button_press_event', on_press_msx)
fig2.canvas.mpl_connect('key_press_event', press_keyboard)
plt.imshow(img_msx)

plt.show()

