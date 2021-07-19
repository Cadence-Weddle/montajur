import glob
from math import floor, ceil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import subprocess
import os
import cv2


image_formats = ["jpg", "png", 'jpeg', 'tiff']

def get_images(di, formats=image_formats):
    o = []
    for f in formats: 
        if (di[-1] == '/' or di[-1] == '\\'):
            filenames = glob.glob(di + "*." + f)
        else: 
            filenames = glob.glob(di + "/*." + f)
        o = o + filenames
    o = sorted(o)
    return o

def pad(img, h_b, h_t, w_l, w_r, color=(0,0,0)):
    o_shape = (img.shape[0] + h_t + h_b, img.shape[1] + w_l + w_r, img.shape[2])
    background = np.full(o_shape, color, dtype=np.uint8)
    h, w, c = img.shape
    background[h_b:h+h_b, w_l:w+w_l] = img
    return background
    
def fit_image(image, m_height, m_width, a_mode='center', crop=True, color=(0,0,0)):
    dh = m_height - image.shape[0]
    dw = m_width - image.shape[1]
    outimage = image
    if a_mode == 'center' and not crop:
        outimage = pad(image, floor(dh / 2), ceil(dh/2), floor(dw / 2), ceil(dw / 2), color)
    return outimage
    
def process_images(images, m_height=-1, m_width=-1):
    p_dim = not(m_height <= 0 or m_width <= 0) 
    for image in tqdm(images):
        img = cv2.imread(image)
        h, w, l = img.shape
        if not p_dim:
            if h > m_height: 
                    m_height = h
            if w > m_width:
                    m_width = w
    print("Ranthrough all images, max height is :" + str(m_height) + "" + " max width is " + str(m_width))
    return m_height, m_width

def clean_ext(images):
    for image in images:
        ext = image.split('.')[-1]
        if ext != ext.lower():
            im = cv2.imread(image)
            o = image[:-len(ext)] + ext.lower()
            os.remove(image)
            cv2.imwrite(o, im)
outfile = 'output.mp4'
res = ('1920', '1080')

def stich(outfile, res=('1920', '1080'), overwrite=False):
    