#!/usr/bin/python

import glob
import os
import sys

from PIL import Image
from functools import reduce

EXTS = 'jpg', 'jpeg', 'gif', 'png'

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    # print("im.getdata:" + str(im.getdata))
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, y_z : x | y_z[1] << y_z[0], enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())), 0)

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

#第一个参数是基准图片，第二个参数是用来比较的其他图片所在的目录，返回结果是两张图片之间不相同的数据位数量（汉明距离）。


def sort_img(user):
	images = []
	#读取目录下所有jpg文件，并放到images列表中
	images.extend(glob.glob(user+'\\*.jpg'))
	print('images=',images)
	print(len(images))

	#imges排序结果保存在seq列表中
	seq = []
	#基准图片为im，h是im的hash值
	im=images[0]
	h = avhash(im)
	for f in images:
		seq.append((f, hamming(avhash(f), h)))
	print("seq:" + str(seq))
	sorted_pics=[]
	#对结果seq列表的元素按第二列的值排序，并只抽取排序结果中的图片，加入sorted_pics列表中
	for f, ham in sorted(seq, key=lambda i: i[1]):
		print ("%d\t%s" % (ham, f))
		sorted_pics.append(f)
	#print(sorted_pics)
	return sorted_pics

if __name__ == '__main__':
	user='@40a275ed93ba42443ed2084cad03e2ccf8e95a7539b93d0fae5891262a8c958d'
	sorted_pics=sort_img(user)
	print (sorted_pics)