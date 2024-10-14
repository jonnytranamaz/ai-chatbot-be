# tests/repositories/test_message_repository.py

from django.test import TestCase
from unittest.mock import patch, Mock
from unittest.mock import patch, MagicMock
from api.repositories.message_repository import MessageRepository
from api.models import Message, Conversation, CustomGuest


class TestMessageRepository(TestCase):

    
    def setUp(self):
        self.repo = MessageRepository()
        self.conversation = 'some_conversation'  # Replace with your actual conversation object
        self.owner_type = 'some_owner_type'      # Replace with your actual owner type

    @patch('api.repositories.message_repository.Message')
    def test_create_message(self, MockMessage):
        # Configure the mock to return an instance when called
        mock_instance = MockMessage.return_value
            
        # Call the method under test
        result = self.repo.create_message(self.conversation, self.owner_type, content='Hello, world!')

        # Assertions
        MockMessage.assert_called_once_with(
            conversation=self.conversation,
            owner_type=self.owner_type,
            content='Hello, world!',
            image=None,
            file=None,
            sender=None
        )
        self.assertEqual(result, mock_instance)  # Check if the returned result is the mock instance
        mock_instance.save.assert_called_once()  # Ensure save was called

    @patch('api.models.Message.objects.filter')
    def test_get_messages_by_conversation(self, mock_filter):
        # Arrange
        mock_message_list = [MagicMock(), MagicMock()]
        mock_filter.return_value.order_by.return_value = mock_message_list

        # Act
        result = self.repo.get_messages_by_conversation(self.conversation)

        # Assert
        mock_filter.assert_called_once_with(conversation=self.conversation)
        self.assertEqual(result, mock_message_list)

    @patch('api.models.Message.objects.filter')
    def test_get_message_by_id(self, mock_filter):
        # Arrange
        mock_message = MagicMock()
        mock_filter.return_value.first.return_value = mock_message

        # Act
        message_id = 1
        result = self.repo.get_message_by_id(message_id)

        # Assert
        mock_filter.assert_called_once_with(id=message_id)
        self.assertEqual(result, mock_message)

    @patch('api.repositories.message_repository.Message')
    def test_update_message(self, MockMessage):
        message_id = 1  # Example message ID
        updated_content = "Updated message content"

        # Set up the mock to return an instance when filtering
        mock_instance = MockMessage.return_value
        MockMessage.objects.filter.return_value.first.return_value = mock_instance

        # Call the method under test (you need to implement this method in your repository)
        self.repo.update_message(message_id, content=updated_content)

        # Assertions
        MockMessage.objects.filter.assert_called_once_with(id=message_id)  # Ensure filtering is called
        mock_instance.save.assert_called_once()  # Ensure save is called after updating
        self.assertEqual(mock_instance.content, updated_content)  # Check if content is updated


    @patch('api.repositories.message_repository.Message')
    def test_delete_message(self, MockMessage):
        message_id = 1  # Example message ID

        # Create a mock instance for the message
        mock_instance = MockMessage.return_value

        # Mock the get_message_by_id method to return the mock_instance
        self.repo.get_message_by_id = Mock(return_value=mock_instance)

        # Call the method under test
        result = self.repo.delete_message(message_id)

        # Assertions
        self.repo.get_message_by_id.assert_called_once_with(message_id)  # Ensure get_message_by_id is called
        mock_instance.delete.assert_called_once()  # Ensure delete is called on the message instance
        self.assertEqual(result, mock_instance)  # Ensure the returned message is the mock instance
