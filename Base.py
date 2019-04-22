#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from maya import cmds
import pymel.core as pm
import maya.OpenMayaUI as omui

# 创建并返回一个基于Maya主窗口的QWidget类的窗口
def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return main_window

def arrange_uv():
    '''
    Rearrange the UV of the scene file according to the objects connected by the texture ball,
    and rename the texture file connected by the texture ball according to the position of UV quadrant
    :return: Returns True on success
    '''
    # 1.通过材质球的SG节点找到对应obj信息
    # <1>.查找场景中的所有SG节点并保存列表sg_nodes_list中
    sg_nodes_list = cmds.ls(type='shadingEngine')
    if 'initialParticleSE' in sg_nodes_list or 'initialShadingGroup' in sg_nodes_list:
        sg_nodes_list.remove('initialParticleSE')
        sg_nodes_list.remove('initialShadingGroup')
        # <2>.通过材质的SG节点找到对应物体或者是面级别
    column = 0  # 列数
    for index, sg_node in enumerate(sg_nodes_list):
        row = (index) / 10  # 行数
        # 使用UDIM (Mari):UV 坐标使用公式 1000+(u+1+v*10)
        udim_name = 1000 + (column + 1 + row * 10)
        # 调用处理UV的函数
        edit_uv_result = edit_uv(sg_node, column, row)
        # 调用设置贴图信息函数
        set_attr_result = set_attr_of_textrue(sg_node, udim_name)
        if column == 9:
            column = 0
        else:
            column += 1
    return True


# 2.对于相同材质球的obj，进行UV同一象限排布，没有重叠
def edit_uv(sg_node, column, row):
    '''

    :param sg_node:
    :param column:
    :param row:
    :return:
    :type:
    '''
    cmds.hyperShade(objects=sg_node)  # 返回值是直接选择物体，并非节点
    # <1>.通过‘被选择的’物体找到并选中UV点
    converted_uvs = pm.polyListComponentConversion(tuv=1)
    cmds.select(converted_uvs, add=True)
    # <2>.挪动UV点到指定的区域
    cmds.polyEditUV(u=column, v=row)
    return True


# <3>.通过SG节点重命名找到材质球所连接的贴图文件并保存
def set_attr_of_textrue(sg_node, udim_name):
    '''
    Find the map file connected to the texture ball through the SG node,
    copy and rename the map file in quadrant position.
    :param sg_node:
    :param udim_name:
    :return:
    :type:  bool
    '''
    color_channel_str = 'color'
    material_node = cmds.listConnections(sg_node + '.surfaceShader')
    color_file_node = cmds.listConnections('%s.%s' % (material_node[0], color_channel_str), type='file')
    texture_file_str = cmds.getAttr("%s.fileTextureName" % color_file_node[0])
    # <3>.通过UV点的位置象限重命名该材质球所连接的贴图文件,命名遵循 <channel>.#.jpg
    file_name_str = color_channel_str + '.' + str(udim_name)
    # <4>.链接函数处理贴图文件。
    new_path = deal_texture(texture_file_str, file_name_str)
    # <5>.更改材质所链接贴图及uv Tiling Mode 为Mari格式。
    cmds.setAttr("%s.fileTextureName" % color_file_node[0], new_path, type="string")
    cmds.setAttr('%s.uvTilingMode' % color_file_node[0], 3)
    return True


# 3.处理贴图文件函数
def deal_texture(source_texture, texture_name):
    '''
    Copy the texture file the texture ball is connected to and change its name.
    :param str source_texture: Absolute path to the original map file.
    :param str texture_name: Name of the modified texture file.
    :return: texture_path: Modified map file absolute path
    :type: str
    '''
    source_texture_name = os.path.basename(source_texture).split('.tif')[0]
    texture_path = source_texture.replace(source_texture_name, texture_name)
    shutil.copy(source_texture, texture_path)
    return texture_path
