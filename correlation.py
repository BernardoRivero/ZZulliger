import numpy as np
import cv2
import math

def media(x):
    rows = x.shape[0]
    columns = x.shape[1]
    sum = 0
    for row in x:
      for elem in row:
        sum += elem
    return float(sum) / (rows*columns)

def standard_deviation(x):
    rows = x.shape[0]
    columns = x.shape[1]
    assert rows*columns > 0
    med_x = media(x)
    sum = 0
    for i in range(0,rows):
      for j in range(0,columns):
        sum += math.pow(x[i][j] - med_x, 2)
    return math.sqrt((sum/(rows*columns)))

def covariance(x, y):
    rows_x = x.shape[0]
    columns_x = x.shape[1]
    assert rows_x*columns_x > 0
    med_x = media(x)
    med_y = media(y)
    sum = 0
    for i in range(0,rows_x):
      for j in range(0,columns_x):
        sum += ((x[i][j] - med_x)*(y[i][j] - med_y))
    return (sum/(rows_x*columns_x))

def calculate_correlation_coefficient(imageA, imageB):
    # Images must be the same size
    if imageA.size > imageB.size:
        width = int(imageB.shape[1])
        height = int(imageB.shape[0])
        dim = (width, height)
        imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)
    else: 
        width = int(imageA.shape[1])
        height = int(imageA.shape[0])
        dim = (width, height)
        imageB = cv2.resize(imageB, dim, interpolation = cv2.INTER_AREA)

    # Extract red channel
    red_channel_im1 = imageA[:,:,2]
    red_channel_im2 = imageB[:,:,2]

    x = np.asarray(red_channel_im1)
    y = np.asarray(red_channel_im2)

    covariance_xy = covariance(x,y)
    deviation_x = standard_deviation(x)
    deviation_y = standard_deviation(y)
    return covariance_xy / (deviation_x * deviation_y)