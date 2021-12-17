#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os
import shutil
from glob import glob


# In[ ]:


def main():
    parser = argparse.ArgumentParser(description="Predict Test Images")

    parser.add_argument("-model", help="predict model location", required=False,default="Model")
    parser.add_argument("-img", help="image size to change", required=False , default=640)
    parser.add_argument("-conf", help="predict confidence", required=False , default=0.6)
    parser.add_argument("-path", help="location for save predicted labels", required=False, default="Datasets/test")
    parser.add_argument("-source", help="location of images", required=False, default="Datasets/test")
    parser.add_argument("-name", help="name of saving folder ", required=False, default="result")
    args = parser.parse_args()
    
    print('Inference Program Start')
    Headfolder = glob('%s/*/' % args.path)
    
    if not Headfolder:
        print("There's no files, check %s" %(args.path))
    else:
        os.system("python preprocess.py -img %s -mode test" % args.img)
        for head in Headfolder:
            Subfolder = glob('%s/*' % head)

            for sub in Subfolder:
                if sub.split('_')[-1] == 'Result':
                    continue
                os.makedirs('%s/%s_Result' % (head,sub.split('\\')[-1]),exist_ok=True)
                
                os.system("python YOLO/detect.py --weights %s/model.pt --img %s --conf %s --source %s --name %s --save-txt --save-conf --exist-ok --nosave" % (args.model,args.img,args.conf,sub,args.name))
                labels = glob('YOLO/runs/detect/%s/labels/*.txt' % (args.name))
                for label in labels:
                    shutil.move(label,'%s/%s_Result' % (head,sub.split('\\')[-1]))


        print('Labels are moved at %s' % (args.path))


# In[ ]:


if __name__ == '__main__':
    main()

