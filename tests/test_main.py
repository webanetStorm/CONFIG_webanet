import unittest
from unittest.mock import patch
from main import VirtualShell


class TestVirtualShell(unittest.TestCase):

    def setUp(self):
        self.shell = VirtualShell()

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_log(self, mock_write):
        self.shell.log('test command')
        self.assertEqual(self.shell.log_element[0].text, 'test command')
        mock_write.assert_called_once_with(self.shell.log_path)

    @patch('main.print')
    def test_ls(self, mock_print):
        self.shell.ls(['dir1', 'dir2', 'file1', 'file2'])
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('dir2')
        mock_print.assert_any_call('file1')
        mock_print.assert_any_call('file2')

    @patch('main.print')
    def test_tree(self, mock_print):
        self.shell.tree(['dir1', 'dir1/dir2', 'dir1/dir2/file1', 'dir1', 'dir1/file2'])
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('    dir2')
        mock_print.assert_any_call('        file1')
        mock_print.assert_any_call('    file2')

    @patch('main.print')
    def test_find(self, mock_print):
        directory = ['dir1/dir2/file1', 'dir1/file2']
        self.shell.find(directory, 'file')
        mock_print.assert_any_call('dir1/dir2/file1')
        mock_print.assert_any_call('dir1/file2')


if __name__ == '__main__':
    unittest.main()
