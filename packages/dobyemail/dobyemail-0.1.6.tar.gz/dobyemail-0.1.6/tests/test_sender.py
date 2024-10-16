import unittest
from unittest.mock import patch, MagicMock
from dobyemail.sender import Sender

class TestSender(unittest.TestCase):

    def setUp(self):
        self.sender = Sender('smtp.example.com', 587, True, 'imap.example.com', 993, True, 'username', 'password')

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        result = self.sender.send_email('to@example.com', 'Test Subject', 'Test Body')
        
        self.assertEqual(result, "Email sent successfully")
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('username', 'password')
        mock_smtp_instance.send_message.assert_called_once()

    @patch('smtplib.SMTP')
    @patch('builtins.open', unittest.mock.mock_open(read_data=b'file content'))
    def test_send_email_with_attachment(self, mock_smtp):
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        result = self.sender.send_email('to@example.com', 'Test Subject', 'Test Body', attachments=['test.txt'])
        
        self.assertEqual(result, "Email sent successfully")
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('username', 'password')
        mock_smtp_instance.send_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()
