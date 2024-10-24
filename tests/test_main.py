import unittest
from unittest.mock import patch, MagicMock
from main import VirtualShell


class TestVirtualShell(unittest.TestCase):

    def setUp(self):
        self.shell = VirtualShell('../webanet.tar', '../log.xml')

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_log(self, mock_write):
        self.shell.log('test command')
        self.assertEqual(self.shell.log_element[0].text, 'test command')
        mock_write.assert_called_once_with(self.shell.log_path)

    @patch('main.print')
    def test_ls_root(self, mock_print):
        self.shell.ls(['dir1', 'dir2', 'file1', 'file2'], None)
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('dir2')
        mock_print.assert_any_call('file1')
        mock_print.assert_any_call('file2')

    @patch('main.print')
    def test_ls_in_directory(self, mock_print):
        self.shell.ls(['dir1/file1', 'dir1/file2'], 'dir1')
        mock_print.assert_any_call('file1')
        mock_print.assert_any_call('file2')

    @patch('main.print')
    def test_ls_no_files(self, mock_print):
        self.shell.ls([], 'dir1')
        mock_print.assert_not_called()

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_cd_root(self, mock_write):
        self.shell.cd('/', ['dir1', 'dir2'])
        self.assertEqual(self.shell.current_path, '')

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_cd_parent_directory(self, mock_write):
        self.shell.current_path = 'dir1/dir2'
        self.shell.cd('..', ['dir1', 'dir2'])
        self.assertEqual(self.shell.current_path, 'dir1')

    @patch('main.print')
    def test_cd_nonexistent_directory(self, mock_print):
        self.shell.cd('dir3', ['dir1', 'dir2'])
        mock_print.assert_any_call('\033[31mcd : Не удается найти путь "/dir3", так как он не существует\033[0m')

    @patch('main.print')
    @patch('tarfile.TarFile.getmember')
    def test_du_single_file(self, mock_getmember, mock_print):
        mock_getmember.return_value.size = 28
        self.shell.du(['etc/config.conf'], 'etc')
        mock_print.assert_any_call('28 байт')

    @patch('main.print')
    @patch('tarfile.TarFile.getmember')
    def test_du_single_file(self, mock_getmember, mock_print):
        mock_getmember.return_value.size = 28
        self.shell.du(['etc/config.conf'], 'etc/config.conf')
        mock_print.assert_any_call('28 байт')

    @patch('main.print')
    @patch('tarfile.TarFile.getmember')
    def test_du_no_files(self, mock_getmember, mock_print):
        mock_getmember.side_effect = KeyError
        self.shell.du([], '.')
        mock_print.assert_any_call('0 байт')

    @patch('main.print')
    def test_tree_basic(self, mock_print):
        self.shell.tree(['dir1', 'dir1/dir2', 'dir1/file1'])
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('    dir2')
        mock_print.assert_any_call('    file1')

    @patch('main.print')
    def test_tree_empty(self, mock_print):
        self.shell.tree([])
        mock_print.assert_not_called()

    @patch('main.print')
    def test_tree_deep_structure(self, mock_print):
        self.shell.tree(['dir1', 'dir1/dir2', 'dir1/dir2/dir3', 'dir1/dir2/dir3/file1'])
        mock_print.assert_any_call('dir1')
        mock_print.assert_any_call('    dir2')
        mock_print.assert_any_call('        dir3')
        mock_print.assert_any_call('            file1')

    @patch('main.print')
    def test_find_existing_file(self, mock_print):
        directory = ['dir1/dir2/file1', 'dir1/file2']
        self.shell.find(directory, 'file1')
        mock_print.assert_any_call('dir1/dir2/file1')

    @patch('main.print')
    def test_find_no_match(self, mock_print):
        directory = ['dir1/dir2/file1', 'dir1/file2']
        self.shell.find(directory, 'file3')
        mock_print.assert_not_called()

    @patch('main.print')
    def test_find_multiple_matches(self, mock_print):
        directory = ['dir1/dir2/file1', 'dir1/file2', 'file1']
        self.shell.find(directory, 'file1')
        mock_print.assert_any_call('dir1/dir2/file1')
        mock_print.assert_any_call('file1')


if __name__ == '__main__':
    unittest.main()
