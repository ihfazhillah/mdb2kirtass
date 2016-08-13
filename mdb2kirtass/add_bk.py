from lxml import etree


def add_bk(tree, bkid, item_id, name, aut, betaka):
    tree = etree.parse(tree)
    item = tree.find(".//Item[@id='{}']".format(item_id))
    etree.SubElement(item, 'bk', {'name': name,
                                  'id': bkid,
                                  'aut': aut,
                                  'betaka' : betaka})
    return tree
