from lxml import etree


def add_item(tree, root_id, item_name, item_id):
    tree = etree.parse(tree)
    root = tree.find(".//root[@id='{}']".format(root_id))
    etree.SubElement(root, 'Item', {'Name': item_name,
                    'id': item_id})

    return tree
