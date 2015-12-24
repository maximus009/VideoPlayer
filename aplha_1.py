import cv2
import sys
from time import sleep

def flick(x):
    pass

cv2.namedWindow('image')
cv2.moveWindow('image',250,100)

video = sys.argv[1] 
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar('S','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('S','image',0)

cv2.createTrackbar('F','image', 1, 100, flick)
cv2.setTrackbarPos('F','image',30)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'

control_pad = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                -1: status, 
                27: 'exit'}
while True:
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
    if im.shape[0]>600:
        im = cv2.resize(im, (500,500))
    #cv2.putText(im, status, )
    cv2.imshow('image', im)
    status = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                -1: status, 
                27: 'exit'}[cv2.waitKey(10)]

    if status == 'play':
      frame_rate = cv2.getTrackbarPos('F','image')
      sleep(0.1-frame_rate/1000.0)
      i+=1
      cv2.setTrackbarPos('S','image',i)
      continue
    if status == 'stay':
      i = cv2.getTrackbarPos('S','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='slow':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='fast':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
  except KeyError:
      print "Invalid Key was pressed"
cv2.destroyWindow('image')
