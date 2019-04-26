import sys

sys.path.append(r'C:/Users/benja/Documents/maya/2018/scripts/base_test_2/')
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import xml.dom.minidom
import material_lookdev_api as mat_dev_api


# xml_file_path = "C:/Users/benja/Documents/maya/2018/scripts/base_test_2/base003.xml"
def xml_write(xml_file_path):
    relationship_infomations_list = mat_dev_api.get_infomation_for_relationship()
    # pprint.pprint(relationship_infomations_list)
    root = Document()
    f = open(xml_file_path, 'w')

    relationship = root.createElement('relationship')
    root.appendChild(relationship)
    # print len(relationship_infomations_list['material'])
    # print type(relationship_infomations_list['material'])
    for info_dic in relationship_infomations_list['material']:
        # print "info_dic:",info_dic

        material_name = info_dic['material_name']
        material_type = info_dic['material_type']
        # print "material_type:",material_type
        sg_node = info_dic['sg_node_name']
        obj_info_list = info_dic['objects']
        tex_info = info_dic['texture']

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
            # obj.appendChild(root.createTextNode(obj_info))
            obj.setAttribute('object', obj_info)
        # break
    f.write(root.toprettyxml(indent="    "))
    f.close()

    return True


# r'C:\Users\benja\Documents\maya\2018\scripts\base_test_2/base002.xml'
def read_xml(xml_file_path):
    objects_list = []

    dom = xml.dom.minidom.parse(xml_file_path)

    root = dom.documentElement

    materials = root.getElementsByTagName("material")
    print "materials:", materials

    for material in materials:
        mat_name = material.getAttribute("material_name")
        print "mat_name:", mat_name

        mat_type = material.getElementsByTagName('material_type')[0]
        material_type = mat_type.childNodes[0].data
        print "material_type:", material_type

        sg_node = material.getElementsByTagName('sg_node_name')[0]
        sg_node_name = sg_node.childNodes[0].data
        print "sg_node_name:", sg_node_name

        texture_file = material.getElementsByTagName('texture_file')[0]
        file_path = texture_file.childNodes[0].data
        print "file_path:", file_path

        objects_xml_list = material.getElementsByTagName('objects')

        for obj in objects_xml_list:
            object_poly = obj.getAttribute('object')
            objects_list.append(object_poly)
        print "objects_list:", objects_list

        mat_dev_api.create_material_node(mat_name, material_type, sg_node_name, file_path, corresponding_model)

# ren = read_xml(xml_file_path)