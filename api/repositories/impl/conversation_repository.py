from api.repositories.i_conversation_repository import IConversationRepository
from api.models import Conversation

class ConversationRepository(IConversationRepository):
    def create_conversation(self, user):
        print(f"Creating conversation for user: {user}")  # Print statement to check the user
        conversation = Conversation(sender=user)  # This will be mocked during testing
        print(f"Conversation created: {conversation}")  # Print statement to verify creation
        conversation.save()
        return conversation
    
    def get_conversation_by_id(self, conversation_id):
        return Conversation.objects.filter(id=conversation_id).first()
    
    def get_conversation_by_user(self, user):
        return Conversation.objects.filter(user=user).first()
    
    def delete_conversation(self, conversation_id):
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.delete()
        return conversation
    
    def update_conversation(self, conversation_id, **kwargs):
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            for key, value in kwargs.items():
                setattr(conversation, key, value)
            conversation.save()
        return conversation
    