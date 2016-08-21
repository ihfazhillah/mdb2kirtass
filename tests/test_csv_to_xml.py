import unittest
from lxml import etree
from io import StringIO
from lxml_asserts.testcase import LxmlTestCaseMixin

from mdb2kirtass.csv_to_xml import CsvtoXml


class CsvtoXmlTestCase(unittest.TestCase, LxmlTestCaseMixin):

    def original_csv_file(self):
        return StringIO("""bk,no,betaka,authno,cat
nama,1,ini buku bagus,1,3
munawir,2,kamus indo arab,2,4
sidu,3,kertas putih,4,3""".strip())


    def test_dapatkan_satu_baris_pertama(self):
        data = dict(bk='nama', no='1',
                    betaka='ini buku bagus', authno='1', cat='3')
        hasil = CsvtoXml(self.original_csv_file())
        self.assertEqual(data, list(hasil._dict_csv())[0])

    def test_buat_xml_file_dengan_tag_header_text_isi(self):
        """header csv adalah tag, dan isi adalah text tanpa
        ada perubahan nama"""
        hasil = CsvtoXml(self.original_csv_file())
        expected = """<item><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat>
        <bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat>
        <bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat>
        </item>"""
        self.assertXmlEqual(expected,
                    hasil._make_xml())

    def test_buat_xml_objek_dengan_tag_header_setiap_row_dengan_parent(self):
        """header csv adalah tag, setiap baris ada tag parent, dengan root
        adalah item, tanpa ada perubahan nama"""
        hasil = CsvtoXml(self.original_csv_file())._make_xml(parent='book')
        expected = """<item>
        <book><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_dengan_custom_root(self):
        """root selain item...."""
        hasil = CsvtoXml(self.original_csv_file())._make_xml(root='custom',
                                                                    parent='book')
        expected = """<custom>
        <book><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </custom>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_tapi_colom_tag_diubah_satu(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml(parent='book',
                col_name=[('bk', 'b')])
        expected = """<item>
        <book><b>nama</b><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><b>munawir</b><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><b>sidu</b><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_tapi_colom_tag_diubah_satu_dengan_tanpa_parent(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml(col_name=[('bk', 'b')])
        expected = """<item>
        <b>nama</b><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat>
        <b>munawir</b><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat>
        <b>sidu</b><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_make_xml_objek_dengan_header_sebagai_attrib(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml(tag='groupe',
                                                                as_attrib=True)
        expected = """<item>
        <groupe bk='nama' no='1' betaka='ini buku bagus' authno='1' cat='3'/>
        <groupe bk='munawir' no='2' betaka='kamus indo arab' authno='2' cat='4'/>
        <groupe bk='sidu' no='3' betaka='kertas putih' authno='4' cat='3'/>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_header_sebagai_attrib_dengan_diubah(self):
        """Beberapa attrib diubah"""
        hasil = CsvtoXml(self.original_csv_file())._make_xml(tag='groupe',
                                    col_name=[('bk', 'title')], as_attrib=True)
        expected = """<item>
        <groupe title='nama' no='1' betaka='ini buku bagus' authno='1' cat='3'/>
        <groupe title='munawir' no='2' betaka='kamus indo arab' authno='2' cat='4'/>
        <groupe title='sidu' no='3' betaka='kertas putih' authno='4' cat='3'/>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_header_sebagai_attrib_dipilih(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml(tag='groupe',
                        include=['bk', 'betaka'], col_name=[('bk', 'title')], as_attrib=True)
        expected = """<item>
        <groupe title='nama' betaka='ini buku bagus' />
        <groupe title='munawir'  betaka='kamus indo arab' />
        <groupe title='sidu'  betaka='kertas putih' />
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_update_xml_objek_header_attrib_parent_element_objek(self):
        xml = """<parent>
            <root id='1'/>
            <root id='2' />
        </parent>
        """
        p = etree.fromstring(xml)
        parent = p.findall('.//root')[0]
        csv = CsvtoXml(self.original_csv_file())
        hasil = csv._update_xml(tree_orig=p, tag='groupe', as_attrib=True, parent=parent)
        expected = """<parent>
        <root id='1'>
        <groupe bk='nama' no='1' betaka='ini buku bagus' authno='1' cat='3'/>
        <groupe bk='munawir' no='2' betaka='kamus indo arab' authno='2' cat='4'/>
        <groupe bk='sidu' no='3' betaka='kertas putih' authno='4' cat='3'/>
        </root>
        <root id='2'/>
        </parent>"""
        # self.fail(etree.tostring(hasil))
        self.assertXmlEqual(expected, hasil)

    def test_update_xml_objek_header_attrib_parent_element_objek_with_include(self):
        xml = """<parent>
            <root id='1'/>
            <root id='2' />
        </parent>
        """
        p = etree.fromstring(xml)
        parent = p.findall('.//root')[0]
        csv = CsvtoXml(self.original_csv_file())
        hasil = csv._update_xml(tree_orig=p, tag='groupe',
            as_attrib=True, parent=parent, include=['bk', 'no', 'betaka'])
        expected = """<parent>
        <root id='1'>
        <groupe bk='nama' no='1' betaka='ini buku bagus'/>
        <groupe bk='munawir' no='2' betaka='kamus indo arab' />
        <groupe bk='sidu' no='3' betaka='kertas putih'/>
        </root>
        <root id='2'/>
        </parent>"""
        # self.fail(etree.tostring(hasil))
        self.assertXmlEqual(expected, hasil)

    def test_update_xml_objek_header_attrib_parent_changed_element_objek_with_include(self):
        xml = """<parent>
            <root id='1'/>
            <root id='2' />
        </parent>
        """
        p = etree.fromstring(xml)
        parent = p.findall('.//root')[0]
        csv = CsvtoXml(self.original_csv_file())
        hasil = csv._update_xml(tree_orig=p, tag='groupe',
            as_attrib=True, parent=parent, include=['bk', 'no', 'betaka'],
            col_name=[('bk', 'name')])
        expected = """<parent>
        <root id='1'>
        <groupe name='nama' no='1' betaka='ini buku bagus'/>
        <groupe name='munawir' no='2' betaka='kamus indo arab' />
        <groupe name='sidu' no='3' betaka='kertas putih'/>
        </root>
        <root id='2'/>
        </parent>"""
        # self.fail(etree.tostring(hasil))
        self.assertXmlEqual(expected, hasil)

    def test_update_xml_objek_header_attrib_dengan_tambah_attrib(self):
        xml = """<parent>
            <root id='1'/>
            <root id='2' />
        </parent>
        """
        p = etree.fromstring(xml)
        parent = p.findall('.//root')[1]
        csv = CsvtoXml(self.original_csv_file())
        hasil = csv._update_xml(tree_orig=p, tag='groupe',
            as_attrib=True, parent=parent, include=['bk', 'no', 'betaka'],
            col_name=[('bk', 'name')],
            cus_attr=({'c':str(x)} for x in range(3)))
        expected = """<parent>
        <root id='1' />
        <root id='2'>
        <groupe name='nama' no='1' betaka='ini buku bagus' c='0'/>
        <groupe name='munawir' no='2' betaka='kamus indo arab' c='1'/>
        <groupe name='sidu' no='3' betaka='kertas putih' c='2'/>
        </root>
        </parent>"""
        # self.fail(etree.tostring(hasil))
        self.assertXmlEqual(expected, hasil)

    def test_update_xml_objek_header_attrib_value_diganti(self):
        """value dari attribut suatu tag adalah key dari sebuah dictionary,
        dan akan diganti dengan value yang sesuai.

        contoh value adalah : '1', '2', '3'
        dan sebuah dictionary adalah : {'1': 'kamu', '2': 'aku', '3': 'dia'}

        maka ketika value dari atribut sebuah tag adalah 1, maka akan diganti
        menjadi 'kamu'
        """
        D = {1: 'bagus',
             2: 'anang',
             4: 'adit'}

        xml = """<parent>
            <root id='1'/>
            <root id='2' />
        </parent>
        """
        p = etree.fromstring(xml)
        parent = p.findall('.//root')[0]
        csv = CsvtoXml(self.original_csv_file())
        hasil = csv._update_xml(tree_orig=p,
                                tag='groupe',
                                as_attrib=True,
                                parent=parent,
                                change_val=[('authno', D)])
        expected = """<parent>
        <root id='1'>
        <groupe bk='nama' no='1' betaka='ini buku bagus' authno='bagus' cat='3'/>
        <groupe bk='munawir' no='2' betaka='kamus indo arab' authno='anang' cat='4'/>
        <groupe bk='sidu' no='3' betaka='kertas putih' authno='adit' cat='3'/>
        </root>
        <root id='2'/>
        </parent>"""
        # self.fail(etree.tostring(hasil))
        self.assertXmlEqual(expected, hasil)
