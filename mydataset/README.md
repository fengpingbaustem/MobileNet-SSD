#caffe SSD目标检测lmdb数据格式制作
======================
主要参考《caffe SSD目标检测lmdb数据格式制作.pdf》中提到的制作VOC数据集的方法，生成自己的lmdb文件用于Caffe SSD的训练。
本目录中不包含jpg和mdb文件。
制作过程
----------------------
1. 通过find_face_in_vid.py抓取视频文件中的帧，并通过dlib检测人脸的位置，生成*.jpg和gt_*.txt文件到Image和label目录；
2. 通过create_voc_data.py生成test和train的数据库文件，本文件中对insertObject函数增加了cls参数，取值为face的name；
3. 通过create_data.sh生成lmdb文件；

