#!/usr/bin/python

from PIL import Image

pilImage = Image.open('btn_play.png')
print pilImage.convert("RGB").tobytes()

def main():
    return True

if __name__ == '__main__':
    main()
