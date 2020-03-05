#!/usr/bin/env python
import numpy as np
import math
import sys
import cv2
import subprocess
import random
import sys
import os


def detect_lines(frame):
    # print(frame[0])
    # 先沿着图边缘画一个矩形
    cv2.line(frame, (0, 1000000), (0, -1000000), (75, 75, 75), 10)
    cv2.line(frame, (-1000000, len(frame)),
             (1000000, len(frame)), (75, 75, 75), 10)
    cv2.line(frame, (1000000, 0), (-1000000, 0), (75, 75, 75), 10)
    cv2.line(frame, (len(frame[0]), 1000000),
             (len(frame[0]), -1000000), (75, 75, 75), 10)
    # cv2.imshow('result.jpg', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    high_thresh, thresh_im = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # print(gray,high_thresh, thresh_im)
    lowThresh = 0.2 * high_thresh
    # cv2.imwrite(prefix + str(count) + "thresh.jpg", thresh_im)
    edges = cv2.Canny(gray, lowThresh, high_thresh)
    edges = cv2.GaussianBlur(edges, (7, 7), 2)
    # cv2.imwrite(prefix + str(count) + "edges.jpg", edges)

    lines = cv2.HoughLinesP(edges, 1, math.pi / 360, 30, None, 30, 1)
    length_thresh = (frame.shape[0] *
                     frame.shape[0] + frame.shape[1] * frame.shape[1]) * 0.2
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = get_length((x1, y1), (x2, y2))
        if length > length_thresh:
            # print(length)
            slope = get_slope((x1, y1), (x2, y2))
            if(slope == None):
                cv2.line(frame, (x1, y1 - 3), (x2, y2 + 3), (50, 50, 50), 10)
            elif (math.fabs(slope) <= 0.05):
                cv2.line(frame, (x1 - 3, y1), (x2 + 3, y2), (50, 50, 50), 10)
    # cv2.imwrite(prefix + str(count) + "lines.jpg", frame)
    # cv2.imshow("thresh_im", frame)


def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # print("faces", len(faces))
    if len(faces):
        return 1
    else:
        return 0


def get_length(point1, point2):
    dx = (point1[0] - point2[0])
    dy = (point1[1] - point2[1])
    return (((dx * dx) + (dy * dy)))


def get_slope(point1, point2):
    deltaX = point2[0] - point1[0]
    deltaY = point2[1] - point1[1]
    if deltaX == 0:
        return None
    return deltaY / deltaX


def get_largest_contour(frame, prev_max_contour):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 2)
    high_thresh, thresh_im = cv2.threshold(gray, 180, 255, 0)
    # cv2.imwrite(prefix + str(count) + "thresh_im.jpg", thresh_im)
    # print(high_thresh, thresh_im)
    lowThresh = 0.5 * high_thresh
    edges = cv2.Canny(thresh_im, 100, 150)

    # cv2.imwrite(prefix + str(count) + "gray.jpg", gray)
    # cv2.imwrite(prefix + str(count) + "edges.jpg", edges)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, (5, 5))
    # cv2.imshow("thresh_im", thresh_im)
    # cv2.waitKey()
    image, contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour_size = get_contour_size(prev_max_contour)
    max_contour = prev_max_contour
    max_contour_id = 0
    for i, contour in zip(range(len(contours)), contours):
        contour = cv2.approxPolyDP(contour, 100, 1)
        contour = cv2.convexHull(contour)
        contour_size = get_contour_size(contour)
        # cv2.rectangle(frame,(x,y),(x+w,y+h), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
        if contour_size > max_contour_size:
            # print("BIGGER")
            max_contour_size = contour_size
            max_contour = contour
            max_contour_id = i

    try:
        cv2.line(frame, tuple(
            max_contour[len(max_contour) - 2][0]), start, (0, 255, 0), 100)
    except:
        print("")
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

    # cv2.imwrite(prefix + str(count) + "contour.jpg", frame)

    # cv2.minAreaRect(max_contour)
    # x,y,w,h = cv2.boundingRect(max_contour)
    # cv2.rectangle(gray,(x,y),(x+w,y+h), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
    # cv2.imshow("gray", gray)
    # cv2.waitKey(10000)
    return max_contour


def get_contour_size(contour):
    if contour.size == 0:
        return 0
    return cv2.contourArea(contour)


def crop_to_contour(frame, contour):
    mask = np.zeros(frame.shape[:2], np.uint8)
    convex = cv2.convexHull(contour)
    cv2.fillConvexPoly(mask, contour, (255, 255, 255))
    # cv2.imshow("edges", mask)
    # cv2.waitKey(10)
    frame = cv2.bitwise_and(frame, frame, mask=mask)
    # print("cropped")
    # print(frame)
    return frame


def crop(image, contour):
    if contour.size == 0:
        return image
    x, y, w, h = cv2.boundingRect(contour)
    y = y if y - 5 > 0 else y - 5
    x = x if x - 5 > 0 else x - 5
    return image[y: y + h, x: x + w]


def cmpHash(hash1, hash2):
    # Hash值对比
    # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
    # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
    # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def pHash(img):
    # 感知哈希算法
    # 缩放32*32
    img = cv2.resize(img, (32, 32))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]
    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def SimilarityImages(image1, image2):
    hash1 = pHash(image1)
    hash2 = pHash(image2)
    n = cmpHash(hash1, hash2)
    # print(1 - float(n / 64))
    if (1 - float(n / 64)) > 0.9:
        return 1
    else:
        return 0


def AppeardeImage(image):
    for i in range(count):
        appeared_frame = cv2.imread(prefix + str(i) + ".jpg")
        hash1 = pHash(image)
        hash2 = pHash(appeared_frame)
        n = cmpHash(hash1, hash2)
        # print(1 - float(n / 64))
        if (1 - float(n / 64)) > 0.9:
            return 1
    return 0


def main(fileLocation, videoId):
    global location
    global prev
    global runOnce
    global count
    global prefix
    global avg
    global num_frames
    global num_corners
    global max_contour_orig
    global face_cascade
    global location
    global prefix
    global oldFrame
    global cap
    prev = None
    runOnce = False
    count = 0
    avg = 1
    num_frames = 0
    num_corners = 0
    max_contour_orig = np.empty(0)
    prefix = os.getcwd() + "/navigation/video/slides/" + str(videoId) + "/"
    face_cascade = cv2.CascadeClassifier(os.getcwd() +
                                         "/navigation/video/haarcascade_frontalface_default.xml")
    location = fileLocation
    oldFrame = None
    cap = cv2.VideoCapture(location)
    isExists = os.path.exists(
        os.getcwd() + "/navigation/video/slides/" + str(videoId))
    if not isExists:
        os.makedirs(
            os.getcwd() + "/navigation/video/slides/" + str(videoId))
    while True:
        # Capture frame-by-frame
        for i in range(60):
            ret = cap.grab()
            if not ret:
                print("done")
        ret, frame = cap.read()
        # Our operations on the frame come here
        if ret:
            if False:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                gray = np.float32(edges)
                dst = cv2.cornerHarris(gray, 3, 5, 0.04)
                dst = cv2.normalize(dst)
                # print(dst.sum())
                # Display the resulting frame
                dst = cv2.dilate(dst, None)

            # Threshold for an optimal value, it may vary depending on the image.
                edges[dst > 0.05 * dst.max()] = [255]
                # cv2.imshow("edges", gray)
            if True:

                if runOnce:
                    # detect_lines(frame)
                    frame2 = np.copy(frame)
                    detect_lines(frame2)

                    max_contour_orig = get_largest_contour(
                        frame2, max_contour_orig)
                    # print(crop(frame2, max_contour_orig))
                    frame = crop(frame, max_contour_orig)
                    # cv2.imwrite(prefix + str(count) + ".jpg", frame)
                    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

                    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
                    dst = cv2.dilate(dst, None)

                    # Threshold for an optimal value, it may vary depending on the image.
                    # frame2[dst > 0.0001 * dst.max()] = [0, 0, 255]

                    # dst = cv2.normalize( dst );
                    diff = dst.sum()
                    num_frames += 1
                    avg += diff
                    diff = math.fabs(int(dst.sum()))

                    average_val = math.fabs(int((1 * avg) / num_frames))

                    # cv2.waitKey(1)

                    # print("D-value %s avg %s diff %s avg_threshold %s" % (
                    #     diff, average_val, math.fabs(average_val - diff), average_val / 4))
                    if math.fabs(average_val - diff) > average_val / 4:
                        # cv2.imshow('frame', frame)
                        if not detect_face(oldFrame):
                            if not AppeardeImage(oldFrame):
                                cv2.imwrite(prefix + str(count) +
                                            ".jpg", oldFrame)
                                file = open(prefix + "schedule.txt",
                                            'a', encoding="utf-8")
                                file.write(str(count) + ".jpg " +
                                           str(int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "\n")
                                print(count)
                                count += 1
                                # print("TRIGGERING AD DJ %s avg %s" % (math.fabs(average_val - diff), average_val/4))
                                num_frames = 0
                                avg = 0
                    oldFrame = frame
                    if num_frames == 5:
                        num_frames = 0
                        avg = 0

                else:
                    # 处理的第一帧
                    oldFrame = frame
                    cv2.imwrite(prefix + str(count) +
                                ".jpg", oldFrame)
                    file = open(prefix + "schedule.txt", 'w', encoding="utf-8")
                    file.write(str(count) + ".jpg " +
                               str(int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "\n")
                    count += 1
                    runOnce = True
                """for x in range(len(frame)):
                    for y in range(len(frame[x])):
                        frame[x][y] = [0,255,0]"""
            prev = frame

        else:
            print("done")
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


# main("D:/下载/k-means.mp4", 1)
