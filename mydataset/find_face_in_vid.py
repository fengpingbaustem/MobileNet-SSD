import cv2
import sys
import os
import time
import dlib
# ***************************************************************
# Defined for opencv face detection
# ***************************************************************
storagePath = 'myface/JPEGImages/'
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
eyePath = 'haarcascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(eyePath)
detector = dlib.get_frontal_face_detector()
t_start = time.time()
fps = 0
def opencv_detection(gray):
    faces = []
    face_locations = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in face_locations:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) == 0:
            print("eyes not found")
            continue
        faces.append((x, y, x + w, y +h))
    return faces

def dlib_detection(image):
    faces = []
    dets = detector(image, 1)
    for i, d in enumerate(dets):
        faces.append((d.left(), d.top(), d.right(), d.bottom()))
    return faces

labels = [  "zhaocheng",
            "yifeng",
            "zhangjun"]
# ***************************************************************
# Processing the images
# ***************************************************************
lastsendTime = time.time()
for name in labels:
    # Capture frame-by-frame
    print("processing {}".format(name))
    video_capture = cv2.VideoCapture("/home/fengping/Videos/" + name + ".mp4")
    fps = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        # gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        # faces = opencv_detection(gray)
        faces = dlib_detection(frame)
        filename=name
        if len(faces) > 0 and fps < 10:
            cv2.imwrite("{}{}-{}.jpg".format(storagePath + "test/", filename, str(fps)),
                        frame)
            cmd = "echo {} >> {}".format(filename, "myface/ImageSets/Main/test.txt")
            os.system(cmd)
            for i, (x, y, w, h) in enumerate(faces):
                cmd = "echo \"{} {} {} {} \\\"{}\\\"\" >> {}".format(x, y, w, h, name,
                                                                "myface/label/test/" + "gt_" + filename +"-"+str(fps)+ ".txt")
                os.system(cmd)
        elif len(faces) > 0:
            cv2.imwrite("{}{}-{}.jpg".format(storagePath + "train/", filename, str(fps)),
                        frame)
            cmd = "echo {} >> {}".format(filename, "myface/ImageSets/Main/train.txt")
            os.system(cmd)
            for i, (x, y, w, h) in enumerate(faces):
                cmd = "echo \"{} {} {} {} \\\"{}\\\"\" >> {}".format(x, y, w, h, name,
                                                                "myface/label/train/" + "gt_" + filename +"-"+str(fps) + ".txt")
                os.system(cmd)
        # Calculate and show the FPS
        fps = fps + 1
        sfps = fps / (time.time() - t_start)
        #cv2.putText(frame, "FPS : " + str(int(sfps)) + '//' + str(fps), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # Display the resulting frame
        #cv2.imshow('Video', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    # When everything is done, release the capture
    video_capture.release()

