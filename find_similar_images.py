#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image
import six

import imagehash

"""
Demo of hashing
Link to docs: https://github.com/JohannesBuchner/imagehash
"""
def find_similar_images(userpaths, hashfunc = imagehash.average_hash, threshold = 20):
    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
            f.endswith(".jpeg") or f.endswith(".bmp") or \
            f.endswith(".gif") or '.jpg' in f or  f.endswith(".svg")
    
    image_filenames = []
    for userpath in userpaths:
        image_filenames += [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    images = []
    for img_filename in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img_filename))
        except Exception as e:
            print('Problem:', e, 'with', img_filename)
            continue

        images.append({
            'hash': hash,
            'filename': img_filename
        })
        
    for image in images:

        hash = image['hash']
        filename = image['filename']

        similar_images = []

        for image_to_compare in images:
            another_hash = image_to_compare['hash']
            another_filename = image_to_compare['filename']
            diff = hash - another_hash
            # TODO: Change this for debugging
            # print('diff: ', diff, ' images: ', filename, ' -> ', another_filename)
            if diff <= threshold and another_filename != filename:
                similar_images.append(another_filename)
        
        if len(similar_images) > 0:
            print(filename, '  is similar or equal to', ', '.join(similar_images))
            print('==============================')


if __name__ == '__main__':
    import sys, os
    def usage():
        sys.stderr.write("""SYNOPSIS: %s [ahash|phash|dhash|...] [<threshold>] [<directory>]
Identifies similar images in the directory.
Method: 
  ahash:      Average hash
  phash:      Perceptual hash
  dhash:      Difference hash
  whash-haar: Haar wavelet hash
  whash-db4:  Daubechies wavelet hash
""" % sys.argv[0])
        sys.exit(1)
    
    hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')
    else:
        usage()
    threshold = sys.argv[2] if len(sys.argv) > 2 else 20
    userpaths = sys.argv[3:] if len(sys.argv) > 3 else "."
    find_similar_images(userpaths=userpaths, hashfunc=hashfunc, threshold=int(threshold))
    