from IPython.display import display, Javascript, clear_output
#from google.colab.output import eval_js
from base64 import b64decode
import time
import pybase64
from IPython.display import Image
import os
import cv2
from io import BytesIO
import PIL
import IPython
#from funboost import boost, BrokerEnum
import cv2
import supervision as sv
from ultralytics import YOLOv10
import matplotlib.pyplot as plt
import numpy as np
import base64, io
from PIL import Image

plt.ion()  # Turn on interactive mode

## Yolo Dection Model Load
def YoloDetect(model, image):
  results = model(image)[0]
  detections = sv.Detections.from_ultralytics(results)
  bounding_box_annotator = sv.BoundingBoxAnnotator()
  label_annotator = sv.LabelAnnotator()
  annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
  annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)
  #sv.plot_image(annotated_image)
  #img_display.set_data(sv.plot_image(annotated_image))
  #return np.array(Image.open(io.BytesIO(base64.b64decode(annotated_image))))
  return annotated_image


#Use 'jpeg' instead of 'png' (~5 times faster)
def array_to_image(a, fmt='jpeg'):
    #Create binary stream object
    f = BytesIO()

    #Convert array to binary stream object
    PIL.Image.fromarray(a).save(f, fmt)

    return IPython.display.Image(data=f.getvalue())

def get_frame(cam):
    # Capture frame-by-frame
    ret, frame = cam.read()

    #flip image for natural viewing
    frame = cv2.flip(frame, 1)

    return frame

d = display("", display_id=1)
d2 = display("", display_id=2)


###def take_photo(filename='photo', quality=1.0):
###  js = Javascript('''
###    async function takePhoto(quality) {
###      const div = document.createElement('div');
###      //const capture = document.createElement('button');
###      //capture.textContent = 'Capture';
###      //div.appendChild(capture);
###
###      const video = document.createElement('video');
###      video.style.display = 'block';
###      const stream = await navigator.mediaDevices.getUserMedia({video: true});
###
###      document.body.appendChild(div);
###      div.appendChild(video);
###      video.srcObject = stream;
###      await video.play();
###
###      // Resize the output to fit the video element.
###      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
###
###      // Wait for Capture to be clicked.
###      //await new Promise((resolve) => capture.onclick = resolve);
###      //setInterval(abc, 1000);
###
###      const canvas = document.createElement('canvas');
###      canvas.width = video.videoWidth;
###      canvas.height = video.videoHeight;
###      canvas.getContext('2d').drawImage(video, 0, 0);
###      stream.getVideoTracks()[0].stop();
###      div.remove();
###      return canvas.toDataURL('image/jpeg', quality);
###
###    }
###    ''')

a = 0

Yolo_instance = YOLOv10(f'{HOME}/weights/yolov10n.pt')
# Initialize the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
#annotated_image = get_new_image()
img_0 = cv2.imread('/content/LoadingPic.jpg')
img_display = ax.imshow(img_0)

while True:
    t1 = time.time()
    #time.sleep(0)

    display(js)
    data = eval_js('takePhoto({})'.format(quality))
    tt = time.time()
    print("evalJS "+ str(tt-t1))

    #binary = b64decode(data.split(',')[1])
    binary = pybase64.b64decode(data.split(',')[1])
    t2 = time.time()
    print("decoding"+ str(t2-tt))
    t3 = time.time()
    with open(filename + str(a) + '.jpg', 'wb') as f:
      f.write(binary)
    t4 = time.time()
    print("writing file"+ str(t4-t3))
    ## Caputring Imge load
    t5 = time.time()
    img = cv2.imread(filename + str(a) + '.jpg')
    ## Detection load
    annotated_image = YoloDetect(Yolo_instance,img)
    img_display.set_data(annotated_image)
    fig.canvas.draw()
    fig.canvas.flush_events()

    #frame = get_frame(img)
    frame = img
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = array_to_image(frame)
    t6 = time.time()
    print("Caputring Imge load"+ str(t6-t5))
    d.update(im)

    s = f"""{int(1/(t2-t1))} FPS"""
    d2.update( IPython.display.HTML(s) )
    #display(Image(filename+ str(a)+ '.jpg'))
    #clear_output(wait=False)
    if a != 0:
        os.remove(filename + str(a-1) + '.jpg')
        a +=1
return filename
    try:
        filename = take_photo()
        print('Saved to {}'.format(filename))

        # Show the image which was just taken.
        display(Image(filename))
    except Exception as err:
        # Errors will be thrown if the user does not have a webcam or if they do not
        # grant the page permission to access it.
        print(str(err))