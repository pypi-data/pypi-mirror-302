import datetime
import time
from pprint import pp
import ntanh
APP_NAME="AI_yolo_label_checker"

sHelp = """
Các chức năng của chương trình:
    Hiển thị tổng số ảnh, tổng số nhãn mỗi ROI 
Phím tắt:
    Phím mũi tên: lên, phải: ảnh tiếp theo
                  Xuống, trái: quay lại ảnh trước đó
    Phím *: Bật/Tắt chế độ in chữ trên ảnh ra màn hình (để kiểm tra xem ảnh hiện tại là ảnh nào, tên gì)
    Phím -: Giảm kích cỡ chữ in trên màn hình (nhìn dc nhiều thông tin hơn)  
    Phím =: Tăng kích cỡ chữ in trên màn hình (nhìn rõ hơn)  
    
    F1: Trích xuất riêng tất cả các ROIs ra thành folder để kiểm tra xem có bị đánh lộn nhãn không (đánh thiếu phải xem trên ảnh)
    F3, F5, F6: Plot ROI ra ảnh, lưu lại (path in ra màn hình lúc bấm phím), có 3 kiểu plot khác nhau cho dễ phân biệt
    F4: In tọa độ Cover ROI ra màn hình
    F7, F8: thay đổi độ dày của ROI đang vẽ.
    F11, F12: giảm/tăng cỡ chữ của ROI.
    
    "F1"  : Extract Rois
    "F2"  : Open config file for next time use
    "F3"  : Plot Overlay
    "F4"  : print cover box
    "F5"  : Plot Overlay
    "F6"  : Plot Overlay
    "F7"  : Line width -
    "F8"  : Line width +
    "F9"  : windows -
    "F10" : windows +
    "F11" : Text-
    "F12" : Text +
        
    ` (dấu ~): in đường dẫn file ảnh hiện tại.
    Bấm phím số rồi ENTER: hiển thị ảnh có STT vừa bấm.
    Phím ESC: thoát 
"""
import random
import shutil
from collections import OrderedDict
from os.path import dirname, basename, join, exists, isfile

import cv2
import os
import subprocess

# import AiLibs
# image_dirname = '/images'
# label_dirname = '/labels'


# =============================================================================================
from os.path import join

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cv2
from matplotlib.ticker import MaxNLocator

import cv2


# Hàm chuyển key thành tên phím
def print_key_name(key):
    if key == -1:
        return  # Không có phím nào được nhấn

    # Các phím điều khiển đặc biệt
    special_keys = {
        27: "ESC",
        13: "ENTER",
        8: "BACKSPACE",
        9: "TAB",
        32: "SPACE",
        2555904: "RIGHT_ARROW",
        2424832: "LEFT_ARROW",
        2490368: "UP_ARROW",
        2621440: "DOWN_ARROW",
        3014656: "SHIFT",
        3080192: "CTRL",
        262145: "ALT",
        # Bạn có thể thêm nhiều phím đặc biệt khác tại đây
        # Nhóm phím Function (F1 đến F12) với mã từ bạn cung cấp
        7340032: "F1",  # Extract Rois
        7405568: "F2",  # Open config file for next time use
        7471104: "F3",  # Plot Overlay
        7536640: "F4",  # print cover box
        7602176: "F5",  # Plot Overlay
        7667712: "F6",  # Plot Overlay
        7733248: "F7",  # Line width -
        7798784: "F8",  # Line width +
        7864320: "F9",  # windows -
        7929856: "F10",  # windows +
        7995392: "F11",  # Text-
        8060928: "F12",  # Text +
    }

    if key in special_keys:
        print(f"Key pressed: {key}: {special_keys[key]}")
    elif 32 <= key <= 126:  # Các ký tự in được
        print(f"Key pressed: {key} {chr(key)}")
    else:
        print(f"Unknown key: {key}")


class AiLibs:
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
        output_image[y : y + new_height, x : x + new_width] = resized_image

        return output_image

    def Plot2Dict_onImage(
        image,
        output_imsize=(1024, 600),
        dict1=None,
        dict2=None,
        myTitle="ROIs in Data",
        label1=None,
        label2=None,
        xLabel=None,
        yLable=None,
        cnt=None,
        pDir=None,
    ):
        # Create stacked bar graph
        # plt.figure(figsize=(800//4,600//4))
        if dict1 is None:  # Example, default params
            dict1 = {"`A": 10, "B": 20, "C": 15, "D": 25}
        if dict2 is None:
            dict2 = {"`A": 5, "B": 10, "C": 7, "D": 12}
        # plt.figure(facecolor='none',  figsize=(120, 90), dpi=100)
        # fig.patch.set_alpha(0.5)

        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2, left=0.15)
        # ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # Interger x axis
        ax.yaxis.set_major_locator(
            MaxNLocator(integer=True)
        )  # Interger x axis  <<============ Remove if has many ROIs
        mpl.rcParams.update({"font.size": 24})
        plt.title(myTitle, fontsize=24)  # set title font size to 24 points
        plt.xlabel(xLabel, fontsize=24)  # set x-axis label font size to 18 points
        plt.ylabel(yLable, fontsize=24)  # set y-axis label font size to 18 points
        plt.xticks(fontsize=22)  # set x-axis tick label font size to 14 points
        plt.yticks(fontsize=22)  # set y-axis tick label font size to 14 points
        x = np.array(list(dict1.keys()))
        y1 = np.array(list(dict1.values()))
        y2 = np.array(list(dict2.values()))
        direct = "ngang"
        if direct == "doc":
            ax.barh(x, y1, label="")
            ax.barh(x, y2, bottom=y1, label="")
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
        img = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(
            fig.canvas.get_width_height()[::-1] + (4,)
        )  # Shape with 4 channels (RGBA)
        img = img[:, :, :3]  # Bỏ kênh alpha, chỉ lấy RGB

        if pDir is not None:
            p = f"{join(pDir,'ROI_his')}_{cnt%2}.png"
            print("Saved to: ", p)
            cv2.imwrite(p, img)
        # Get dimensions of the CV2 image and target image
        target_img = AiLibs.resize_image(image, output_imsize)
        target_height, target_width, _ = target_img.shape

        plotheight, plotwidth = target_height // 4, target_width // 4
        img = cv2.resize(img, (plotwidth, plotheight))
        img_height, img_width, _ = img.shape

        # Calculate coordinates of bottom right corner of target image
        x_coord = target_width - img_width
        y_coord = target_height - img_height - 10

        # Overlay CV2 image on target image
        target_img[y_coord : y_coord + plotheight, x_coord : x_coord + plotwidth] = img
        plt.close()
        del fig
        matplotlib.pyplot.close()
        return target_img


# =============================================================================================
import tkinter as tk
from tkinter import ttk

import yaml
from numpy.core.defchararray import isnumeric
from tqdm import tqdm

import numpy as np


def swap_left_right(image):
    # Lấy kích thước của ảnh
    height, width = image.shape[:2]

    # Tính vị trí giữa của ảnh
    mid = width // 2

    # Chia ảnh thành hai nửa
    left_half = image[:, :mid]
    right_half = image[:, mid:]

    # Đổi hai nửa và ghép lại
    swapped_image = np.hstack((right_half, left_half))

    return swapped_image


def runApp(RunningClick=False):
    # Read config: ------------------------------------------
    cfg = taLibs.LoadConfigFromfiles()
    print(cfg)

    pDir1 = cfg["pDir1"]
    pDir2 = cfg["pDir2"]
    pDir3 = cfg["pDir3"]
    if not RunningClick:
        pDir1 = os.getcwd()

    print("Current dir:", pDir1)
    RandColor = cfg["RandColor"]
    fDraw_ROI_2_Imgs = cfg["fDraw_ROI_2_Imgs"]
    CollectLabel = int(cfg["CollectLabel"])
    Rename_files_Src = cfg["Rename_files_Src"]
    Rename_files_Des = cfg["Rename_files_Des"]
    Rename_files_Pre = cfg["Rename_files_Pre"]
    Resized_W = cfg["Resized_W"]
    Resized_H = cfg["Resized_H"]
    fResize = cfg["fResize"]
    fMove2Test = cfg["fMove2Test"]

    clicked = False
    Run_Program = 1

    # ---------------------------------------------------------------------
    # Make GUI:
    # Create an instance of Tkinter frame
    win = tk.Tk()
    # Set the geometry of Tkinter frame
    # win.geometry("750x550")
    tab_control = ttk.Notebook()
    tab_control.pack(side="left", expand=True)

    tab1 = tk.Frame(tab_control)
    tab1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tab_control.add(tab1, text="Phần mềm Xem ảnh/Nhãn Yolo")

    tab2 = tk.Frame(tab_control)
    tab2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
    tab_control.add(tab2, text="Đổi tên Ảnh+Label")

    tab3 = tk.Frame(tab_control)
    tab3.pack(side=tk.TOP, padx=10, pady=10)
    tab_control.add(tab3, text="Resize Image")

    tab4 = tk.Frame(tab_control)
    tab4.pack(side=tk.TOP, padx=10, pady=10)
    tab_control.add(tab4, text="Make Test Folder From Train Folder")

    def lblEntry(frm, txt, vl):  # Initialize a Label to display the User Input
        ttk.Label(frm, text=txt).pack(
            side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2
        )  # Create an Entry widget to accept User Input
        # tvar=tk.StringVar(value=vl)
        entry = ttk.Entry(frm)
        entry.pack(
            side=tk.TOP, expand=True, fill="x", anchor="nw", padx=5, pady=5, ipadx=2
        )
        entry.insert(0, vl)
        return entry

    if "Hiển thị TAB1":
        # ttk.Label(tab1, text='Phần mềm xem ảnh từ YOLO',).pack(side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2)
        frm1 = ttk.LabelFrame(tab1, text="Xem nhãn YOLO", borderwidth=1, border=1)
        frm1.pack(
            side=tk.TOP,
            expand=True,
            anchor="center",
            fill="x",
            padx=20,
            pady=1,
            ipadx=2,
        )

        entry1 = lblEntry(
            frm1,
            "Dir 1: Thư mục cần xem gồm có thư mục con + thư mục ảnh (có thể +txt)",
            pDir1,
        )
        entry2 = lblEntry(frm1, "Dir 2: Thư mục txt (nếu khác Dir 1)", pDir2)
        entry3 = lblEntry(
            frm1,
            "Dir 3: Move missing label to here: Thư mục chứa files thiếu file nhãn",
            pDir3,
        )
        entry1.focus_set()
        fRandColor = tk.BooleanVar(value=RandColor)
        checkConfigLedBtn1 = ttk.Checkbutton(
            frm1,
            text="RandColor (mỗi lần thay đổi hiện thị, mỗi nhãn sẽ có 1 màu mới)",
            variable=fRandColor,
        )
        checkConfigLedBtn1.pack(
            side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2
        )

        DrawROI_SaveImg = tk.BooleanVar(value=fDraw_ROI_2_Imgs)
        checkConfigLedBtn2 = ttk.Checkbutton(
            frm1,
            text="Vẽ ROI vào ảnh => Save dir (tự động Open dir khi làm xong) ",
            variable=DrawROI_SaveImg,
        )
        checkConfigLedBtn2.pack(
            side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2
        )

        frm2 = ttk.LabelFrame(tab1, text="Tách Image/Label theo nhãn")
        frm2.pack(side="top", expand=True, fill="both", padx=20, pady=1, ipadx=2)
        entry_CollectLabel = lblEntry(
            frm2,
            "Label mà bạn muốn tách ra khỏi Data, =-1 nghĩa là không tách, = số => Tách nhãn có số đó ra",
            CollectLabel,
        )

        def display_text():
            nonlocal pDir1, pDir2, pDir3, clicked, Run_Program, CollectLabel, fDraw_ROI_2_Imgs, Resized_W, Resized_H, RandColor, cfg
            pDir1 = entry1.get().replace('"', "")
            pDir2 = entry2.get().replace('"', "")
            pDir3 = entry3.get().replace('"', "")
            clicked = True
            Run_Program = 1
            CollectLabel = entry_CollectLabel.get()
            if isnumeric(CollectLabel):
                CollectLabel = int(CollectLabel)
            fDraw_ROI_2_Imgs = int(DrawROI_SaveImg.get())
            Resized_W = int(inpResized_W.get())
            Resized_H = int(inpResized_H.get())
            RandColor = fRandColor.get()
            cfg["pDir1"] = pDir1
            cfg["pDir2"] = pDir2
            cfg["pDir3"] = pDir3
            cfg["RandColor"] = RandColor
            cfg["fDraw_ROI_2_Imgs"] = fDraw_ROI_2_Imgs
            cfg["CollectLabel"] = CollectLabel
            # cfg['Rename_files_Src'] =Rename_files_Src
            # cfg['Rename_files_Des'] =Rename_files_Des
            # cfg['Rename_files_Pre'] =Rename_files_Pre
            # cfg['Resized_W'] =Resized_W
            # cfg['Resized_H'] =Resized_H
            # cfg['fResize'] =fResize
            taLibs.fnSaveConfigFile(cfg)
            win.destroy()

        # Create a Button to validate Entry Widget
        ttk.Button(tab1, text="Okay", width=20, command=display_text).pack(pady=20)
    if "Tab2":
        frm2 = ttk.LabelFrame(
            tab2,
            text="Đổi tên ảnh + label để hòa nhập 2 kho Yolo data (khi có ảnh trùng tên)",
        )
        frm2.pack(side="top", expand=True, fill="both", padx=20, pady=1, ipadx=2)

        tab2_entry1 = lblEntry(frm2, "Dir 1: Source Dir", Rename_files_Src)
        tab2_entry2 = lblEntry(frm2, "Dir 2: Des dir", Rename_files_Des)
        tab2_entry3 = lblEntry(
            frm2, "Prefix text (Text thêm vào đầu ảnh/label)", Rename_files_Pre
        )
        tab2_entry1.focus_set()

        def TachLabelKhoiYolo():
            nonlocal pDir1, pDir2, Run_Program, clicked, cfg, Rename_files_Pre
            pDir1 = tab2_entry1.get()
            pDir2 = tab2_entry2.get()
            Rename_files_Pre = tab2_entry3.get()
            cfg["Rename_files_Src"] = pDir1
            cfg["Rename_files_Des"] = pDir2
            cfg["Rename_files_Pre"] = Rename_files_Pre
            taLibs.fnSaveConfigFile(cfg)
            Run_Program = 2
            clicked = 1
            win.destroy()
            pass

        btn_t2 = ttk.Button(tab2, text="Okay", width=20, command=TachLabelKhoiYolo)
        btn_t2.pack(pady=20)
        pass

    if "TAB 3":
        frm3 = ttk.LabelFrame(tab3, text="Resize Image")
        frm3.pack(side="top", expand=True, fill="both", padx=20, pady=1, ipadx=2)

        def fnTab3():
            nonlocal pDir1, pDir2, clicked, Run_Program, fResize, Resized_W, Resized_H
            pDir1 = resizeEntry1.get().replace('"', "").replace("\\", "/")
            pDir2 = resizeEntry2.get().replace('"', "").replace("\\", "/")
            fResize = resizevl3.get()
            Resized_W = int(inpResized_W.get())
            Resized_H = int(inpResized_H.get())
            Run_Program = 3
            clicked = 1
            win.destroy()

        resizeEntry1 = lblEntry(frm3, "Image Input", pDir1)
        resizeEntry2 = lblEntry(frm3, "Image Output", pDir1)
        resizevl3 = tk.BooleanVar(value=fResize)
        chkResize3 = ttk.Checkbutton(frm3, text="Rezise ảnh", variable=resizevl3)
        chkResize3.pack(side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2)
        inpResized_W = lblEntry(frm3, "Resized W", Resized_W)
        inpResized_H = lblEntry(frm3, "Resized H", Resized_H)
        ttk.Button(frm3, text="Resize", width=20, command=fnTab3).pack(pady=20)
    if "TAB 4":
        frm4 = ttk.LabelFrame(tab4, text="Create Test folder")
        frm4.pack(side="top", expand=True, fill="both", padx=20, pady=1, ipadx=2)

        def fnTab4():
            nonlocal pDir1, pDir2, clicked, Run_Program, fResize, Resized_W, Resized_H, fMove2Test
            pDir1 = resizeEntry1.get().replace('"', "").replace("\\", "/")
            pDir2 = resizeEntry2.get().replace('"', "").replace("\\", "/")
            fResize = resizevl4.get()
            fMove2Test = fchkMove2Test.get()
            Resized_W = int(inpResized_W.get())
            Resized_H = int(inpResized_H.get())
            Run_Program = 4
            clicked = 1
            win.destroy()

        resizeEntry1 = lblEntry(frm4, "Image Input", pDir1)
        resizeEntry2 = lblEntry(frm4, "Image Output", pDir1)
        resizevl4 = tk.BooleanVar(value=fResize)
        fchkMove2Test = tk.BooleanVar(value=fMove2Test)

        chkResize4 = ttk.Checkbutton(
            frm4, text="Resize image in folder: ___imgs_from_videos", variable=resizevl4
        )
        chkResize4.pack(side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2)
        inpResized_W = lblEntry(frm4, "Resized W", Resized_W)
        inpResized_H = lblEntry(frm4, "Resized H", Resized_H)

        chkMove2Test = ttk.Checkbutton(
            frm4, text="Move ảnh sang Test folder", variable=fchkMove2Test
        )
        chkMove2Test.pack(
            side=tk.TOP, expand=True, anchor=tk.NW, padx=5, pady=1, ipadx=2
        )
        ttk.Button(frm4, text="Do this work", width=20, command=fnTab4).pack(pady=20)

    win.mainloop()
    print("pDir1=", pDir1)
    print("pDir2=", pDir2)
    # print(pDir1)
    if not clicked:
        exit()
    # if 1 == Run_Program:
    if Run_Program < 3:
        RunProgram(
            Run_Program=Run_Program,
            pDir1=pDir1,
            pDir2=pDir2,
            pDir3=pDir3,
            RandColor=fRandColor.get(),
            fDraw_ROI_2_Imgs=fDraw_ROI_2_Imgs,
            CollectLabel=CollectLabel,
            cfg=cfg,
        )
    if Run_Program == 3 and fResize:
        ResizeImage(pDir1, Resized_W, Resized_H, pDir2)
        pass
    if Run_Program == 4:
        fnMake_Test_folder(pDir1, fResize, Resized_W, Resized_H, pDir2, fMove2Test)
        pass


def fnMake_Test_folder(
    pDir1, fResize, Resized_W, Resized_H, pDir2=None, fMove_files_to_test_Folder=None
):
    if fResize:
        if not pDir2:
            pDir2 = pDir1 + "__Resize"
        fis = taLibs.getFiles(pDir1)
        pDir1 = pDir1.replace("\\", "/")
        pDir2 = pDir2.replace("\\", "/")
        if pDir2:
            os.makedirs(pDir2, exist_ok=True)
            print("Create dir:", pDir2)
        Nimg = len(fis)
        for fn in tqdm(fis):
            img = taLibs.fnResize1Img(fn, Resized_W, Resized_H, ResizeType="same")
            fnDes = fn.replace(pDir1, pDir2)
            cv2.imwrite(fnDes, img)
            # if k % 100 == 0:
            #     print(f"{k}/{Nimg}")
        print("Resize Done!")
    if not pDir2 or pDir1 == pDir2:
        pDir2 = pDir1 + "__TestData"
    print()
    print("Input  dir:", pDir1)
    print("Output dir:", pDir2)
    if fMove_files_to_test_Folder:
        print("Create mode: Move 20% from Input to Output dir")
    else:
        print("Create mode: Copy 20% from Input to Output dir")

    for D, _, F in os.walk(pDir1):
        filtered = list(filter(lambda myfn: myfn.endswith(".jpg"), F))
        if len(filtered) > 4:
            sample_list = random.choices(filtered, k=round(len(filtered) * 0.2))
            for fn in sample_list:
                fn = join(D, fn)
                if exists(fn.replace(".jpg", ".avi")):
                    continue  # Nếu là ảnh có video đi kèm thì bỏ qua.
                fnDes = fn.replace(pDir1, pDir2)
                fntxt = fn.replace(".jpg", ".txt")
                fnTxT_Des = fntxt.replace(pDir1, pDir2)
                myFunc = shutil.copy
                if fMove_files_to_test_Folder:
                    myFunc = shutil.move
                os.makedirs(dirname(fnDes), exist_ok=True)
                print("Create dir fnDes:", fnDes)
                myFunc(fn, fnDes)
                myFunc(fntxt, fnTxT_Des)
    print("Done!")


def ResizeImage(pDir1, Resized_W, Resized_H, pDir2=None):
    if not pDir2:
        pDir2 = pDir1 + "__Resize"
    fis = taLibs.getFiles(pDir1)
    pDir1 = pDir1.replace("\\", "/")
    pDir2 = pDir2.replace("\\", "/")
    if pDir2:
        os.makedirs(pDir2, exist_ok=True)
        print("Create pDir2 ResizeImage:", pDir2)
    Nimg = len(fis)
    for fn in tqdm(fis):
        img = taLibs.fnResize1Img(fn, Resized_W, Resized_H, ResizeType="same")
        fnDes = fn.replace(pDir1, pDir2)
        cv2.imwrite(fnDes, img)
        # if k % 100 == 0:
        #     print(f"{k}/{Nimg}")
    print("Resize Done!")


def RunProgram(
    Run_Program=1,
    pDir1=r"E:\DATA-SupperCAP\Step1_2---SUPERCAP_DATA\images\1.jpg",
    pDir2=r"E:\DATA-SupperCAP\Step1_2---SUPERCAP_DATA\labels",  # pImdir
    pDir3="",
    RandColor=True,  # Mỗi ảnh sẽ có tập màu ngẫu nhiên, ROI cùng tên thì cùng màu
    fDraw_ROI_2_Imgs=False,
    # Nếu =True, chỉ xuất ảnh ra thư mục, không hiển thị. =False: chỉ hiển thị, không xuất ảnh.
    CollectLabel=-1,
    # = None nếu không muốn move files ra thư mục khác, = nhãn nếu muốn move ra thư mục khác (vd nhãn =4)
    cfg=None,
):
    print("Press ESC to exit App")
    if 1 == Run_Program:  # Check YoloData
        # Check Yolo Images/Labels folder để kiểm tra xem nhãn nào vẽ ở đâu, số lượng ảnh bao nhiêu, mỗi nhãn có số lượng bao nhiêu.
        CheckYolo_Data(
            pDir1, pDir2, pDir3, RandColor=RandColor, CollectLabel=CollectLabel, cfg=cfg
        )

    if 2 == Run_Program:  # Rename imgage/label files
        Src_images_labels = pDir1  # r'E:\DATA-SupperCAP\STEP2-SUPERCAP'
        Des_images_labels = pDir2  # r'E:\DATA-SupperCAP\STEP2-SUPERCAP'
        prefix = "fold3_"  # Tên riêng, đặc trưng của thư mục này, nó sẽ thêm vào đầu của tất cả các ảnh và label tương ứng.
        Merge_Yolo_Data(Src_images_labels, Des_images_labels, prefix=prefix)


# =============================================================================================
# =============================================================================================
# =============================================================================================


# =============================================================================================
# from libs import taLibs

# os.makedirs("IVIS_data", exist_ok=True)
Fontscale = 1
fPrint_text = 0


class taLibs:
    def fnList_2Count(mlist):
        mDict = {}
        for x in mlist:
            mDict[x] = mDict[x] + 1 if x in mDict else 1
        mDict = dict(sorted(mDict.items(), key=lambda key_value: key_value[0]))
        return mDict

    def fnResize1Img(fn, Resized_W, Resized_H, ResizeType="same"):
        img = cv2.imread(fn)
        if ResizeType == "same":
            img = cv2.resize(
                img, dsize=(Resized_W, Resized_H), interpolation=cv2.INTER_CUBIC
            )
        if ResizeType == "MaxWidth":
            pass
        if ResizeType == "MaxHeight":
            pass

        return img

    def LoadConfigFromfiles(ymlPath: str = "config.yml"):
        if ymlPath.startswith("IVIS_data"):
            ymlPath = basename( ymlPath )  
            # tương thích với version cũ: truyền vào 'IVIS_data/config.yml'
            
        rootDir = ntanh.ParamsBase.get_Home_Dir(APP_NAME)
        IVIS_data_dir = join(rootDir, "IVIS_data")
        os.makedirs(IVIS_data_dir, exist_ok=True)

        ymlPath = join(IVIS_data_dir, ymlPath)
        print(f"LoadConfigFromfiles('{ymlPath}')")

        if not exists(ymlPath):  # Create new config file
            print("# Create new config file")             
            fnta = join(IVIS_data_dir, "system.ta")

            if not exists(fnta):
                with open(fnta, "w", encoding="utf-8") as fntaFile:
                    fntaFile.write(
                        r"""CollectLabel: '-1'
RandColor: true
Rename_files_Des: E:\DATA-SupperCAP\STEP2-SUPERCAP
Rename_files_Pre: im2_
Rename_files_Src: E:\DATA-SupperCAP\STEP2-SUPERCAP
Resized_H: 640
Resized_W: 640
fDraw_ROI_2_Imgs: 0
fMove2Test: false
fResize: false
pDir1: H:\DATA\Cam360SmartGate\Training_data_from_DUY\_Train\11_10\4
pDir2: ''
pDir3: ''
show_full_txt_path_on_image: false
swapHorizontal: false
"""
                    )
            with open(fnta, "r", encoding="utf-8") as ymlfile:
                cfg0 = yaml.load(ymlfile, Loader=yaml.FullLoader)
            taLibs.fnSaveConfigFile(cfg0, ymlPath)
            pass
        with open(ymlPath, "r", encoding="utf-8") as ymlfile:
            mcfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return mcfg

    def fnSaveConfigFile(cfg, ymlPath="IVIS_data/config.yml"):
        
        if ymlPath.startswith("IVIS_data"):            ymlPath = basename( ymlPath )               
        rootDir = ntanh.ParamsBase.get_Home_Dir(APP_NAME)
        IVIS_data_dir = join(rootDir, "IVIS_data")
        os.makedirs(IVIS_data_dir, exist_ok=True)
        ymlPath = join(IVIS_data_dir, ymlPath)
        
        with open(ymlPath, "w", encoding="utf-8") as yaml_file:
            yaml.dump(cfg, yaml_file, default_flow_style=False)
        pass

    def fnExplore(spath: str):
        FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
        # explorer would choke on forward slashes
        spath = os.path.normpath(spath)
        if os.path.isdir(spath):
            subprocess.run([FILEBROWSER_PATH, spath])
        elif os.path.isfile(spath):
            subprocess.run([FILEBROWSER_PATH, "/select,", spath])

    def Yolo_to_Box(imShape: tuple, sYoloBox):
        h, w = imShape[:2]
        # extract x1, y1 <- center, width, height
        mID = int(sYoloBox.split(" ")[0])
        x1 = int(float(sYoloBox.split(" ")[1]) * w)
        y1 = int(float(sYoloBox.split(" ")[2]) * h)
        xw = int(float(sYoloBox.split(" ")[3]) * w / 2)
        yw = int(float(sYoloBox.split(" ")[4]) * h / 2)
        # make x1,y1, x2,y2
        start_point = (x1 - xw, y1 - yw)
        end_point = (x1 + xw, y1 + yw)
        # draw rectangle
        # cvmat = cv2.rectangle(cvmat, start_point, end_point, (255, 0, 0), 2)
        x1, y1 = start_point
        x2, y2 = end_point
        return mID, [x1, y1, x2, y2]

    def getFiles(sPath: str, ext=(".jpg",)):
        infis = []
        for D, _, F in os.walk(sPath):
            for fn in F:
                if fn.endswith(ext):
                    infis.append(join(D, fn).replace("\\", "/"))
        return infis

    import cv2

    def image_resize(image, height, inter=cv2.INTER_AREA):
        # Lấy kích thước hiện tại của ảnh
        (h, w) = image.shape[:2]

        # Tính toán chiều rộng mới để giữ nguyên tỷ lệ
        aspect_ratio = w / h
        new_width = int(height * aspect_ratio)

        # Resize ảnh với chiều cao mới và chiều rộng đã tính
        resized_image = cv2.resize(image, (new_width, height), interpolation=inter)

        return resized_image

    def image_resize_w(image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def put_text_top(img, LINES, scolor=None, showAll=False):
        sbox, txt, tbox, tbox_vids, allRois = LINES

        stbox = str(tbox).replace(": ", ":")  # ROI image
        stbox_vids = str(tbox_vids).replace(": ", ":")  # ROI Video
        allRois = str(allRois).replace(": ", ":")  # ROI total

        # font = random.randint(0,6) # cv2.FONT_HERSHEY_SIMPLEX
        font = 2  # 0..7
        # fontScale = img.shape[0] / 1100  # 0.6
        fontScale = (img.shape[0] / 1200) * Fontscale  # 0.6
        h = round((fontScale * img.shape[0]) // 22)  # 24
        Line1 = (h, h)  # (24,24)
        Line2 = (4 * h, 2 * h)  # (24,48)
        Line3 = (4 * h, 3 * h)  # (24,48)
        Line4 = (4 * h, 4 * h)  # (24,48)
        fontColor = (204, 0, 102)  # '#6600cc' # (0, 255, 0)
        BgColor = (153, 255, 255)  # (0, 0, 0)
        thickness = 1
        lineType = 1

        if fPrint_text:
            print(txt)
            print(tbox)
            print()

        def put1Line(img, txt, Line1, font, fontScale, BgColor, thickness, lineType):
            cv2.putText(
                img, txt, Line1, font, fontScale, BgColor, thickness * 3, lineType
            )
            cv2.putText(
                img, txt, Line1, font, fontScale, fontColor, thickness, lineType
            )

        put1Line(img, txt, Line1, font, fontScale, BgColor, thickness, lineType)
        if showAll:
            put1Line(
                img,
                "JPG:" + stbox,
                Line2,
                font,
                fontScale,
                BgColor,
                thickness,
                lineType,
            )
            put1Line(
                img,
                "VID:" + stbox_vids,
                Line3,
                font,
                fontScale,
                BgColor,
                thickness,
                lineType,
            )
            put1Line(
                img,
                "ALL:" + allRois,
                Line4,
                font,
                fontScale,
                BgColor,
                thickness,
                lineType,
            )

        if scolor:
            drawed = {}
            colored = {}
            for k, [mID, scolor] in enumerate(zip(sbox, scolor)):
                drawed[mID] = drawed[mID] + 1 if mID in drawed else 1
                colored[mID] = scolor

            # for k, [mID, scolor] in enumerate(zip(sbox, scolor)):
            for k, (mID, mNumber) in enumerate(drawed.items()):
                scolor = colored[mID]
                line = (h, (k + 3) * h)
                # cv2.putText(img, f"Box:{mID}", line, font, fontScale, (255,255,255), thickness*2+2, lineType)
                cv2.putText(
                    img,
                    f"{mID}: {mNumber}",
                    line,
                    font,
                    fontScale,
                    (255, 255, 255),
                    thickness * 2,
                    lineType,
                )
                cv2.putText(
                    img,
                    f"{mID}: {mNumber}",
                    line,
                    font,
                    fontScale,
                    scolor,
                    thickness,
                    lineType,
                )

        return img

    def put_text_top0(img, txt, x, tbox=None, sbox=None, scolor=None):
        # font = random.randint(0,6) # cv2.FONT_HERSHEY_SIMPLEX
        font = 2  # 0..7
        h = img.shape[0] // 25  # 24
        Line1 = (h, h)  # (24,24)
        Line2 = (h, 2 * h)  # (24,48)
        fontScale = (img.shape[0] / 1000) * Fontscale  # 0.6
        fontColor = (204, 0, 102)  # '#6600cc' # (0, 255, 0)
        BgColor = (153, 255, 255)  # (0, 0, 0)
        thickness = 1
        lineType = 1
        if fPrint_text:
            print(txt)
            print(tbox)
            print()
        cv2.putText(img, txt, Line1, font, fontScale, BgColor, thickness * 3, lineType)
        cv2.putText(img, txt, Line1, font, fontScale, fontColor, thickness, lineType)
        if tbox:
            cv2.putText(
                img, tbox, Line2, font, fontScale, BgColor, thickness * 3, lineType
            )
            cv2.putText(
                img, tbox, Line2, font, fontScale, fontColor, thickness, lineType
            )
        if scolor:
            drawed = {}
            colored = {}
            for k, [mID, scolor] in enumerate(zip(sbox, scolor)):
                drawed[mID] = drawed[mID] + 1 if mID in drawed else 1
                colored[mID] = scolor

            # for k, [mID, scolor] in enumerate(zip(sbox, scolor)):
            for k, (mID, mNumber) in enumerate(drawed.items()):
                scolor = colored[mID]
                line = (h, (k + 3) * h)
                # cv2.putText(img, f"Box:{mID}", line, font, fontScale, (255,255,255), thickness*2+2, lineType)
                cv2.putText(
                    img,
                    f"Box: {mID}: {mNumber}",
                    line,
                    font,
                    fontScale,
                    (255, 255, 255),
                    thickness * 2,
                    lineType,
                )
                cv2.putText(
                    img,
                    f"Box: {mID}: {mNumber}",
                    line,
                    font,
                    fontScale,
                    scolor,
                    thickness,
                    lineType,
                )
        return img

    def Rect0(image, p1, p2, color, thickness):
        cv2.rectangle(image, p1, p2, (255, 255, 255), thickness=thickness * 2)
        cv2.rectangle(image, p1, p2, color, thickness=thickness)
        return

    import cv2

    def Rect(image, p1, p2, color, thickness):
        x1, y1 = p1
        x2, y2 = p2

        # Tính chiều dài và chiều rộng của hình chữ nhật
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        # Tính 10% chiều dài và chiều rộng
        line_len_w = int(0.1 * width)
        line_len_h = int(0.1 * height)

        # Vẽ 4 góc, với 2 hình chữ nhật chồng lên nhau (đường nền và đường màu)

        # Góc trên trái
        cv2.line(
            image,
            (x1, y1),
            (x1 + line_len_w, y1),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # ngang
        cv2.line(
            image,
            (x1, y1),
            (x1, y1 + line_len_h),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # dọc
        cv2.line(
            image, (x1, y1), (x1 + line_len_w, y1), color, thickness=thickness
        )  # ngang
        cv2.line(
            image, (x1, y1), (x1, y1 + line_len_h), color, thickness=thickness
        )  # dọc

        # Góc trên phải
        cv2.line(
            image,
            (x2, y1),
            (x2 - line_len_w, y1),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # ngang
        cv2.line(
            image,
            (x2, y1),
            (x2, y1 + line_len_h),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # dọc
        cv2.line(
            image, (x2, y1), (x2 - line_len_w, y1), color, thickness=thickness
        )  # ngang
        cv2.line(
            image, (x2, y1), (x2, y1 + line_len_h), color, thickness=thickness
        )  # dọc

        # Góc dưới trái
        cv2.line(
            image,
            (x1, y2),
            (x1 + line_len_w, y2),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # ngang
        cv2.line(
            image,
            (x1, y2),
            (x1, y2 - line_len_h),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # dọc
        cv2.line(
            image, (x1, y2), (x1 + line_len_w, y2), color, thickness=thickness
        )  # ngang
        cv2.line(
            image, (x1, y2), (x1, y2 - line_len_h), color, thickness=thickness
        )  # dọc

        # Góc dưới phải
        cv2.line(
            image,
            (x2, y2),
            (x2 - line_len_w, y2),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # ngang
        cv2.line(
            image,
            (x2, y2),
            (x2, y2 - line_len_h),
            (255, 255, 255),
            thickness=thickness * 2,
        )  # dọc
        cv2.line(
            image, (x2, y2), (x2 - line_len_w, y2), color, thickness=thickness
        )  # ngang
        cv2.line(
            image, (x2, y2), (x2, y2 - line_len_h), color, thickness=thickness
        )  # dọc
        cv2.rectangle(image, p1, p2, color, thickness=max(thickness // 3, 1))
        return

    def fnExtract_First_Frame_invideo_to_image(fis_videos):
        fis_video_frames = {}
        for vfn in fis_videos:
            ifn = vfn.replace(".avi", ".jpg")
            ifn = ifn.replace(".mp4", ".jpg")
            vidcap = cv2.VideoCapture(vfn)
            length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            fis_video_frames[ifn] = length
            if not exists(ifn):
                success, image = vidcap.read()
                if success:
                    cv2.imwrite(ifn, image)
            vidcap.release()
        return fis_video_frames

    def draw_label(
        im, ObjName, Confident, x, y, mcolor, hide_labels_type, FONT_SCALE=1.5
    ):
        """

        :param im:
        :param ObjName:
        :param Confident:
        :param x:
        :param y:
        :param hide_labels_type:  =0,1,2,3:  =0 ẩn, =1: hiện số đơn giản, =2: hiện số có nền, =3: hiện số + độ chính xác
        :return:
        """
        """Draw text onto image at location."""
        FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX

        THICKNESS = 1
        # Get text size.
        if hide_labels_type == 0:
            return
        if hide_labels_type in [1, 2]:
            label = f"{ObjName}"
        if hide_labels_type == 3:
            label = "{}:{:.2f}".format(ObjName, Confident)
        THICKNESS = round(FONT_SCALE + 0.5)
        text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
        dim, baseline = text_size[0], text_size[1]
        y = y - baseline - dim[1]
        # Use text size to create a BLACK rectangle.
        if hide_labels_type in [2, 3]:
            cv2.rectangle(
                im, (x, y), (x + dim[0], y + dim[1] + baseline), (0, 0, 0), cv2.FILLED
            )
        # Display text inside the rectangle.
        cv2.putText(
            im,
            label,
            (x, y + dim[1]),
            FONT_FACE,
            FONT_SCALE,
            (200, 200, 200),
            THICKNESS * 2,
            cv2.LINE_AA,
        )  # Background
        cv2.putText(
            im,
            label,
            (x, y + dim[1]),
            FONT_FACE,
            FONT_SCALE,
            mcolor,
            THICKNESS,
            cv2.LINE_AA,
        )
        # print(f"fontScale={FONT_SCALE},thickness={THICKNESS}, t/f={THICKNESS / FONT_SCALE}")

    @staticmethod
    def Read_draw_1image(
        fn,
        pYoLoLabel,
        RandColor,
        color,
        extract_Rois_only=False,
        save_dir=None,
        fswapHorizontal=None,
        LineWidth_k=1,
        ROI_windows=None,
    ):
        global mOverlay
        if exists(pYoLoLabel):
            image = cv2.imread(fn)
            if fswapHorizontal:
                image = swap_left_right(image)
            imshape = image.shape
            # if fPrint_text: print(fn)
            sbox = []
            scolor = []
            w = LineWidth_k * imshape[1] // 500
            h = imshape[0] // 25
            if RandColor:
                for k in range(0, 100):
                    color[k] = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
            with open(pYoLoLabel) as ff:
                yoloBoxes = ff.readlines()
                for line in yoloBoxes:
                    if line.strip() == "":
                        continue
                    mID, [x1, y1, x2, y2] = taLibs.Yolo_to_Box(imshape, line)

                    if fswapHorizontal:
                        xc = imshape[1] // 2
                        x11 = x1
                        x21 = x2
                        if x11 < xc and x21 < xc:
                            x1, x2 = x1 + xc, x2 + xc
                        elif x11 >= xc and x21 >= xc:
                            x1, x2 = x1 - xc, x2 - xc
                        elif x11 < xc < x21:
                            x1 = 0
                            x2 = imshape[1]
                            pass

                        pass
                    if extract_Rois_only:
                        img1 = image[y1:y2, x1:x2]
                        mfn = (
                            f"{save_dir}/{mID}/{random.random() * random.random()}.jpg"
                        )
                        os.makedirs(dirname(mfn), exist_ok=True)
                        cv2.imwrite(mfn, img1)
                    else:
                        sbox.append([mID, color[mID]])
                        # color0 = (0, 255, 255)
                        # cv2.rectangle(image, (x1,y1), (x2,y2), color0, thickness=7)
                        ROI_windows["x1"] = min(ROI_windows["x1"], x1)
                        ROI_windows["y1"] = min(ROI_windows["y1"], y1)
                        ROI_windows["x2"] = max(ROI_windows["x2"], x2)
                        ROI_windows["y2"] = max(ROI_windows["y2"], y2)
                        ROI_windows["HW"] = image.shape[:2]
                        if mOverlay is None:
                            mOverlay = taOverlay(
                                image=image,
                            )
                        mOverlay.update_mask_1box((x1, y1, x2, y2))
                        taLibs.Rect(
                            image,
                            (x1, y1),
                            (x2, y2),
                            color[mID],
                            thickness=max(1, int(w)),
                        )
                        taLibs.draw_label(
                            image,
                            mID,
                            1,
                            x1,
                            y1,
                            color[mID],
                            hide_labels_type=1,
                            FONT_SCALE=myFONT_SCALE,
                        )
            taLibs.Rect(
                image,
                (ROI_windows["x1"], ROI_windows["y1"]),
                (ROI_windows["x2"], ROI_windows["y2"]),
                (128, 128, 128),
                thickness=max(1, int(w // 2)),
            )
            return image, sbox
        return None

    def explore(path: str):
        FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
        # explorer would choke on forward slashes
        path = os.path.normpath(path)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, "/select,", path])


import numpy as np


class taOverlay:
    """
    Class dùng để tính mật độ di chuyển của các đối tượng trong ảnh và vẽ overlay lên ảnh gốc dựa trên kết quả phát hiện.

    Attributes:
    -----------
    mskImg : np.ndarray
        Ảnh mask có kích thước tương tự ảnh gốc, được sử dụng để lưu trữ số lần các đối tượng xuất hiện tại mỗi vị trí (bounding box).

    Methods:
    --------
    __init__(image):
        Khởi tạo class với ảnh gốc và tạo mảng `mskImg` kích thước [H, W, 1] với giá trị khởi tạo là 0.

    update_mask(boxes):
        Cập nhật giá trị trong `mskImg` dựa trên danh sách các bounding box của các đối tượng phát hiện được.

    drawOverlay(image):
        Vẽ overlay lên ảnh gốc dựa trên giá trị của `mskImg`, với giá trị lớn nhất tương ứng với 40% mức độ trong suốt (opacity).

    Usage:
    ------
    1. Khởi tạo class với ảnh gốc:

    ```python
    image = cv2.imread('path_to_image')  # Ảnh gốc
    overlay = taOverlay(image)
    ```

    2. Cập nhật `mskImg` với các bounding box từ đối tượng phát hiện được:

    ```python
    boxes = [(50, 50, 100, 100), (200, 150, 300, 250)]  # Ví dụ bounding box
    overlay.update_mask(boxes)
    ```

    3. Vẽ overlay lên ảnh gốc sau khi đã cập nhật đủ các bounding box:

    ```python
    overlay_image = overlay.drawOverlay(image)
    cv2.imshow('Overlay Image', overlay_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ```
    """

    def __init__(self, image):
        """
        Khởi tạo đối tượng taOverlay.

        Parameters:
        -----------
        image : np.ndarray
            Ảnh gốc dùng để tính toán và vẽ overlay, kích thước [H, W, 3].
        """
        H, W = image.shape[:2]
        self.mskImg = np.zeros((H, W, 1), dtype=np.float32)

    def update_mask_1box(self, box):
        x1, y1, x2, y2 = box  # Box gồm tọa độ góc trên trái và dưới phải
        self.mskImg[y1:y2, x1:x2, 0] += 1.0  # Tăng giá trị tại vùng của bounding box

    def update_mask_boxes(self, boxes):
        """
        Cập nhật giá trị trong mskImg dựa trên danh sách bounding box.

        Parameters:
        -----------
        boxes : list of tuples
            Danh sách các bounding box, mỗi bounding box là tuple (x1, y1, x2, y2) chứa tọa độ của góc trên trái và góc dưới phải.
        """
        for box in boxes:
            self.update_mask_1box(box)

    def drawOverlay(self, image, mask_color=(0, 0, 255), alpha=0.4):
        """
        Vẽ overlay lên ảnh gốc dựa trên giá trị của mskImg.

        Parameters:
        -----------
        image : np.ndarray
            Ảnh gốc để vẽ overlay, kích thước [H, W, 3].
        mask_color : tuple
            Màu của mask (RGB), ví dụ: (0, 0, 255) cho màu đỏ.
        alpha : float
            Độ trong suốt của lớp mask, giá trị từ 0.0 (hoàn toàn trong suốt) đến 1.0 (hoàn toàn mờ đục).

        Returns:
        --------
        np.ndarray
            Ảnh với overlay được vẽ lên trên ảnh gốc, với mức độ trong suốt tỷ lệ với giá trị trong mskImg (giá trị lớn nhất tương ứng với alpha).
        """
        # Chuẩn hóa mskImg sao cho giá trị lớn nhất = 1 (để dễ dàng điều chỉnh alpha)
        max_value = np.max(self.mskImg)
        if max_value > 0:
            normalized_mask = self.mskImg / max_value  # Giá trị lớn nhất sẽ là 1
        else:
            normalized_mask = self.mskImg  # Nếu không có giá trị nào được thay đổi

        # Đảm bảo kích thước của normalized_mask khớp với kích thước của image
        normalized_mask_resized = cv2.resize(
            normalized_mask, (image.shape[1], image.shape[0])
        )

        # Tạo lớp mask màu theo kích thước ảnh gốc
        overlay_mask = np.zeros_like(image, dtype=np.uint8)

        # Áp dụng màu mask tại các vị trí có giá trị trong normalized_mask_resized
        for i in range(3):  # Duyệt qua các kênh màu R, G, B
            overlay_mask[:, :, i] = (
                normalized_mask_resized * mask_color[i] * 255
            ).astype(np.uint8)

        # Áp dụng overlay với độ trong suốt alpha
        overlay = cv2.addWeighted(image, 1, overlay_mask, alpha, 0)

        return overlay

    def drawOverlay_byColor(self, image, alpha=0.4):
        """
        Vẽ overlay gradient lên ảnh gốc dựa trên giá trị của mskImg.

        Parameters:
        -----------
        image : np.ndarray
            Ảnh gốc để vẽ overlay, kích thước [H, W, 3].
        alpha : float
            Độ trong suốt của lớp mask, giá trị từ 0.0 (hoàn toàn trong suốt) đến 1.0 (hoàn toàn mờ đục).

        Returns:
        --------
        np.ndarray
            Ảnh với overlay gradient được vẽ lên trên ảnh gốc, với màu dựa trên mức độ xuất hiện đối tượng.
        """
        # Chuẩn hóa mskImg sao cho giá trị lớn nhất = 1 (để dễ dàng điều chỉnh alpha)
        max_value = np.max(self.mskImg)
        if max_value > 0:
            normalized_mask = self.mskImg / max_value  # Giá trị lớn nhất sẽ là 1
        else:
            normalized_mask = self.mskImg  # Nếu không có giá trị nào được thay đổi

        # Đảm bảo kích thước của normalized_mask khớp với kích thước của image
        normalized_mask_resized = cv2.resize(
            normalized_mask, (image.shape[1], image.shape[0])
        )

        # Tạo lớp overlay mask với màu gradient dựa trên giá trị của normalized_mask_resized
        overlay_mask = np.zeros_like(image, dtype=np.float32)

        # Chuyển giá trị từ mask thành giá trị màu gradient (blue -> green -> red)
        for y in range(normalized_mask_resized.shape[0]):
            for x in range(normalized_mask_resized.shape[1]):
                value = normalized_mask_resized[y, x]  # Truy cập phần tử 2 chiều

                if value > 0:
                    # Tạo màu gradient từ blue (ít di chuyển) -> green -> red (nhiều di chuyển)
                    blue = max(
                        0, 255 - int(value * 2 * 255)
                    )  # Màu giảm dần khi value tăng
                    green = max(
                        0, int(255 - abs(value * 2 - 1) * 255)
                    )  # Màu cao nhất ở giữa
                    red = min(255, int(value * 2 * 255))  # Màu tăng dần khi value tăng

                    overlay_mask[y, x] = (blue, green, red)

        # Chuẩn hóa overlay_mask về dạng uint8
        overlay_mask = (overlay_mask).astype(np.uint8)

        # Áp dụng overlay với độ trong suốt alpha
        overlay = cv2.addWeighted(image, 1, overlay_mask, alpha, 0)

        return overlay

    def drawOverlay_byColor2(self, image, alpha=0.4):
        """
        Vẽ overlay gradient lên ảnh gốc dựa trên giá trị của mskImg.

        Parameters:
        -----------
        image : np.ndarray
            Ảnh gốc để vẽ overlay, kích thước [H, W, 3].
        alpha : float
            Độ trong suốt của lớp mask, giá trị từ 0.0 (hoàn toàn trong suốt) đến 1.0 (hoàn toàn mờ đục).

        Returns:
        --------
        np.ndarray
            Ảnh với overlay gradient được vẽ lên trên ảnh gốc, với màu dựa trên mức độ xuất hiện đối tượng.
        """
        # Chuẩn hóa mskImg sao cho giá trị lớn nhất = 1 (để dễ dàng điều chỉnh alpha)
        max_value = np.max(self.mskImg)
        if max_value > 0:
            normalized_mask = self.mskImg / max_value  # Giá trị lớn nhất sẽ là 1
        else:
            normalized_mask = self.mskImg  # Nếu không có giá trị nào được thay đổi

        # Đảm bảo kích thước của normalized_mask khớp với kích thước của image
        normalized_mask_resized = cv2.resize(
            normalized_mask, (image.shape[1], image.shape[0])
        )

        # Tạo lớp overlay mask với gradient bằng cách nhân với 0xFFFFFF (tức là giá trị màu RGB)
        gradient_mask = (normalized_mask_resized * 0xFFFFFF).astype(np.uint32)

        # Chuyển gradient_mask thành các kênh màu R, G, B
        overlay_mask = np.zeros_like(image, dtype=np.uint8)
        overlay_mask[:, :, 0] = (gradient_mask & 0xFF).astype(np.uint8)  # Blue
        overlay_mask[:, :, 1] = ((gradient_mask >> 8) & 0xFF).astype(np.uint8)  # Green
        overlay_mask[:, :, 2] = ((gradient_mask >> 16) & 0xFF).astype(np.uint8)  # Red

        # Áp dụng overlay với độ trong suốt alpha
        overlay = cv2.addWeighted(image, 1, overlay_mask, alpha, 0)

        return overlay


mOverlay = None
MouseCnt = 0
cnt = 0


def tt1():
    return datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")


def tt2():
    return str(time.time())


myFONT_SCALE = 1


def CheckYolo_Data(
    pImgdir,
    pLabel,
    pDirErrorTxt,
    fDraw_ROI_2_Imgs=False,
    RandColor=True,
    CollectLabel=-1,
    cfg={},
):
    r"""
     p=r"E:\DATA-SupperCAP\Step1_2---SUPERCAP_DATA\images\1.jpg"
     CheckYolo_Data(p)

    :param pImgdir: path to 1 image in the images' folder
    :param fDraw_ROI_2_Imgs: =true ==> Tạo 1 thư mục thêm đuôi output vào, khoanh toàn bộ data, rồi lưu kết quả vào đó. E:\DATA-SupperCAP\STEP2-SUPERCAP_output\...
    :return: Nếu  fDraw_ROI_2_Imgs=true: xem thư mục ảnh, nếu =false: xem ảnh qua OpenCV imshow
    """
    global cnt, Fontscale, fPrint_text, myFONT_SCALE
    pImgdir = pImgdir.lower().replace("\\", "/")
    if not pLabel:
        pLabel = pImgdir
    # Không hiển thị ra CV2 mà lưu ra file
    if isfile(pImgdir):
        pImgdir = dirname(pImgdir)
    if isfile(pLabel):
        pLabel = dirname(pLabel)
    pLabel = pLabel.replace("\\", "/")
    save_dir = pImgdir + "_Output"
    CollectLabel = int(CollectLabel)
    if int(CollectLabel) > -1:
        print("Saved to: ", save_dir)
        os.makedirs(save_dir, exist_ok=True)

    fis_videos = taLibs.getFiles(sPath=pImgdir, ext=(".avi", ".mp4"))
    nVideo = len(fis_videos)
    print("Processing:", nVideo, " Video files")
    fis_video_frames = taLibs.fnExtract_First_Frame_invideo_to_image(fis_videos)
    fis = taLibs.getFiles(sPath=pImgdir)
    # fis=sorted(fis, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))

    n = len(fis)
    if not pDirErrorTxt:
        pDirErrorTxt = pImgdir + "__Errors"
    print("Dir Error: No Txt=", pDirErrorTxt)
    print("Processing:", n, " Image files")
    noLabel = []
    for fn in fis:  # Anh
        fnLabel = fn.replace(".jpg", ".txt")
        fnLabel = fnLabel.replace(pImgdir, pLabel)
        if not exists(fnLabel):
            noLabel.append(fn)

            dstFN = fn.replace(pImgdir, pDirErrorTxt)
            os.makedirs(dirname(dstFN), exist_ok=True)
            shutil.move(fn, dstFN)

    for fn in fis_videos:
        fnLabel = fn.replace(".avi", ".txt")
        if not exists(fnLabel):
            noLabel.append(fn)
            dstFN = fn.replace(pImgdir, pDirErrorTxt)
            os.makedirs(dirname(dstFN), exist_ok=True)
            shutil.move(fn, dirname(dstFN))

    pp(noLabel)
    print("Image without labels:", len(noLabel))
    if len(noLabel) > 0:
        print("After move files:")
        fis_videos = taLibs.getFiles(sPath=pImgdir, ext=(".avi", ".mp4"))
        nVideo = len(fis_videos)
        print("Processing:", nVideo, " Video files")
        taLibs.fnExtract_First_Frame_invideo_to_image(fis_videos)
        fis = taLibs.getFiles(sPath=pImgdir)

    # ------- Label Process -----------------------------------------------
    if "All Label Processing":
        lbl_fis = taLibs.getFiles(sPath=pLabel, ext=(".txt",))
        # if CollectLabel is not None:
        CollectLabels = []
        sbox = OrderedDict()
        sbox_vids = OrderedDict()
        for pYoLoLabel in lbl_fis:
            if pYoLoLabel.endswith("classes.txt"):
                continue
            AddNums = 0
            if pYoLoLabel.replace(".txt", ".jpg") in fis_video_frames:
                AddNums = fis_video_frames[pYoLoLabel.replace(".txt", ".jpg")]
            pimg = pYoLoLabel.replace(".txt", ".jpg")
            pimg = pimg.replace(pLabel, pImgdir)
            if not exists(pimg):
                continue
            with open(pYoLoLabel) as ff:
                yoloBoxes = ff.readlines()
                for line in yoloBoxes:
                    if line.strip() == "":
                        continue
                    mID, [x1, y1, x2, y2] = taLibs.Yolo_to_Box(
                        imShape=(600, 800, 3), sYoloBox=line
                    )
                    if mID in sbox:
                        sbox[mID] += 1
                        sbox_vids[mID] += AddNums
                    else:
                        sbox[mID] = 1
                        sbox_vids[mID] = AddNums
                    if CollectLabel > -1:
                        if mID == CollectLabel:
                            if pYoLoLabel not in CollectLabels:
                                CollectLabels.append(pYoLoLabel)
        # Nếu move nhãn ra thư mục ngoài: ---------------------------------------------------------
        print("CollectLabels=", len(CollectLabels))
        if CollectLabel > -1:
            save_dirLabel = save_dir + f"_Label{CollectLabel}"
            os.makedirs(save_dirLabel, exist_ok=True)
            pLabel = pLabel.replace("\\", "/")
            pImgdir = pImgdir.replace("\\", "/")
            pLabel = pLabel.lower()
            pImgdir = pImgdir.lower()
            for fn in CollectLabels:
                des = join(save_dirLabel, basename(fn))
                if not exists(des):
                    shutil.move(fn, save_dirLabel)
                    fn = fn.lower().replace("\\", "/")
                    shutil.move(
                        fn.replace(pLabel, pImgdir).replace(".txt", ".jpg"),
                        save_dirLabel,
                    )
            pClassLabel = join(save_dirLabel, "classes.txt")
            if not exists(pClassLabel):
                with open(pClassLabel, "w") as ff:
                    for k in range(100):
                        ff.write(f"{k}\n")
            taLibs.fnExplore(save_dirLabel)
            CollectLabel = -1
        # tbox = sbox
        tbox = dict(sorted(sbox.items(), key=lambda key_value: key_value[0]))
        tbox_vids = dict(sorted(sbox_vids.items(), key=lambda key_value: key_value[0]))

        print("All box names:", "-" * 30)
        print(tbox)
        print("ROIs in videos:")
        print(tbox_vids)
        print("All ROIs:")
        allRois = {}
        for key, val in tbox_vids.items():
            allRois[key] = val + tbox[key]
        print(allRois)
        print("-" * 48)
    #     tbox, tbox_vids, allRois
    # ---------------------------------------------------------------------

    color = {}
    for k in range(0, 100):
        color[k] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
    cnt = 0
    keys = []
    MouseCnt = 0

    # ------------------------------------------------
    def MouseEvent(action, x, y, flags, *userdata):
        global top_left_corner, bottom_right_corner, MouseCnt, cnt
        # print(action, x, y, flags, *userdata)
        if action == cv2.EVENT_LBUTTONDOWN:
            top_left_corner = [(x, y)]
            # print(MouseCnt, 'Left Mouse Down')
            MouseCnt += 1
        elif action == cv2.EVENT_LBUTTONUP:
            bottom_right_corner = [(x, y)]
            # print(MouseCnt, 'Left Mouse Up')
            MouseCnt += 1
            # Draw the rectangle
            # cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), 2, 8)
            # cv2.imshow("Window", image)
        elif action == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                # print(MouseCnt, 'Scroll Up')
                cnt -= 1
            if flags < 0:
                # print(MouseCnt, 'Scroll Down')
                cnt += 1
            MouseCnt += 1
            # print('Mouse event cnt=', cnt)

    window_name = pImgdir
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, MouseEvent)
    fswapHorizontal = cfg["swapHorizontal"]
    # ------------------------------------------------
    print(sHelp)
    imHeight = 0
    LineWidth_k = 1.0
    last_pressed_key = 0
    ROI_windows = {"x1": 10000, "y1": 10000, "x2": -1, "y2": -1, "HW": [600, 800]}
    # ----------------- Overlay:

    # --------------------------
    while (cnt > -1) and (len(fis) > 0):
        # cnt=(cnt + len(fis)) % len(fis)
        fn = ""
        try:
            fn = fis[cnt]
        except:
            print(f"error: {cnt}/{len(fis)}")

        pYoLoLabel = (
            fn.replace(pImgdir, pLabel).replace(".jpg", ".txt").replace('"', "")
        )
        try:

            image, sbox = taLibs.Read_draw_1image(
                fn=fn,
                pYoLoLabel=pYoLoLabel,
                RandColor=RandColor,
                color=color,
                extract_Rois_only=False,
                save_dir=None,
                fswapHorizontal=fswapHorizontal,
                LineWidth_k=LineWidth_k,
                ROI_windows=ROI_windows,
            )
        except Exception as e:
            print("Error: ", e)
            pass
        try:
            sbox.sort()
        except Exception as e:
            print("Error:", e)
        try:
            scolor = [cl for id, cl in sbox]
            sbox = [id for id, cl in sbox]
            dbox = taLibs.fnList_2Count(sbox)
            txt = f'{cnt}/{n} - {str(dbox)} - {fn.replace(pImgdir, "")}'.replace(": ", ":")
            showAll = 0 <= cnt < 1
            image = taLibs.put_text_top(
                image, [sbox, txt, tbox, tbox_vids, allRois], scolor, showAll
            )
        except Exception as e:
            print(fn)
            print('sbox:',e)
            continue
        if 0 <= cnt < 1:
            image = AiLibs.Plot2Dict_onImage(
                image,
                dict1=tbox,
                dict2=tbox_vids,
                output_imsize=(1024 + round(1.46 * imHeight), 700 + imHeight),
                label1="Imgs",
                label2="Vids",
                xLabel="Quantity",
                yLable="Rois",
                myTitle="All ROIs",
                cnt=cnt,
                pDir="",  # pImgdir Save His image if giving dir
            )
        else:
            image = taLibs.image_resize(image, height=600 + imHeight)
            if cfg["show_full_txt_path_on_image"]:
                h, w, c = image.shape
                image = cv2.putText(
                    image,
                    text=pYoLoLabel,
                    org=(10, h - 10),
                    fontFace=3,
                    fontScale=0.6,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=2,
                )
                image = cv2.putText(
                    image,
                    text=pYoLoLabel,
                    org=(10, h - 10),
                    fontFace=3,
                    fontScale=0.6,
                    color=(255, 0, 0),
                    thickness=1,
                    lineType=2,
                )
        if fDraw_ROI_2_Imgs:
            cv2.imwrite(join(save_dir, basename(fn)), image)
            cnt += 1
            if cnt >= n:
                break
        else:
            # cv2.imshow(basename(fn), image)

            cv2.imshow(window_name, image)
            # key=cv2.waitKey(0)
            # print('Main loop cnt=', cnt)
            # ------------------------------------------------------
            cnt0 = cnt
            fWaitEvent = True
            while fWaitEvent:
                key = cv2.waitKeyEx(1)
                if key > 0 or cnt0 != cnt:
                    fWaitEvent = False
                    if key != last_pressed_key:
                        print_key_name(key)
                        last_pressed_key = key
            # ------------------------------------------------------
            # print(key)
            if key == 27:
                break
            if key in [7405568]:  # F2
                ymlPath = "IVIS_data/config.yml"
                rootDir = os.path.dirname(__file__)
                ymlPath = join(rootDir, ymlPath)
                os.startfile(ymlPath)
                pass
            if key in [7536640]:  # F4
                print("-" * 60)
                print("ROI_windows xyxy:", ROI_windows)
                imH, imW = ROI_windows["HW"]
                yolostring_Windows = ntanh.xyxy_to_yolo_str(
                    obj_class=0,
                    x1=ROI_windows["x1"],
                    y1=ROI_windows["y1"],
                    x2=ROI_windows["x2"],
                    y2=ROI_windows["y2"],
                    imH=imH,
                    imW=imW,
                )
                print("ROI_windows Yolo:", yolostring_Windows)

                save_dir = pImgdir + "_Output"
                os.makedirs(save_dir, exist_ok=True)
                fn = join(save_dir, "Cover_Box.txt")
                with open(fn, "w") as ff:
                    ff.write(yolostring_Windows)
                    ff.write(f"\nROI_windows xyxy: {ROI_windows}")
                print("Cover_Box saved to: ", fn)
                print("-" * 60)

            if key in [7340032]:  # F1
                save_dir = f"{pImgdir}_ROI_labels"
                print("Start extract ROIs...")
                for fn in fis:
                    pYoLoLabel = (
                        fn.replace(pImgdir, pLabel)
                        .replace(".jpg", ".txt")
                        .replace('"', "")
                    )

                    taLibs.Read_draw_1image(
                        fn=fn,
                        pYoLoLabel=pYoLoLabel,
                        RandColor=RandColor,
                        color=color,
                        extract_Rois_only=True,
                        save_dir=save_dir,
                        fswapHorizontal=fswapHorizontal,
                        LineWidth_k=LineWidth_k,
                        ROI_windows=ROI_windows,
                    )
                print("Extract finished!")
                print("Save Location:", save_dir)
                taLibs.explore(save_dir)

            if key in [7995392]:  # F11
                myFONT_SCALE -= 0.2
                if myFONT_SCALE < 0.4:
                    myFONT_SCALE = 0.4
            if key in [8060928]:  # F12
                myFONT_SCALE += 0.2

            if key in [ord("*")]:
                print(fn)
            if key in [7798784]:  # f8
                LineWidth_k = LineWidth_k * 1.1
            if key in [7733248]:  # F7
                LineWidth_k = LineWidth_k * 0.9
            if key in [ord("-")]:
                Fontscale = Fontscale * 0.9
            if key in [ord("=")]:  # lui, xuong
                Fontscale = 10 * Fontscale / 9
            if key in [7864320]:  # F9
                imHeight -= 10
                print("Windows size (HxW):", image.shape[:2])

            if key in [7929856]:  # F10
                imHeight += 10
                print("Windows size (HxW):", image.shape[:2])

            if key in [2424832, 2621440]:  # lui, xuong
                cnt = (cnt - 1 + n) % n

            if key in [7471104]:  # F3
                overlay_image = mOverlay.drawOverlay_byColor(image, alpha=1)
                # overlay_image = mOverlay.drawOverlay_byColor( image,   alpha=1 )
                save_dir = pImgdir + "_Output"
                print("Saved to: ", save_dir)
                os.makedirs(save_dir, exist_ok=True)
                cv2.imwrite(join(save_dir, "ROI_di_chuyen_byColor.png"), overlay_image)
                cv2.imshow("ROI_di_chuyen_byColor", overlay_image)

                cv2.waitKey(1)
            if key in [7602176]:  # F5
                overlay_image = mOverlay.drawOverlay(
                    image, mask_color=(0, 10, 0), alpha=1
                )
                # overlay_image = mOverlay.drawOverlay_byColor( image,   alpha=1 )
                save_dir = pImgdir + "_Output"
                print("Saved to: ", save_dir)
                os.makedirs(save_dir, exist_ok=True)
                cv2.imwrite(join(save_dir, "ROI_di_chuyen.png"), overlay_image)
                cv2.imshow("ROI_di_chuyen", overlay_image)

                cv2.waitKey(1)

            if key in [7667712]:  # F6
                # overlay_image = mOverlay.drawOverlay( image, mask_color=(0, 255, 0), alpha=1 )
                overlay_image = mOverlay.drawOverlay_byColor2(image, alpha=1)
                save_dir = pImgdir + "_Output"
                print("Saved to: ", save_dir)
                os.makedirs(save_dir, exist_ok=True)
                cv2.imwrite(join(save_dir, "ROI_di_chuyen_byColor2.png"), overlay_image)
                cv2.imshow("ROI_di_chuyen_byColor2", overlay_image)
                cv2.waitKey(1)

            if (
                key
                not in [
                    -1,
                    ord("*"),
                    ord("-"),
                    ord("="),
                    13,
                    2424832,  # Xuống
                    2621440,  # Lùi
                    7798784,  # F8 Line +
                    7733248,  # F7: Line -
                    7995392,  # F11
                    8060928,  # F12
                    7340032,  # F1 : Trích xuất các nhãn ra thư mục riêng
                    7864320,  # F9 : zoom out
                    7929856,  # F10: zoom in
                ]
            ) and not (ord("0") <= key <= ord("9")):
                cnt = (cnt + 1) % n
            if ord("0") <= key <= ord("9"):
                keys.append(key)
                print(key, keys)
            if key == 96:  # Dấu ` (~): chỉ in đường dẫn, không thay đổi vị trí ảnh
                print(fn)
                # cnt = (cnt - 1 + n) % n

            if key == 13:
                print(keys)
                kq = 0
                for k in keys:
                    kq = kq * 10 + k - 48
                kq = (kq + n) % n
                cnt = kq
                keys = []
                print(f"{cnt}/{n}")
            # ------------------------------------------------------
            # cnt = (cnt + n) % n
        if cnt % 1000 == 0:
            print(f"{cnt}/{n}")

    cv2.destroyAllWindows()
    if fDraw_ROI_2_Imgs:
        taLibs.fnExplore(save_dir)
        print("Saved to: ", save_dir)


def Merge_Yolo_Data(Src_images_labels, Des_images_labels, prefix="fold2_"):
    lblSrc = join(Src_images_labels.lower(), "labels").replace("\\", "/")
    imgSrc = join(Src_images_labels.lower(), "images").replace("\\", "/")

    lblDes = join(Des_images_labels.lower(), "labels").replace("\\", "/")
    imgDes = join(Des_images_labels.lower(), "images").replace("\\", "/")

    fislbl = taLibs.getFiles(lblSrc, ext=(".txt",))
    fisimg = taLibs.getFiles(imgSrc)

    def taCopy(fis):
        for fn in fis:
            fnDirn = dirname(fn).replace(Src_images_labels, Des_images_labels)
            fnBase = basename(fn)
            fnscr = fn
            fn_des = join(fnDirn, prefix + fnBase)
            shutil.move(fnscr, fn_des)
            print(fnscr, " => ", fn_des)

    taCopy(fislbl)
    taCopy(fisimg)


#
# Src_images_labels=r'E:\DATA-SupperCAP\STEP2-SUPERCAP'
# Des_images_labels=r'E:\DATA-SupperCAP\STEP2-SUPERCAP'
# Merge_Yolo_Data(Src_images_labels, Des_images_labels, prefix='fold3_')

if __name__ == "__main__":
    runApp(RunningClick=True)
