#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os
import shutil
from glob import glob


# In[ ]:


def main():
    
    parser = argparse.ArgumentParser(description="train Model")

    parser.add_argument("-weights", help="weight file location", required=False,default="YOLO/yolov5s.pt")
    parser.add_argument("-epochs", help="training epochs", required=False , default=10)
    parser.add_argument("-batch", help="training batch size", required=False , default=4)
    parser.add_argument("-img", help="img size", required=False, default=640)
    
    args = parser.parse_args()
    print('Training Program Start')
    os.makedirs('Model',exist_ok=True)

    os.system("python YOLO/train.py --data YOLO/data.yaml --cfg YOLO/models/yolov5s.yaml  --weights %s --epochs %s --batch %s --img %s --name Model --exist-ok" % (args.weights,args.epochs,args.batch,args.img))
    if os.path.exists('Model/model.pt') and os.path.exists('YOLO/runs/train/Model/weights/best.pt'):
        if os.path.exists('Model/model.old'):
            os.remove('Model/model.old')
        os.rename('Model/model.pt','Model/model.old')
    
    try:
        shutil.move('YOLO/runs/train/Model/weights/best.pt','Model/model.pt')
    except:
        print('Training Failed..')
    else:
        print('Training Complete! Model saved')


# In[ ]:


if __name__ == '__main__':
    main()

