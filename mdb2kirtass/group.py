from lxml import etree
import csv

from mdb2kirtass.csv_to_xml import CsvtoXml

class MakeGroup():

    def add_root(self, tree):
        root = tree.xpath(".//root[starts-with(@id, 'sb')]")
        if len(root) >= 1:
            count = len(root)
            id_ = 'sb%s' %(count)
            name = 'كتب الشاملة%s' %(count)
            etree.SubElement(tree, "root", {"Name": name, 'id': id_})
        else:
            etree.SubElement(tree, "root",
            {'Name': 'كتب الشاملة', 'id': 'sb'})

        return tree

    def add_item(self, tree, csvobject):
        csv = CsvtoXml(csvobject)
        root = tree.xpath(".//root[starts-with(@id, 'sb')]")[-1]
        tree = csv._update_xml(tree_orig=tree, as_attrib=True, parent=root,
            tag='Item', include=['id', 'name'], col_name=[('name', 'Name')])
        return tree

    def _auth_dict(self, csv_file):
        csvread = csv.DictReader(csv_file)
        return {int(x['authid']): x['Lng'] for x in csvread}
