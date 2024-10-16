import unittest
from unittest.mock import patch, MagicMock
from dobyemail.reader import Reader

class TestReader(unittest.TestCase):

    def setUp(self):
        self.reader = Reader('imap.example.com', 993, True, 'username', 'password')

    @patch('imaplib.IMAP4_SSL')
    def test_list_emails(self, mock_imap_ssl):
        mock_imap = MagicMock()
        mock_imap_ssl.return_value.__enter__.return_value = mock_imap
        mock_imap.search.return_value = ('OK', [b'1 2 3'])
        mock_imap.fetch.side_effect = [
            ('OK', [(b'1 (RFC822 {1234}', b'raw email data 1'), b')']),
            ('OK', [(b'2 (RFC822 {1234}', b'raw email data 2'), b')']),
            ('OK', [(b'3 (RFC822 {1234}', b'raw email data 3'), b')'])
        ]
        
        with patch('email.message_from_bytes') as mock_message_from_bytes:
            mock_email = MagicMock()
            mock_email.__getitem__.side_effect = lambda x: {
                'Subject': 'Test Subject',
                'From': 'sender@example.com',
                'Date': 'Mon, 15 May 2023 10:00:00 +0000'
            }[x]
            mock_email.is_multipart.return_value = False
            mock_email.get_payload.return_value = b'Test Body'
            mock_message_from_bytes.return_value = mock_email
            
            emails = self.reader.list_emails('2023-01-01', '2023-12-31')
        
        self.assertEqual(len(emails), 3)
        mock_imap.select.assert_called_once_with('INBOX')
        mock_imap.search.assert_called_once()
        self.assertEqual(mock_imap.fetch.call_count, 3)
        for email in emails:
            self.assertEqual(email['subject'], 'Test Subject')
            self.assertEqual(email['from'], 'sender@example.com')
            self.assertEqual(email['date'], 'Mon, 15 May 2023 10:00:00 +0000')
            self.assertEqual(email['body'], 'Test Body...')

    @patch('imaplib.IMAP4_SSL')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_download_attachments(self, mock_open, mock_makedirs, mock_imap_ssl):
        mock_imap = MagicMock()
        mock_imap_ssl.return_value.__enter__.return_value = mock_imap
        mock_imap.select.return_value = ('OK', [b'1'])
        mock_imap.search.return_value = ('OK', [b'1'])
        mock_imap.fetch.return_value = ('OK', [(b'1 (RFC822 {1234}', b'raw email data'), b')'])
        
        with patch('email.message_from_bytes') as mock_message_from_bytes:
            mock_email = MagicMock()
            mock_attachment = MagicMock()
            mock_attachment.get_filename.return_value = 'test.txt'
            mock_attachment.get_payload.return_value = 'attachment content'
            mock_email.walk.return_value = [mock_attachment]
            mock_message_from_bytes.return_value = mock_email
            
            result = self.reader.download_attachments('2023-01-01', '2023-12-31')
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn('test.txt', result[0])
        mock_open.assert_called_once()
        mock_makedirs.assert_called_once()

if __name__ == '__main__':
    unittest.main()
