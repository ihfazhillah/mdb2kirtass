from lxml import etree
import csv

class CsvtoXml(object):
    """Class untuk mengubah file csv ke file xml
    berdasarkan nama kolom....


    csv_file : file csv, atau yang semisal dengan file (dengan StringIO)?
    """

    def __init__(self, csv_file):
        self.csv_file = csv_file


    def _dict_csv(self):
        """Fungsi untuk mengubah file csv ke objek DictCsvReader"""
        return csv.DictReader(self.csv_file)

    def _make_xml(self, root='item', parent=None, col_name=None, include=None,
                            as_attrib=False, tag=None):
        item = etree.Element(root)
        for row in self._dict_csv():
            if include:
                row = self._process_include(row, include)

            if tag is None and as_attrib is False:
                if parent is None:
                    self._header_as_tag(row, item, col_name)
                else:
                    p = etree.SubElement(item, parent)
                    self._header_as_tag(row, p, col_name)
            else:
                self._header_as_attrib(row, item, tag, col_name)

        return item

    def _update_xml(self, tree_orig, tag, as_attrib, parent, include=None,
                    col_name=None, cus_attr=None,
                    change_val=None):

        if cus_attr:
            for row, ca in zip(self._dict_csv(), cus_attr):
                if include:
                    row = self._process_include(row, include)

                if as_attrib:
                    self._header_as_attrib(row, parent, tag, col_name, ca)
        else:
            for row in self._dict_csv():
                if include:
                    row = self._process_include(row, include)

                if as_attrib:
                    self._header_as_attrib(row, parent, tag, col_name, change_val=change_val)
        return tree_orig

    def _header_as_tag(self, row, parent, col_name):
        """Membuat tag, didalam parent yang ditentukan oleh *parent*
        dari *row* csv, DictReader objek"""
        if col_name:
            self._change_col_name(row, col_name)

        for col in row:
            t = etree.SubElement(parent, col)
            t.text = row[col]

    def _change_col_name(self, row, col_name):
        """http://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary"""

        for c in col_name:
            row[c[1]] = row.pop(c[0])

        return row

    def _process_include(self, row, include):
        return {key:row[key] for key in row if key in include}


    def _header_as_attrib(self, row, item, tag,
                          col_name=None, cus_attr=None,
                          change_val=None):
        """Menjadikan header csv sebagai attribut sebuah tag yang ditentukan
        dengan item adalah root """

        if change_val:
            self._change_val(row, change_val)
        if col_name:
            self._change_col_name(row, col_name)

        attrib = {k:row[k] for k in row}

        if cus_attr:
            attrib.update(cus_attr)

        etree.SubElement(item, tag, attrib)

    def _change_val(self, row, change_val):
        """chage_val harus berupa list didalam list, atau tuple didalam list,
        contohnya adalah = [('authno', D)]
        setiap list/tuple yang didalam harus hanya berjumlah 2.
        index 0 adalah nama key dari row yang akan diganti valuenya.
        index 1 adalah value dari value dari yang pertama.

        dari data seperti ini:

        dict_data = {1: 'abi',
             2: 'saya',
             3: 'kamu'}

        asli = [{'nama':'ihfazh', 'status':'1'},
                {'nama':'sakin', 'status':'2'},
                {'nama':'fufu', 'status':'3'},
                {'nama':'mumu', 'status':'1'},
                {'nama':'maryam', 'status':'2'}]

        expected = \"\"\"<root>
        <data nama='ihfazh' status='abi' />
        <data nama='sakin' status='saya' />
        <data nama='fufu' status='kamu' />
        <data nama='mumu' status='abi' />
        <data nama='maryam' status='saya' />
        </root>\"\"\"
        """
        for v in change_val:
            row[v[0]] = v[1].get(int(row[v[0]]), '')

        return row
