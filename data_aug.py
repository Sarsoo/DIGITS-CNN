#!/usr/bin/env python3
"""Generate extra training data using rotations and flips

Read a DIGITS train.txt and use OpenCV to generate extra data for training.
FLIP an image and/or apply various rotations from ROTATE_DEGREES

Optionally rotate both clockwise and counter-clockwise by given degrees and
apply rotations to flipped images 
"""

import os
import pathlib
import cv2 as cv
import numpy as np

TRAIN_FILE = input('enter train file path: ') # path to train.txt
OUTPUT_PATH = input('enter o/p path: ') # output folder for altered images

# TRAIN_FILE = 'cars/default-split/train.txt' # path to train.txt
# OUTPUT_PATH = '/scratch/Teaching/ap00824/cars/train' # output folder for altered images

DRY_RUN = False # dont output files, just a new train.txt

FLIP = True # just flip image left to right
ROTATE = False # enable rotating image by below options
ROTATE_BOTH = False # do clockwise and counter-clockwise
ROTATE_DEGREES = [15] # different rotations to apply
FLIP_ROTATED = False # do rotations on both flipped images

INCLUDE_ORIG = True # include original train.txt entry in ouput
# if true the output extra_training.txt can be used as a whole train.txt
# otherwise must be merged with original

###################
#    EXP FACTOR
###################

exp_factor = int(ROTATE) * len(ROTATE_DEGREES)
exp_factor *= int(ROTATE_BOTH) + 1 # either 1 or 2 scale factor
exp_factor *= int(FLIP_ROTATED) + 1 # either 1 or 2 scale factor
exp_factor += int(FLIP) + 1 # flip is one extra image, + 1 for original file

print("Expansion Factor of {}".format(exp_factor))

train_file = pathlib.Path(TRAIN_FILE)
output_path = pathlib.Path(OUTPUT_PATH).resolve()

# read input train.txt
with open(TRAIN_FILE, 'r') as tf:
    train_txt_lines = tf.readlines()

# parse to dict objects
train_split = list()
for line in train_txt_lines:
    space_split = line.split(' ')
    train_split.append({
        # "raw_path": space_split[0],
        "image": pathlib.Path(space_split[0]),
        "class": space_split[1].replace('\n', '')
    })

print('New Training Set: {} images'.format(len(train_split) * exp_factor))
print('Generating {} images...'.format(len(train_split) * (exp_factor - 1)))

##################
#     PROCESS
##################

# rotate_bound from imutils
# https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv.warpAffine(image, M, (nW, nH))

# get a modified image name
def insert_path_part(obj, part):
    return obj["image"].stem + '-' + part + obj["image"].suffix

def get_train_entry(obj, path):
    return "{} {}\n".format(str(path), obj['class'])

new_lines = list()
for train in train_split:
    if not DRY_RUN:
        img = cv.imread(str(train["image"]))

    if INCLUDE_ORIG:
        new_lines.append(get_train_entry(train, train["image"]))

    if FLIP:
        op_path = output_path / insert_path_part(train, 'flip')
        if not DRY_RUN:
            cv.imwrite(str(op_path), cv.flip(img, 1))
        new_lines.append(get_train_entry(train, op_path))

    if ROTATE:
        for deg in ROTATE_DEGREES:
            op_path = output_path / insert_path_part(train, 'rot-{}'.format(deg))
            if not DRY_RUN:
                cv.imwrite(str(op_path), rotate_bound(img, deg))
            new_lines.append(get_train_entry(train, op_path))

            if FLIP_ROTATED:
                op_path = output_path / insert_path_part(train, 'flip-rot-{}'.format(deg))
                if not DRY_RUN:
                    cv.imwrite(str(op_path), cv.flip(rotate_bound(img, deg), 1))
                new_lines.append(get_train_entry(train, op_path))

            if ROTATE_BOTH:
                op_path = output_path / insert_path_part(train, 'rot-min-{}'.format(deg))
                if not DRY_RUN:
                    cv.imwrite(str(op_path), rotate_bound(img, -deg))
                new_lines.append(get_train_entry(train, op_path))

                if FLIP_ROTATED:
                    op_path = output_path / insert_path_part(train, 'flip-rot-min-{}'.format(deg))
                    if not DRY_RUN:
                        cv.imwrite(str(op_path), cv.flip(rotate_bound(img, -deg), 1))
                    new_lines.append(get_train_entry(train, op_path))

with open('extra_training.txt', 'w') as op_file:
    op_file.writelines(new_lines)
