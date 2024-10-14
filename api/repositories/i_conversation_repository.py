from abc import ABC, abstractmethod
from typing import Optional
from ..models import Conversation, CustomUser

class IConversationRepository(ABC):

    @abstractmethod
    def create_conversation(self, user: CustomUser) -> Conversation:
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: int) -> Optional[Conversation]:
        pass

    @abstractmethod
    def get_conversation_by_user(self, user: CustomUser) -> Optional[Conversation]:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: int) -> Optional[Conversation]:
        pass

    @abstractmethod
    def update_conversation(self, conversation_id: int, **kwargs) -> Optional[Conversation]:
        pass