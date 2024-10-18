from os.path import join

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cv2
from matplotlib.ticker import MaxNLocator


def resize_image(image, imsize):
    """
    Resize an image to a given width and height while maintaining its aspect ratio.

    Args:
        :param image: (numpy.ndarray): The input image.
        :param imsize: = tulpe (width (int),  height (int)): The desired size of the output image.
    Returns:
        numpy.ndarray: The resized image.
    """
    width, height = imsize
    # Get the dimensions of the input image
    img_height, img_width, channel = image.shape

    # Calculate the aspect ratio of the input image
    aspect_ratio = img_width / img_height

    # Calculate the aspect ratio of the output image
    output_aspect_ratio = width / height

    # Calculate the new dimensions of the output image
    if output_aspect_ratio > aspect_ratio:
        new_width = int(height * aspect_ratio)
        new_height = height
    else:
        new_width = width
        new_height = int(width / aspect_ratio)

    # Resize the input image to the new dimensions
    resized_image = cv2.resize(image, (new_width, new_height))

    # Create a black background of the desired output dimensions
    output_image = np.zeros((height, width, channel), dtype=np.uint8)

    # Calculate the coordinates to paste the resized image onto the output image
    x = (width - new_width) // 2
    y = (height - new_height) // 2

    # Paste the resized image onto the output image
    output_image[y:y + new_height, x:x + new_width] = resized_image

    return output_image


def Plot2Dict_onImage(image,
                      output_imsize=(1024, 600),
                      dict1=None,
                      dict2=None,
                      myTitle='ROIs in Data',
                      label1=None,
                      label2=None,
                      xLabel=None,
                      yLable=None,
                      cnt=None,
                      pDir=None
                      ):
    # Create stacked bar graph
    # plt.figure(figsize=(800//4,600//4))
    if dict1 is None:  # Example, default params
        dict1 = {'`A': 10, 'B': 20, 'C': 15, 'D': 25}
    if dict2 is None:
        dict2 = {'`A': 5, 'B': 10, 'C': 7, 'D': 12}
    # plt.figure(facecolor='none',  figsize=(120, 90), dpi=100)
    # fig.patch.set_alpha(0.5)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2, left=0.15)
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # Interger x axis
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Interger x axis  <<============ Remove if has many ROIs
    mpl.rcParams.update({'font.size': 24})
    plt.title(myTitle, fontsize=24)  # set title font size to 24 points
    plt.xlabel(xLabel, fontsize=24)  # set x-axis label font size to 18 points
    plt.ylabel(yLable, fontsize=24)  # set y-axis label font size to 18 points
    plt.xticks(fontsize=22)  # set x-axis tick label font size to 14 points
    plt.yticks(fontsize=22)  # set y-axis tick label font size to 14 points
    x = np.array(list(dict1.keys()))
    y1 = np.array(list(dict1.values()))
    y2 = np.array(list(dict2.values()))
    direct = 'ngang'
    if direct == 'doc':
        ax.barh(x, y1, label='')
        ax.barh(x, y2, bottom=y1, label='')
        ax.set_ylim(0, max(y1 + y2) + 5)  # set y-axis limits
    else:
        ax.barh(x, y1, label=label1)
        ax.barh(x, y2, left=y1, label=label2)

    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_title('Stacked Bar Graph')
    if cnt is not None:
        if cnt % 2 == 0:
            ax.legend()
    else:
        ax.legend()

    # Convert Matplotlib figure to CV2 image
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    if pDir is not None:
        p=f"{join(pDir,'ROI_his')}_{cnt%2}.png"
        print("Saved to: ", p)
        cv2.imwrite(p, img)
    # Get dimensions of the CV2 image and target image
    target_img = resize_image(image, output_imsize)
    target_height, target_width, _ = target_img.shape

    plotheight, plotwidth = target_height // 4, target_width // 4
    img = cv2.resize(img, (plotwidth, plotheight))
    img_height, img_width, _ = img.shape

    # Calculate coordinates of bottom right corner of target image
    x_coord = target_width - img_width
    y_coord = target_height - img_height - 10

    # Overlay CV2 image on target image
    target_img[y_coord:y_coord + plotheight, x_coord:x_coord + plotwidth] = img
    plt.close()
    del fig
    matplotlib.pyplot.close()
    return target_img
