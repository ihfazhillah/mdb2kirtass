from lxml import etree


class MakeGroup():

    def add_root(self, tree):
        root = tree.find(".//root[@id='sb']")
        if root:
            pass
        else:
            etree.SubElement(tree, "root",
            {'Name': 'كتب الشاملة', 'id': 'sb'})

        return tree
