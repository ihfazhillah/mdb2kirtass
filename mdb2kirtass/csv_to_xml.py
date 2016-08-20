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

    def _update_xml(self, tree_orig, tag, as_attrib, parent, include=None):
        for row in self._dict_csv():
            if include:
                row = self._process_include(row, include)

            if as_attrib:
                self._header_as_attrib(row, parent, tag)
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


    def _header_as_attrib(self, row, item, tag, col_name=None):
        """Menjadikan header csv sebagai attribut sebuah tag yang ditentukan
        dengan item adalah root """

        if col_name:
            self._change_col_name(row, col_name)

        attrib = {k:row[k] for k in row}
        return etree.SubElement(item, tag, attrib)
