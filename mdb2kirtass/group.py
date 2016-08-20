from lxml import etree


class MakeGroup():

    def add_root(self, tree):
        root = [x for x in tree.findall(".//root") if x.attrib['id'].startswith('sb')]
        if len(root) >= 1:
            count = len(root)
            id_ = 'sb%s' %(count)
            name = 'كتب الشاملة%s' %(count)
            etree.SubElement(tree, "root", {"Name": name, 'id': id_})
        else:
            etree.SubElement(tree, "root",
            {'Name': 'كتب الشاملة', 'id': 'sb'})

        return tree
