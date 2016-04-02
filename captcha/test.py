import cv2
import os
import string

keymap = dict(zip(range(97,123),string.lowercase) + zip(range(48,58),range(0,10)))
print keymap

cv2.namedWindow("TEST")
l = os.listdir('/home/zsj/Workspace/python/ustcmis/captcha')
l2 = [i for i in l if i.endswith('.jpg')]
for i in l2:
    img = cv2.imread(i)
    cv2.imshow("TEST", img)
    key = int(cv2.waitKey(0))
    if key == 27:
        break
    if keymap.has_key(key):
        print keymap[key]
        print i
        os.rename(i,'./collect/' + str(keymap[key]) + '/' + str(i))
