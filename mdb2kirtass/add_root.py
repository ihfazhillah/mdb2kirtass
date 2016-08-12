from lxml import etree


def add_root(original, name):
    """Menambahkan root dari xml objek berupa original, dengan
    data name_id yang berupa dictionary objek
        name = nama
        id = id root

    contoh mau menambahkan root bernama shamela_book dengan id bs1
    >> add_root(original, {'name':'shamela_book', 'id':'bs1'})
    """

    tree = etree.parse(original)
    setting = tree.getroot()
    root = root = tree.find('.//root[@Name="{}"]'.format(name))
    if root is not None:
        root_len = len(root)
        id_ = root_len + 1
        new = etree.SubElement(setting, 'root', {'name': name,
                                                'id': str(id_)})
    else:
        new = etree.SubElement(setting, 'root', {'name': name,
        'id':'0'})

    return tree
