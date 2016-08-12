from lxml import etree


def add_root(original, name_id):
    """Menambahkan root dari xml objek berupa original, dengan
    data name_id yang berupa dictionary objek
        name = nama
        id = id root

    contoh mau menambahkan root bernama shamela_book dengan id bs1
    >> add_root(original, {'name':'shamela_book', 'id':'bs1'})
    """

    tree = etree.parse(original)
    setting = tree.getroot()
    root = setting.find('.//root')
    if not tree.find('.//root[Name="{}"]'.format(name_id['name'])):
        new = etree.SubElement(setting, 'root', {'name': name_id['name'],
                                                'id':name_id['id']})

    return new
