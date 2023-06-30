# importing required libraries
import cv2
import numpy as np
from PIL import Image
from env import *

def closest_value(input_value):
  arr = np.array([0, 128, 192, 255])
  i = (np.abs(arr - input_value)).argmin()
  return arr[i]

def closest_rgb(r,g,b):
   r = closest_value(r)
   g = closest_value(g)
   b = closest_value(b)

   return (r,g,b)

def capture_color_sequence():
    color_seq = []
    queue = []

    # taking the input from webcam
    # vid = cv2.VideoCapture(0)
    vid = cv2.VideoCapture('shortVideo.mp4')

    milliseconds = 0
    while vid.isOpened():

        # capturing the current frame
        valid, frame = vid.read()
        
        if not valid:
           break

        # displaying the current frame
        cv2.imshow("frame", frame)

        # setting values for base colors
        b = frame[:, :, :1]
        g = frame[:, :, 1:2]
        r = frame[:, :, 2:]

        # computing the mean
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)

        # finding closest rgb
        rgb = closest_rgb(r_mean, g_mean, b_mean)
        color = dec_to_color.get(rgb, 404)

        # print((r_mean,g_mean,b_mean), rgb, color)

        color_seq.append(color)
        queue.append(color)

        if len(queue) == 4:
           print(decode_sequence(queue))
           queue.clear()

        # forward by milliseconds
        milliseconds += MIN_COLOR_DURATION
        vid.set(cv2.CAP_PROP_POS_MSEC, milliseconds)

    return color_seq

def decode_sequence(seq):
   return valid_pattern.get(tuple(seq), 'Invalid')

print(capture_color_sequence())