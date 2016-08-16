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

    def _make_xml_original(self, root='item', parent=None, col_name=None,
                            as_attrib=False, tag=None):
        item = etree.Element(root)
        for row in self._dict_csv():
            if tag is None:
                if parent is None:
                    if col_name is None:
                        self._make_tag_with_parent_from_row(row, item)
                    else:
                        self._make_tag_and_rename_it_inside_parent_from_row(row,
                                                                     item, col_name)
                else:
                    p = etree.SubElement(item, parent)
                    if col_name is None:
                        self._make_tag_with_parent_from_row(row, p)
                    else:
                        self._make_tag_and_rename_it_inside_parent_from_row(row,
                                                        p, col_name)
            else:
                attrib = {k:row[k] for k in row}
                etree.SubElement(item, tag, attrib)
                
        return item

    def _make_tag_with_parent_from_row(self, row, parent, as_attrib=False):
        """Membuat tag, didalam parent yang ditentukan oleh *parent*
        dari *row* csv, DictReader objek"""
        for col in row:
            t = etree.SubElement(parent, col)
            t.text = row[col]

    def _make_tag_and_rename_it_inside_parent_from_row(self, row,
                                                       parent, col_name):
        """membuat tag, dengan nama yang diubah, didalam row objek DictReader,
        col_name adalah list/tuple di dalam list/atau tuple, index 0 adalah
        asli, index 1 adalah setelah diubah"""

        for col in row:
            for cn in col_name:
                if col == cn[0]:
                    col = cn
                else:
                    col = (col, col)
            t = etree.SubElement(parent, col[1])
            t.text = row[col[0]]
