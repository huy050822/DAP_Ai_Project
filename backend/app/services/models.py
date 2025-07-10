from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    content: str
    type: str  # 'user' or 'assistant'
    timestamp: datetime

class Conversation(BaseModel):
    id: str
    title: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    user_id: str
    analysis_results: Optional[dict] = None

class AnalysisResult(BaseModel):
    type: str  # e.g., 'sales', 'inventory', 'customers'
    data: dict
    timestamp: datetime
    conversation_id: str
    user_id: str

class UserPreference(BaseModel):
    user_id: str
    preferred_analyses: List[str]
    frequently_asked: List[str]
    last_active: datetime
