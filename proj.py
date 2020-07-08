# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 00:08:07 2019

@author: shivansh
"""

import sys
from PIL import Image
from random import randrange
import math
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def histogram(path):
    img = cv2.imread(path, -1)
    #cv2.imshow('GoldenGate',img)

    color = ('b','g','r')
    for channel,col in enumerate(color):
        histr = cv2.calcHist([img],[channel],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
#        plt.title('Histogram for color scale picture')
    plt.show()

def padHex(string, length):
    while len(string) < length:
        string = "0" + string
    return string

def padBack(string, length):
    while len(string) < length:
        string += "0"
    return string

#default pixel mapping for AnyImg/ImgAny. Maps row by row, left to right, top to bottom.
def linearMap(n, width, height):
    return (n % width, n // width)

def main():
    choice = int(input("Enter choice-\n1.Encrypt\n2. Decrypt\n "))
    if choice == 1:
#        if len(sys.argv) < 7:
#           raise Exception("""It seems like you're missing some arguments.
#Run stego.py with no arguments for help.""")
        sec=input("Enter the secret file:")
        file = open(sec, "rb")
        cov=input("Enter the cover image:")
        imgIn = Image.open(cov).convert("RGBA")
        out=input("Enter the output image:")
        imgOutPath = out
        b=input("Enter the bits:")
        bits = abs(int(b))
        channel=input("Enter channels:r: +1. g: +2. b: +4. a: +8.\ne.g. encoding in red and blue channels: 1+4 = 5.\n")
        style = padHex(bin(abs(int(channel)))[2:], 4)
        R = int(style[3])
        G = int(style[2])
        B = int(style[1])
        A = int(style[0])
        if bits > 8:
            raise Exception("""stego.py does not export more than 8 bits per channel""")
        width, height = imgIn.size
        if (width*height*(bits * (R + G + B + A)))//8 < os.path.getsize(sec):
            raise Exception("""Can't fit file into image; use more bits or channels.""")
        key = chr(0)
        key_choice=input("Want to enter key? y/n")
        if key_choice =='y':
            key=input("Enter key:")
        else:
            print("Key will be:",key)
            #perform embedding
            #first read file, perform xor, and sort into appropriate lists per pixel
        binString = "" #sort all bytes into this linear binary string
        #file=secret file
        b = file.read(1)
        while b:
            b = int.from_bytes(b, byteorder = "big", signed = False) ^ ord(key[0])# cnverting the byte value into 256base and then xor with key
            key = key[1:] + key[0]
            binString = binString + padHex(bin(b)[2:], 8)
            b = file.read(1)
           
        binString = binString + "0"*256 #a null terminus to mark the end of file
        lsbList = [] #sort binary into list of ints that can be added to pixels
        while len(binString) > 0:
            pix = [0, 0, 0, 0]
            if R and binString[:bits] != "":
                pix[0] = int(binString[:bits], 2)
                binString = binString[bits:]
            if G and binString[:bits] != "":
                pix[1] = int(binString[:bits], 2)
                binString = binString[bits:]
            if B and binString[:bits] != "":
                pix[2] = int(binString[:bits], 2)
                binString = binString[bits:]
            if A and binString[:bits] != "":
                pix[3] = int(binString[:bits], 2)
                binString = binString[bits:]
            lsbList.append(pix)
        #pad out rest of image with noise
        while len(lsbList) < width*height:
            lsbList.append([randrange(2**bits), randrange(2**bits), randrange(2**bits), randrange(2**bits)])
        #now, add values to pixels in image
        for n in range(width*height):
            pixXY = linearMap(n, width, height)
            r,g,b,a = imgIn.getpixel(pixXY)
            for i in range(bits): # set bits # of lsb to 0
                r -= 2**i * int(padHex(bin(r)[2:], 8)[::-1][i:i+1]) * R
                g -= 2**i * int(padHex(bin(g)[2:], 8)[::-1][i:i+1]) * G
                b -= 2**i * int(padHex(bin(b)[2:], 8)[::-1][i:i+1]) * B
                a -= 2**i * int(padHex(bin(a)[2:], 8)[::-1][i:i+1]) * A
            r += lsbList[n][0] * R
            g += lsbList[n][1] * G
            b += lsbList[n][2] * B
            a += lsbList[n][3] * A
            imgIn.putpixel(pixXY,(r,g,b,a))

        imgIn.save(imgOutPath, "PNG")
#        print("Histogram of cover image:")
 #       histogram(cov);
  #      print("Histogram of coded image:")
  #      histogram(out);
        print("finish!")
        
        
    if choice == 2:
        in_file=input("Enter the file:")
        imgIn = Image.open(in_file).convert("RGBA")
        out_file=input("Enter the output file:")
        file = open(out_file, "wb")
        b=input("Enter the bits:")
        bits = abs(int(b))
        channel=input("Enter channels:")
        style = padHex(bin(abs(int(channel)))[2:], 4)
        R = int(style[3])
        G = int(style[2])
        B = int(style[1])
        A = int(style[0])
        if bits > 8:
            raise Exception("""stego.py does not support more than 8 bits per channel""")
        key = chr(0)
        key_choice=int(input("Want to enter key? 1 for yes"))
        if key_choice ==1:
            key=input("Enter key:")
        else:
            print("Key will be:",key)

            #first extract out all lsb data
        binString = ""
        width, height = imgIn.size
        for n in range(width*height):
            pixXY = linearMap(n, width, height)
            r,g,b,a = imgIn.getpixel(pixXY)
            dr = 0
            dg = 0
            db = 0
            da = 0
            for i in range(bits):
                dr += 2**i * int(padHex(bin(r)[2:], 8)[::-1][i:i+1])
                dg += 2**i * int(padHex(bin(g)[2:], 8)[::-1][i:i+1])
                db += 2**i * int(padHex(bin(b)[2:], 8)[::-1][i:i+1])
                da += 2**i * int(padHex(bin(a)[2:], 8)[::-1][i:i+1])
            binString += (padHex(bin(dr)[2:],bits) if R else "") + (padHex(bin(dg)[2:], bits) if G else "") + (padHex(bin(db)[2:], bits) if B else "") + (padHex(bin(da)[2:], bits) if A else "")
        #now, apply xor and write string back into file
        while binString[:256] != "0"*256:
            b = int(binString[:8], 2) ^ ord(key[0])
            key = key[1:] + key[0]
            file.write(b.to_bytes(1, byteorder = "big"))
            binString = binString[8:]
        file.close()
        print("finish!")
        
if __name__ == '__main__':
    main()