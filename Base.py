#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from maya import cmds
import pymel.core as pm

# 1.通过材质球的SG节点找到对应obj信息
# <1>.查找场景中的所有SG节点并保存列表sgNodesList中
sgNodesList = cmds.ls(type='shadingEngine')
if 'initialParticleSE' in sgNodesList or 'initialShadingGroup' in sgNodesList:
    sgNodesList.remove('initialParticleSE')
    sgNodesList.remove('initialShadingGroup')
    # <2>.通过材质的SG节点找到对应物体或者是面级别
row = 0
for index, sgNode in enumerate(sgNodesList):
    colorChannel = 'color'
    coulmn = (index) / 10
    print "row+1+coulmn*10", row + 1 + coulmn * 10 + 1000
    if row == 10:
        row = 0
    print "%s-->%s-->%s" % (row, coulmn, sgNode)
    row += 1
    cmds.hyperShade(objects=sgNode)  # 返回值是直接选择物体，并非节点

    # <3>.通过SG节点重命名找到材质球所连接的贴图文件并保存
    materialNode = cmds.listConnections(sgNode + '.surfaceShader')
    print "materialNode:", materialNode

    fileNode = cmds.listConnections('%s.%s' % (materialNode[0], colorChannel), type='file')
    currentFile = cmds.getAttr("%s.fileTextureName" % fileNode[0])
    print "currentFile:", currentFile

    # 2.对于相同材质球的obj，进行UV同一象限排布，没有重叠
    # <1>.通过‘被选择的’物体找到UV点
    selUVs = pm.polyListComponentConversion(tuv=1)
    print 'selUVs:', selUVs
    # 选中UV点
    cmds.select(selUVs, add=True)

    # <2>.通过挪动UV点到指定的区域
    # cmds.polyEditUV(u=5,v=5)
    cmds.polyEditUV(u=row, v=coulmn)

    # <3>.通过UV点的位置象限重命名该材质球所连接的贴图文件,命名遵循 <channel>.#.jpg
    # (1).链接函数处理贴图文件
    if row + 1 == 10:
        name = str(coulmn + 1) + '0'
    else:
        # print "dealTexture-->%s--->%s" %(coulmn,row+1)
        name = str(coulmn) + str(row + 1)
    channelName = colorChannel + '.10' + name
    print "%s----->" % channelName
    newPath = dealTexture(currentFile, channelName)
    # cmds.setAttr(materialNode[0]+'_AlbedoMapFile.fileTextureName',newPath,type = "string")
    cmds.setAttr("%s.fileTextureName" % fileNode[0], newPath, type="string")

    row += 1


# 4.处理贴图文件函数
def dealTexture(filePath, channelName):
    print "filePath:", filePath
    # print "channelName:",channelName
    fileName = os.path.basename(filePath).split('.tif')[0]
    print "fileName:", fileName
    texturePath = filePath.replace(fileName, channelName)
    print "finnaly path:", texturePath
    # os.rename(filePath,texturePath)
    shutil.copy(filePath, texturePath)
    return texturePath

