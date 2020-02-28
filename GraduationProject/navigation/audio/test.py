from moviepy.editor import *


video = VideoFileClip('D:\\下载\\【03】12 课程介绍-课程后勤.mp4')
audio = video.audio
audio.write_audiofile('D:\\下载\\test2.mp3')
