#!/usr/bin/env python
# coding: utf-8

# In[45]:


from xml.etree.ElementTree import Element,dump,SubElement , ElementTree
import argparse
import os
import shutil
from glob import glob


# In[37]:


def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# In[88]:


def Label_Reformatter(arg,width,height):
    classes = ['Vehicle','Pedestrian','TrafficLight','TrafficSign']
    arg[0] = int(arg[0])
    arg[1:] = [float(i) for i in arg[1:]]
    half_x , half_y = arg[3]/2 , arg[4]/2
    result = [classes[arg[0]],int((arg[1]-half_x)*width),int((arg[2]-half_y)*height),int((arg[1]+half_x)*width),int((arg[2]+half_y)*height)]
    return result


# In[46]:


def main():
    axis_name = ['xmin','ymin','xmax','ymax']
    
    parser = argparse.ArgumentParser(description="PostProcessing")
    parser.add_argument("-path", help="location of images to be postprocess", required=False, default='Datasets/test')
    parser.add_argument("-width", help="original image width size", required=False, default=1920)
    parser.add_argument("-height", help="original image height size", required=False, default=1080)
    args = parser.parse_args()
    
    print('Post-Processing Program Start')
    
    Labelfolder = glob('%s/*/*_Result' % args.path)
    for folder in Labelfolder:
        txts = glob('%s/*.txt' % folder)

        for txt in txts:
            with open(txt,'r') as f:
                datas = f.readlines()
            for index,data in enumerate(datas):
                datas[index] = data.strip('\n').split()

            root = Element('annotation')

            for data in datas:
                obj= SubElement(root,'object')
                org_data = Label_Reformatter(data,args.width , args.height)
                name = SubElement(obj,'name')
                name.text = org_data[0]

                bnd = SubElement(obj,'bndbox')
                for index,axis in enumerate(axis_name):
                    SubElement(bnd,axis).text = str(org_data[index+1])
                indent(root)
                #dump(root)
                tree = ElementTree(root)
                tree.write('%s.xml' % txt[:-4] ,encoding='utf-8', xml_declaration=True)
            os.remove(txt)
        print('%d label data processed' % len(txts))
    
    print('All label datas at %s have been Reformatted Successfully' % args.path)


# In[ ]:


if __name__ == '__main__':
    main()

