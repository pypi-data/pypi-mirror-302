import unittest
from unittest.mock import patch, MagicMock
from dobyemail.transfer import Transfer

class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.transfer = Transfer('imap.example.com', 993, True, 'username', 'password')

    @patch('imaplib.IMAP4_SSL')
    def test_copy_messages(self, mock_imap_ssl):
        mock_imap = MagicMock()
        mock_imap_ssl.return_value.__enter__.return_value = mock_imap
        mock_imap.search.return_value = ('OK', [b'1 2 3'])
        
        self.transfer.copy_messages('INBOX', 'Archive')
        
        mock_imap.select.assert_called_once_with('INBOX')
        mock_imap.search.assert_called_once_with(None, 'ALL')
        self.assertEqual(mock_imap.copy.call_count, 3)

    @patch('imaplib.IMAP4_SSL')
    def test_move_messages(self, mock_imap_ssl):
        mock_imap = MagicMock()
        mock_imap_ssl.return_value.__enter__.return_value = mock_imap
        mock_imap.search.return_value = ('OK', [b'1 2 3'])
        
        self.transfer.move_messages('INBOX', 'Archive')
        
        mock_imap.select.assert_called_once_with('INBOX')
        mock_imap.search.assert_called_once_with(None, 'ALL')
        self.assertEqual(mock_imap.copy.call_count, 3)
        self.assertEqual(mock_imap.store.call_count, 3)
        mock_imap.expunge.assert_called_once()

if __name__ == '__main__':
    unittest.main()
