from django.test import TestCase
from unittest.mock import patch, MagicMock
from api.repositories.conversation_repository import ConversationRepository
from api.models import Conversation, CustomGuest


class TestConversationRepository(TestCase):
    
    def setUp(self):
        # Create a real CustomGuest instance with correct fields
        self.user = CustomGuest.objects.create(
            fullname='Test User',
            age=30,
            telephone='1234567890'
        )
        self.repo = ConversationRepository()

    @patch('api.repositories.conversation_repository.Conversation')  # Ensure correct path
    def test_create_conversation(self, MockConversation):
        # Arrange
        mock_conversation = MockConversation.return_value  # This will be the mock instance

        # Act
        result = self.repo.create_conversation(self.user)

        # Assert
        MockConversation.assert_called_once_with(user=self.user)  # Ensure it was called correctly
        mock_conversation.save.assert_called_once()  # Ensure the save method was called
        self.assertEqual(result, mock_conversation)  # Check that the returned value is the mock

    @patch('api.models.Conversation.objects.filter')
    def test_get_conversation_by_id(self, mock_filter):
        # Arrange
        mock_conversation = MagicMock()
        mock_filter.return_value.first.return_value = mock_conversation

        # Act
        conversation_id = 1
        result = self.repo.get_conversation_by_id(conversation_id)

        # Assert
        mock_filter.assert_called_once_with(id=conversation_id)
        self.assertEqual(result, mock_conversation)

    @patch('api.models.Conversation.objects.filter')
    def test_get_conversation_by_user(self, mock_filter):
        # Arrange
        mock_conversation = MagicMock()
        mock_filter.return_value.first.return_value = mock_conversation

        # Act
        result = self.repo.get_conversation_by_user(self.user)

        # Assert
        mock_filter.assert_called_once_with(user=self.user)
        self.assertEqual(result, mock_conversation)

    @patch('api.repositories.conversation_repository.ConversationRepository.get_conversation_by_id')
    def test_delete_conversation(self, mock_get_conversation_by_id):
        # Arrange
        mock_conversation = MagicMock()
        mock_get_conversation_by_id.return_value = mock_conversation

        # Act
        conversation_id = 1
        result = self.repo.delete_conversation(conversation_id)

        # Assert
        mock_get_conversation_by_id.assert_called_once_with(conversation_id)
        mock_conversation.delete.assert_called_once()
        self.assertEqual(result, mock_conversation)

    @patch('api.repositories.conversation_repository.ConversationRepository.get_conversation_by_id')
    def test_update_conversation(self, mock_get_conversation_by_id):
        # Arrange
        mock_conversation = MagicMock()
        mock_get_conversation_by_id.return_value = mock_conversation

        # Act
        conversation_id = 1
        updates = {'status': 'active'}
        result = self.repo.update_conversation(conversation_id, **updates)

        # Assert
        mock_get_conversation_by_id.assert_called_once_with(conversation_id)
        mock_conversation.status = 'active'  # Ensure the attribute is set correctly
        mock_conversation.save.assert_called_once()
        self.assertEqual(result, mock_conversation)
