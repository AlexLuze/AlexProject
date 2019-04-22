#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author  : Alex
@Time    : 2019/4/22 10:31
"""
import os
import shutil
from maya import cmds
import pymel.core as pm

def arrange_uv():
    '''
    Rearrange the UV of the scene file according to the objects connected by the texture ball,
    and rename the texture file connected by the texture ball according to the position of UV quadrant.
    :return: Returns True on success.
    '''
    sg_nodes_list = cmds.ls(type='shadingEngine')
    if 'initialParticleSE' in sg_nodes_list or 'initialShadingGroup' in sg_nodes_list:
        sg_nodes_list.remove('initialParticleSE')
        sg_nodes_list.remove('initialShadingGroup')
    column = 0
    for index, sg_node in enumerate(sg_nodes_list):
        row = (index) / 10
        # Use UDIM (Mari):UV coordinates use formula 1000+(u+1+v*10)
        udim_name = 1000 + (column + 1 + row * 10)
        edit_uv_result = edit_uv(sg_node, column, row)
        set_attr_result = set_attr_of_textrue(sg_node, udim_name)
        if column == 9:
            column = 0
        else:
            column += 1
    return True

def edit_uv(sg_node, column, row):
    '''
    For obj of the same material sphere, UV is arranged in the same quadrant without overlapping.
    :param str sg_node: the current SG node.
    :param int column: number of u.
    :param int row: number of v
    :return: True
    :type: bool
    '''
    cmds.hyperShade(objects=sg_node)
    converted_uvs = pm.polyListComponentConversion(tuv=1)
    cmds.select(converted_uvs, add=True)
    cmds.polyEditUV(u=column, v=row)
    return True

def set_attr_of_textrue(sg_node, udim_name):
    '''
    Find the map file connected to the texture ball through the SG node,
    copy and rename the texture file in quadrant position,and
    change the texture path and uv Tiling Mode to Mari format.
    :param str sg_node: the current SG node.
    :param int udim_name: UDIM serial number.
    :return: True
    :type:  bool
    '''
    color_channel_str = 'color'
    material_node = cmds.listConnections('%s.surfaceShader' % sg_node)
    color_file_node = cmds.listConnections('%s.%s' % (material_node[0], color_channel_str), type='file')
    texture_file_str = cmds.getAttr("%s.fileTextureName" % color_file_node[0])
    file_name_str = '{}.{}'.format(color_channel_str,str(udim_name))
    new_path = deal_texture(texture_file_str, file_name_str)
    cmds.setAttr("%s.fileTextureName" % color_file_node[0], new_path, type="string")
    cmds.setAttr('%s.uvTilingMode' % color_file_node[0], 3)
    return True

def deal_texture(source_texture, texture_name):
    '''
    Copy the texture file the texture ball is connected to and change its name.
    :param str source_texture: Absolute path to the original map file.
    :param str texture_name: Name of the modified texture file.
    :return: str texture_path: Modified map file absolute path
    :type: str
    '''
    file_format = os.path.splitext(source_texture)
    source_texture_name = os.path.basename(source_texture).split(file_format[-1])[0]
    texture_path = source_texture.replace(source_texture_name, texture_name)
    shutil.copyfile(source_texture, texture_path)
    return texture_path