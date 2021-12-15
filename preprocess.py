#!/usr/bin/env python
# coding: utf-8

# In[6]:


from glob import glob
import PIL.Image as PIL
import numpy as np
import shutil
import os
import xml.etree.ElementTree as et
import pickle
import argparse


# In[13]:


def label_formatter(arg,width,height):
    trans = [round((arg[0]+arg[2])/(width*2),6),round((arg[1]+arg[3])/(height*2),6),round((arg[2]-arg[0])/width,6),round((arg[3]-arg[1])/height,6)]
    for index,i in enumerate(trans):
        if i < 0:
            trans[index] = 0
        elif i > 1:
            trans[index] = 1
    return trans


# In[19]:


def Label_Process(rawlabel,width,height,path):
    classes = ['Vehicle','Pedestrian','TrafficLight','TrafficSign']
    axis_name = ['xmin','ymin','xmax','ymax']
    one_label = []
    entry = []
    for raw in rawlabel:
        one_label = []
        entry = []

        tree = et.parse(raw)
        root = tree.getroot()
        
        for obj in root.iter('object'):
            name = obj.find('name').text
            try:
                name_index = classes.index(name.split('_')[0])
            except:
                continue
            entry.append(name_index)

            for axis in axis_name: # 4
                entry.append(int(obj.find("bndbox").findtext(axis)))
            entry[1:] = label_formatter(entry[1:],width,height)
            entry = ' '.join(str(i) for i in entry) # to string
            one_label.append('%s\n' % entry)
            entry = [] 
        link = raw.split('\\')[-1][:-11]

        with open('%s/train/labels/%s.txt' % (path,link),'w') as f:
            f.writelines(one_label)
    print('%d labels Processed'%len(rawlabel))


# In[14]:


def Image_Process(rimgs,sc,path):
    scale = sc
    batch = 3000
    
    while True:
        if not len(rimgs):
            break
            
        if len(rimgs) <= batch:
            batch = len(rimgs)
            
        rimgsPIL = [ PIL.open(rimgs[i]).convert('RGB').resize(scale) for i in range(batch)]
        print('Processing  %d imgs...' % batch,end=' ')
        [rimgsPIL[i].save('%s/%s' % (path,rimgs[i].split('\\')[-1]),'JPEG') for i in range(len(rimgsPIL))]
        del rimgs[:batch]
        print('Done!')
        rimgsPIL = 0
        


# In[15]:


def main():
    
    
    parser = argparse.ArgumentParser(description="Preprocess for training with YOLO")

    parser.add_argument("-raw", help="Relative location of raw images and labels", required=False,default="Datasets/raw")
    parser.add_argument("-img", help="image size to change", required=False , default=640)
    parser.add_argument("-path", help="images saving path", required=False, default="Datasets")
    parser.add_argument("-mode", help="train or test datasets preprocessing", required=False, default="train")

    args = parser.parse_args()
    
    print('Preprocess Program Start')
    

    scale = [int(args.img),int(int(args.img)*0.75)]

    if args.mode == 'train':
        rawimage = glob('%s/*/*/*.jpg' % args.raw,recursive=True)
        height , width,_ = np.array(PIL.open(rawimage[0])).shape
        rawlabel = glob('%s/*/*/*.xml' % args.raw,recursive=True)
        
        os.makedirs('%s/train/images' % args.path,exist_ok=True)
        os.makedirs('%s/train/labels' % args.path,exist_ok=True)
        if not rawimage or not rawlabel:
            print('No Datasets Found')
            exit()
        print('Detected %d images , %d labels' % (len(rawimage)  , len(rawlabel)))  
        Image_Process(rawimage,scale,'%s/train/images' % args.path)
        Label_Process(rawlabel,width,height,args.path)
    else:
        if args.raw == 'Datasets/raw':
            args.raw = 'Datasets/test'
        rawimage = glob('%s/*/*/*.jpg' % args.raw,recursive=True)
        
        if not rawimage:
            print('No Datasets Found')
            exit()
        print('Detected %d images' % (len(rawimage)))       
        Headfolder = glob('%s/*' % args.raw)
        
        for head in Headfolder:
            Subfolder = glob('%s/*' % head)
            for sub in Subfolder:
                imgs = glob('%s/*.jpg' % sub)
                if not imgs:
                    print('%s Folder is Empty!' % sub)
                    continue
                Image_Process(imgs,scale,sub)



# In[ ]:


if __name__ == "__main__":
    main()

