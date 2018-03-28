import os
import numpy as np
import sys
import cv2
from itertools import islice
from xml.dom.minidom import Document
def getlabelname(file):
    return os.path.splitext(file)[0].split("-")[0]

def create_list(dataName,img_list_txt,img_path,img_name_list_txt,type):
   f=open(img_name_list_txt,'w')
   fAll=open(img_list_txt,'w')
   for name in os.listdir(img_path):
      f.write(name[0:-4]+'\n')
      fAll.write(dataName+'/'+'JPEGImages'+'/'+type+'/'+name[0:-4]+'.jpg'+' ')
      fAll.write(dataName+'/'+'Annotations'+'/'+type+'/'+name[0:-4]+'.xml'+'\n')
   f.close()
def insertObject(doc, datas, cls):
    obj = doc.createElement('object')
    name = doc.createElement('name')

    name.appendChild(doc.createTextNode(cls))
    obj.appendChild(name)
    bndbox = doc.createElement('bndbox')

    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(datas[0]).strip(' ')))
    bndbox.appendChild(xmin)
    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode(str(datas[1]).strip(' ')))
    bndbox.appendChild(ymin)
    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode(str(datas[2]).strip(' ')))
    bndbox.appendChild(xmax)
    ymax = doc.createElement('ymax')
    ymax.appendChild(doc.createTextNode(str(datas[3]).strip(' ')))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)
    return obj


def txt_to_xml(labels_path,img_path,img_name_list_txt,xmlpath_path,bb_split,name_size):
    img_name_list=np.loadtxt(img_name_list_txt,dtype=str)
    name_size_file=open(name_size,'w')
    for img_name in img_name_list:
        print(img_name)
        imageFile = img_path + img_name + '.jpg'
        cls = getlabelname(img_name + '.jpg')
        img = cv2.imread(imageFile)
        imgSize = img.shape
        name_size_file.write(img_name+' '+str(imgSize[0])+' '+str(imgSize[1])+'\n')

        sub_label=labels_path+'gt_'+img_name+'.txt'
        fidin = open(sub_label, 'r')
        flag=0
        for data in islice(fidin, 0, None):
            print(data)
            flag=flag+1
            data = data.strip('\n')
            datas = data.split(bb_split)
            if 5 != len(datas):
                print (img_name+':bounding box information error')
                exit(-1)
            if 1 == flag:
                xml_name = xmlpath_path+img_name+'.xml'
                f = open(xml_name, "w")
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)

                folder = doc.createElement('folder')
                folder.appendChild(doc.createTextNode(dataName))
                annotation.appendChild(folder)

                filename = doc.createElement('filename')
                filename.appendChild(doc.createTextNode(img_name+'.jpg'))
                annotation.appendChild(filename)

                size = doc.createElement('size')
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(imgSize[1])))
                size.appendChild(width)
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(imgSize[0])))
                size.appendChild(height)
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(imgSize[2])))
                size.appendChild(depth)
                annotation.appendChild(size)
                annotation.appendChild(insertObject(doc, datas, cls))
            else:
                annotation.appendChild(insertObject(doc, datas, cls))
        try:
            f.write(doc.toprettyxml(indent='    '))
            f.close()
            fidin.close()
        except:
            pass
    name_size_file.close()
if __name__ == '__main__':
   dataName = 'myface'  # dataset name
   type = 'train'  # type
   bb_split=' '
   img_path = dataName + '/JPEGImages/' + type + '/'  # img path
   img_name_list_txt = dataName + '/ImageSets/Main/'+type+'.txt'
   img_list_txt=type+'.txt'
   create_list(dataName,img_list_txt,img_path,img_name_list_txt,type)
   labels_path = dataName+'/label/'+type+'/'
   xmlpath_path = dataName+'/Annotations/'+type+'/'
   name_size=type+'_name_size.txt'
   txt_to_xml(labels_path,img_path,img_name_list_txt,xmlpath_path,bb_split,name_size)