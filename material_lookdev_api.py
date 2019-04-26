#!/usr/bin/env python
# -*- coding:utf-8 -*-
from maya import cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return main_window


def get_workspace():
    workspace = cmds.workspace(q=True, rd=True)

    return workspace


# Export

def get_sg_nodes():
    sg_nodes_list = cmds.ls(type='shadingEngine')
    if 'initialParticleSE' in sg_nodes_list or 'initialShadingGroup' in sg_nodes_list:
        sg_nodes_list.remove('initialParticleSE')
        sg_nodes_list.remove('initialShadingGroup')

    return sg_nodes_list


def get_infomation_for_relationship():
    all_info_dic = {}
    all_info_list = []

    sg_nodes_list = get_sg_nodes()

    for sg_node in sg_nodes_list:
        # material_dic = {}
        base_info_dic = {}

        # 获取材质球名字和类型
        material_name = cmds.listConnections('{}.surfaceShader'.format(sg_node))
        material_type = cmds.nodeType(material_name)

        # 获取与材质球相连的贴图信息
        fileNode = cmds.listConnections('{}.color'.format(material_name[0]), type='file')
        current_file = cmds.getAttr("{}.fileTextureName".format(fileNode[0]))

        # 获取与材质球相连的模型信息
        cmds.hyperShade(objects=sg_node)
        corresponding_face_id = cmds.ls(sl=True)

        base_info_dic['material_name'] = material_name[0]
        base_info_dic['material_type'] = material_type
        base_info_dic['sg_node_name'] = sg_node
        base_info_dic['texture'] = current_file
        base_info_dic['objects'] = corresponding_face_id

        # material_dic[material_name[0]] = base_info_dic
        all_info_list.append(base_info_dic)

    all_info_dic['material'] = all_info_list
    return all_info_dic


# import pprint

# relationship_infomations_list = get_infomation_for_relationship()
# print len(relationship_infomations_list['material'])

# pprint.pprint(get_infomation_for_relationship())
# 3.将以上的两种对应关系整理成：
'''
{
    material:
        [
            {
                '材质球1名字':
                    {
                        'sg_node_name':'对应的SG节点的名字'
                        'texture':'color通道贴图路径',
                        'objects':'对应的obj物体或面级别'
                    }
            },
            {
                '材质球2名字':
                    {
                        'sg_node_name':'对应的SG节点的名字'
                        'texture':'color通道贴图路径',
                        'objects':'对应的obj物体或面级别'
                    }
            }
            ]
        }
'''


# Import
# 创建材质节点，返回值为材质节点名
def create_material_node(mat_name, mat_type, sg_node, texture_file_path, corresponding_model):
    file_node_name = os.path.basename(texture_file_path).split(file_format)[0]

    mat_node = cmds.shadingNode(mat_type, asShader=True, name=mat_name)
    cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_node)
    cmds.connectAttr('{}.outColor'.format(mat_node), '{}.surfaceShader'.format(sg_node), f=True)

    texture_file_node = create_texture_node(texture_file_path)
    cmds.connectAttr('{}.outColor'.format(texture_file_node), '{}.color'.format(mat_node), f=True)

    cmds.sets(corresponding_model, e=True, forceElement=sg_node)

    return True


# 创建texture file节点，返回值为file节点名
def create_texture_node(texture_file_path):
    file_format = os.path.splitext(texture_file_path)[-1]
    file_node_name = os.path.basename(texture_file_path).split(file_format)[0]
    file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=file_node_name)
    cmds.setAttr('{}.fileTextureName'.format(file_node), texture_file_path, type="string")

    return file_node


