#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import shutil
from maya import cmds
import pymel.core as pm

# 1.通过材质球的SG节点找到对应obj信息
# <1>.查找场景中的所有SG节点并保存列表sgNodes_list中
sgNodes_list = cmds.ls(type='shadingEngine')
if 'initialParticleSE' in sgNodes_list or 'initialShadingGroup' in sgNodes_list:
    sgNodes_list.remove('initialParticleSE')
    sgNodes_list.remove('initialShadingGroup')
    # <2>.通过材质的SG节点找到对应物体或者是面级别
row = 0
for index, sgNode in enumerate(sgNodes_list):
    colorChannel_str = 'color'
    coulmn = (index) / 10
    # 使用UDIM (Mari):UV 坐标使用公式 1000+(u+1+v*10)
    name = 1000 + (row + 1 + coulmn * 10)
    cmds.hyperShade(objects=sgNode)  # 返回值是直接选择物体，并非节点
    # <3>.通过SG节点重命名找到材质球所连接的贴图文件并保存
    materialNode = cmds.listConnections(sgNode + '.surfaceShader')
    fileNode = cmds.listConnections('%s.%s' % (materialNode[0], colorChannel_str), type='file')
    textureFile_str = cmds.getAttr("%s.fileTextureName" % fileNode[0])

    # 2.对于相同材质球的obj，进行UV同一象限排布，没有重叠
    # <1>.通过‘被选择的’物体找到并选中UV点
    selUVs = pm.polyListComponentConversion(tuv=1)
    cmds.select(selUVs, add=True)

    # <2>.挪动UV点到指定的区域
    cmds.polyEditUV(u=row, v=coulmn)

    # <3>.通过UV点的位置象限重命名该材质球所连接的贴图文件,命名遵循 <channel>.#.jpg
    fileName_str = colorChannel_str + '.' + str(name)
    # <4>.链接函数处理贴图文件。
    newPath = dealTexture(textureFile_str, fileName_str)
    # <5>.更改材质所链接贴图及uv Tiling Mode 为Mari格式。
    cmds.setAttr("%s.fileTextureName" % fileNode[0], newPath, type="string")
    cmds.setAttr('%s.uvTilingMode' % fileNode[0], 3)
    if row == 9:
        row = 0
    else:
        row += 1


# 4.处理贴图文件函数
def dealTexture(sourceTexture, textureName):
    fileName = os.path.basename(sourceTexture).split('.tif')[0]
    texturePath = sourceTexture.replace(fileName, textureName)
    shutil.copy(sourceTexture, texturePath)
    return texturePath
