from xml.dom.minidom import Document
doc = Document()

infos = {'material':
             [
                 {
                     'mat1':
                         [
                             {'texture': "C:/base01.jpg"},
                             {'obj': [u'pCube1.f[0:5]',u'pCube1.f[6:26]']}

                         ]
                 },
                 {
                     "mat2":
                         [
                            {'texture': "C:/base02.jpg"},
                            {'obj': [u'pCube1.f[88:156]',u'pCube1.f[589:723]']}
                         ]
                 }
             ]
}

relationship = doc.createElement("relationship")
doc.appendChild(relationship)

material1 = doc.createElement('material')
relationship.appendChild(material1)

# material_name = doc.createTextNode("mat1")
# material.appendChild(material_name)

material1.setAttribute('material_name',"mat1")

file_path1 = doc.createElement("file_path")
material1.appendChild(file_path1)

path_name = doc.createTextNode("C:/base.jpg")
file_path1.appendChild(path_name)

obj1 = doc.createElement("obj")
material1.appendChild(obj1)

obj_name1 = doc.createTextNode("polySphere")
obj1.appendChild(obj_name1)

filename = "E:/BaseFX_maya_test_20190411/base.xml"
f = open(filename, "w")
f.write(doc.toprettyxml(indent="  "))
f.close()
