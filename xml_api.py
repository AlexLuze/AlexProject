#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
This module is an API for writing and reading xml file.
Here are the functions in the module:
    xml_write(): Writing the dictionary information obtained from the material_api file to the XML file.
    xml_read(): Read the XML file information,
                save as the corresponding parameter,
                and to create a material sphere to the corresponding geometries.
"""
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import material_api as mat_dev_api


def xml_write(xml_file_path):
    """
    Writing the dictionary information obtained from the material_lookdev_api file to the XML file.
    :param str xml_file_path: The absolute path to the xml.
    :return: True
    :rtype: bool
    """

    # Get the material sphere information of the current scene in Maya and return it in dictionary format.
    relationship_information_list = mat_dev_api.get_information_for_relationship()

    root = Document()
    xml_file = open(xml_file_path, 'w')

    relationship = root.createElement('relationship')
    root.appendChild(relationship)
    for information in relationship_information_list['material']:

        # Read the information in the dictionary and save it.
        material_name = information['material_name']
        material_type = information['material_type']
        sg_node = information['sg_node_name']
        obj_info_list = information['objects']
        tex_info = information['texture']

        # Create the corresponding element information in the XML file.
        material_xml = root.createElement('material')
        material_xml.setAttribute('material_name', material_name)
        relationship.appendChild(material_xml)

        material_type_xml = root.createElement('material_type')
        material_type_xml.appendChild(root.createTextNode(material_type))
        material_xml.appendChild(material_type_xml)

        sg_node_xml = root.createElement('sg_node_name')
        sg_node_xml.appendChild(root.createTextNode(sg_node))
        material_xml.appendChild(sg_node_xml)

        texture_xml = root.createElement('texture_file')
        texture_xml.appendChild(root.createTextNode(tex_info))
        material_xml.appendChild(texture_xml)

        for obj_info in obj_info_list:
            obj = root.createElement("objects")
            material_xml.appendChild(obj)
            obj.setAttribute('object', obj_info)

    xml_file.write(root.toprettyxml(indent="    "))
    xml_file.close()

    return True


def xml_read(xml_file_path):
    """
    Read the XML file information,
    save as the corresponding parameter,
    and to create a material sphere to the corresponding geometries.
    :param str xml_file_path: The absolute path of the XML file to be read.
    :return: True
    :rtype: bool
    """
    dom = parse(xml_file_path)
    root = dom.documentElement
    materials = root.getElementsByTagName("material")

    for material in materials:

        objects_list = []

        mat_name = material.getAttribute("material_name")

        mat_type = material.getElementsByTagName('material_type')[0]
        material_type = mat_type.childNodes[0].data

        sg_node = material.getElementsByTagName('sg_node_name')[0]
        sg_node_name = sg_node.childNodes[0].data

        texture_file = material.getElementsByTagName('texture_file')[0]
        file_path = texture_file.childNodes[0].data

        objects_xml_list = material.getElementsByTagName('objects')

        for obj in objects_xml_list:
            object_poly = obj.getAttribute('object')
            objects_list.append(object_poly)

        # Create a texture sphere and apply it to the geometries.
        mat_dev_api.create_material_node(mat_name, material_type, sg_node_name, file_path, objects_list)
    return True
