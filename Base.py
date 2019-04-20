#!/usr/bin/env python
# -*- coding:utf-8 -*-
from maya import cmds
import pymel.core as pm

# 1.通过材质球的SG节点找到对应obj信息
# <1>.查找场景中的所有SG节点并保存列表sgNodesList中
sgNodesList = cmds.ls(type='shadingEngine')
if 'initialParticleSE' in sgNodesList or 'initialShadingGroup' in sgNodesList:
    sgNodesList.remove('initialParticleSE')
    sgNodesList.remove('initialShadingGroup')

    # <2>.通过材质的SG节点找到对应物体或者是面级别
coulmn = 0
for index, sgNode in enumerate(sgNodesList):
    row = (index) / 10
    if coulmn == 10:
        coulmn = 0
    print "%s-->%s-->%s" % (row, coulmn, sgNode)
    coulmn += 1
    # cmds.hyperShade(objects = sgNode)  # 返回值是直接选择物体，并非节点

    # <3>.通过SG节点重命名找到材质球所连接的贴图文件并保存
    materialNode = cmds.listConnections(sgNode + '.surfaceShader')
    print "materialNode:", materialNode

    fileNode = cmds.listConnections('%s.color' % (materialNode[0]), type='file')
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
    # (1).链接函数处理贴图文件
    dealTexture(currentFile, row, coulmn)
    # coulmn += 1

    # <3>.通过UV点的位置象限重命名该材质球所连接的贴图文件


# 3.根据UV象限的序号修改材质球所连得贴图文件命名，命名遵循 <channel>.#.jpg


# 4.处理贴图文件函数
def dealTexture(texturePath, row, coulmn):
    print "dealTexture-->%s--->%s" % (row, coulmn)

