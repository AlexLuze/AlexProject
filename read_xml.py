# coding=utf-8
from xml.dom.minidom import parse
import xml.dom.minidom

# 打开xml文档
dom = xml.dom.minidom.parse('E:/BaseFX_maya_test_20190411/base002.xml')

root = dom.documentElement

materials = root.getElementsByTagName("material")

print "%s--->", materials
for material in materials:
    mat_name = material.getAttribute("material_name")
    print "mat_name:", mat_name
    texture_file = material.getElementsByTagName('texture_file')[0]
    print "222:", texture_file
    file_path = texture_file.childNodes[0].data
    print "file_path；", file_path
    objects_list = material.getElementsByTagName('obj')
    print "objects_list；", objects_list
    for obj in objects_list:
        print "object:", obj.getAttribute('obj')
