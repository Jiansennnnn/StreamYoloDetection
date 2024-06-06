import time

import cv2
from win32con import HWND_TOPMOST, SWP_NOMOVE, SWP_NOSIZE
from win32gui import FindWindow, SetWindowPos

from toolkit import Capturer, Detector, Timer
from toolkit import Timer, Capturer

scale_factor = 1
region = ((3440 // 5 * 2) * scale_factor, (1440 // 3) * scale_factor, (3440 // 5) * scale_factor, (1440 // 3)* scale_factor)
#region = (2752, 480, 688, 480)
weight = r'C:\Users\Jiansen\Desktop\Project\weights\yolov10n.pt'
detector = Detector(weight)

title = 'Realtime Screen Capture Detect'
while True:

    t1 = time.perf_counter_ns()
    img = Capturer.backup(region)
    t2 = time.perf_counter_ns()
    _, img = detector.detect(image=img, show=True)
    t3 = time.perf_counter_ns()
    cv2.putText(img, f'{Timer.cost(t3 - t1)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
    cv2.putText(img, f'{Timer.cost(t2 - t1)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
    cv2.putText(img, f'{Timer.cost(t3 - t2)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    #cv2.imshow(title, img)
    cv2.imshow(title,img)
    SetWindowPos(FindWindow(None, title), HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    k = cv2.waitKey(1)  # 0:不自动销毁也不会更新, 1:1ms延迟销毁
    if k % 256 == 27:
        cv2.destroyAllWindows()
        exit('ESC ...')
