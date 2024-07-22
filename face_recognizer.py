#!/usr/bin/env python3

#
# face_recognizer.py
#
# Date    : 2024-05-26
# Author  : Hirotoshi FUJIBE
# History :
#
# Copyright (c) 2024 Hirotoshi FUJIBE
#

# Import Libraries
import cv2
import tkinter as tk
from tkinter import Label, messagebox
from tkinterdnd2 import *
from PIL import Image, ImageTk, ImageOps

# Constants
XML_FILE_PATH = '.\\xml\\haarcascade_frontalface_default.xml'
WINDOW_RATIO = 60
WINDOW_WIDTH = 16 * WINDOW_RATIO
WINDOW_HEIGHT = 10 * WINDOW_RATIO
LINE_GAP = 70


# Recognize Face
def recognize_face(file_name: str):
    try:
        cascade = cv2.CascadeClassifier(XML_FILE_PATH)
        image_org = cv2.imread(file_name)
        image_gray = cv2.cvtColor(image_org, cv2.COLOR_BGR2GRAY)
        face_list = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        for (x, y, w, h) in face_list:
            red = (0, 0, 255)
            cv2.rectangle(image_org, (x, y), (x + w, y + h), red, thickness=5)
        rgb_image = cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB)
        return rgb_image
    except Exception as ex:
        raise Exception(ex)


# Image Data
global disp_image


# Main
def main() -> None:

    def drop_file(event):

        global disp_image

        canvas.delete('all')
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        try:
            rgb_image = recognize_face(event.data)
            pil_image = Image.fromarray(rgb_image)
            align_image = ImageOps.pad(pil_image, (canvas_width, canvas_height), color='gray')
            disp_image = ImageTk.PhotoImage(image=align_image)
            canvas.create_image(0, 0, image=disp_image, anchor=tk.NW)
        except Exception as ex:  # noqa
            canvas.create_line(0 + LINE_GAP, 0 + LINE_GAP,
                               canvas_width - LINE_GAP, canvas_height - LINE_GAP, fill='red')
            canvas.create_line(canvas_width - LINE_GAP, 0 + LINE_GAP,
                               0 + LINE_GAP, canvas_height - LINE_GAP, fill='red')
            canvas.create_text(canvas_width / 2, canvas_height / 2, text='Read file error has occurred.')
            canvas.create_text(canvas_width / 2, canvas_height / 2 + 20, text='( %s )' % ex)
            messagebox.showerror('Error', 'Read file error has occurred.\n( %s )' % ex)
        return event.action

    root = TkinterDnD.Tk()
    root.title('Face Recognizer')
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    label = Label(root, text='Please drag and drop image file on below.')
    label.pack()

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop_file)
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(expand=True, fill=tk.BOTH)

    root.mainloop()


# Goto Main
if __name__ == '__main__':
    main()
