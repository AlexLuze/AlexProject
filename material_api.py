#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
This module is an API for importing and exporting Maya material.
It contains some functions that can be used in the current project.
Here are the functions in the module:
    maya_main_window(): Instantiate the Maya main window with the OpenMayaUI module.
    get_workspace(): Gets the workspace for the current project in Maya.
    get_sg_nodes(): Get all SG nodes in the current scene.
    get_information_for_relationship(): get the information relationship of all the material nodes in the scene.
    create_material_node(): Create a material sphere node and assign the material sphere.
    create_texture_node(): Create a texture file node and return the value of the file node name.
    create_place_texture(): Create a place 2d texture.
"""
import os
from maya import cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Instantiate the Maya main window with the OpenMayaUI module.
    :return: main_window
    :rtype: QWidget
    """
    main_window = omui.MQtUtil.mainWindow()
    return main_window


def get_workspace():
    """
    Gets the workspace for the current project in Maya.
    :return: workspace
    :rtype: unicode
    """
    workspace = cmds.workspace(q=True, rd=True)

    return workspace


def get_sg_nodes():
    """
    Get all SG nodes in the current scene in the XML export process.
    (Note:excluding the default two nodes,'initialParticleSE' and 'initialShadingGroup')
    :return: sg_nodes_list
    :rtype: list
    """
    sg_nodes_list = cmds.ls(type='shadingEngine')
    if 'initialParticleSE' in sg_nodes_list or 'initialShadingGroup' in sg_nodes_list:
        sg_nodes_list.remove('initialParticleSE')
        sg_nodes_list.remove('initialShadingGroup')

    return sg_nodes_list


def get_information_for_relationship():
    """
    In the process of XML export,
    get the information relationship of all the material nodes in the scene.
    Returns the data structure, for example:
    {'material': [{'material_name': 'material_name',
                   'material_type': 'material_type',
                   'objects': ['object1',
                               'object2',
                               ...]
                   'sg_node_name': 'sg_node_name',
                   'texture': 'texture_path'},]
                   }
    :return: all_info_dic
    :rtype: dict
    """
    all_info_dic = {}
    all_info_list = []
    sg_nodes_list = get_sg_nodes()

    for sg_node in sg_nodes_list:
        base_info_dic = {}

        # Gets the name and type of the material sphere
        material_name = cmds.listConnections('{}.surfaceShader'.format(sg_node))
        material_type = cmds.nodeType(material_name)

        # Gets the texture information associated with the material sphere
        file_node = cmds.listConnections('{}.color'.format(material_name[0]), type='file')
        current_file = cmds.getAttr("{}.fileTextureName".format(file_node[0]))

        # Gets the model information (shape or face id) associated with the material sphere
        cmds.hyperShade(objects=sg_node)
        corresponding_face_id = cmds.ls(sl=True)

        base_info_dic['material_name'] = material_name[0]
        base_info_dic['material_type'] = material_type
        base_info_dic['sg_node_name'] = sg_node
        base_info_dic['texture'] = current_file
        base_info_dic['objects'] = corresponding_face_id

        all_info_list.append(base_info_dic)

    all_info_dic['material'] = all_info_list

    return all_info_dic


def create_material_node(mat_name, mat_type, sg_node, texture_file_path, corresponding_model):
    """
    Create a material sphere node and
    assign the material sphere to the corresponding the model(shape or face id) for import.
    :param str mat_name: The name of the material,specifies the name used to create the material.
    :param str mat_type: The type of the material,creates a material sphere of the specified type.
    :param str sg_node: Name of SG node connected by material,
                        used to specify the name of the SG node created.
    :param str texture_file_path: The full path of the texture file.
    :param list corresponding_model: The material is exported with a list of corresponding geometry names.
    :return: True
    :rtype: bool
    """
    file_format = os.path.splitext(texture_file_path)[-1]
    file_node_name = os.path.basename(texture_file_path).split(file_format)[0]

    mat_node = cmds.shadingNode(mat_type, asShader=True, name=mat_name)
    cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_node)
    cmds.connectAttr('{}.outColor'.format(mat_node), '{}.surfaceShader'.format(sg_node), f=True)

    texture_file_node = create_texture_node(texture_file_path)
    cmds.connectAttr('{}.outColor'.format(texture_file_node), '{}.color'.format(mat_node), f=True)

    cmds.sets(corresponding_model, e=True, forceElement=sg_node)

    return True


def create_texture_node(texture_file_path):
    """
    Create a texture file node and return the value of the file node name
    :param str texture_file_path: The full path of the texture file.
    :return: file_node
    :rtype: unicode
    """
    file_format = os.path.splitext(texture_file_path)[-1]
    file_node_name = os.path.basename(texture_file_path).split(file_format)[0]
    file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=file_node_name)
    cmds.setAttr('{}.fileTextureName'.format(file_node), texture_file_path, type="string")
    create_place_texture(file_node)

    return file_node


def create_place_texture(file_node):
    """
    Create a place 2d texture.
    :param str file_node: Created file node.
    :return: True
    :rtype: bool
    """
    place_texture = cmds.shadingNode('place2dTexture', asUtility=True)
    connections = ['rotateUV', 'offset', 'noiseUV', 'vertexCameraOne',
                   'vertexUvThree', 'vertexUvTwo', 'vertexUvOne', 'repeatUV', 'wrapV', 'wrapU',
                   'stagger', 'mirrorU', 'mirrorV', 'rotateFrame', 'translateFrame', 'coverage']

    cmds.connectAttr('{}.outUV'.format(place_texture), '{}.uvCoord'.format(file_node))
    cmds.connectAttr('{}.outUvFilterSize'.format(place_texture), '{}.uvFilterSize'.format(file_node))

    for connection in connections:
        cmds.connectAttr('{}.{}'.format(place_texture, connection), '{}.{}'.format(file_node, connection))

    return True
