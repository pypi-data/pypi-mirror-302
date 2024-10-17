from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ChattyContentContacts(BaseModel):
    full_name: str #Meta Formatted name
    phone_number: str #Meta waid
    name_details: Optional[Dict[str, Any]] = None
    phones: Optional[List[Dict[str, Any]]] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    birthday: Optional[str] = None
    emails: Optional[List[Dict[str, Any]]] = None
    org: Optional[Dict[str, Any]] = None
    urls: Optional[List[Dict[str, Any]]] = None
    
    def model_dump(self) -> Dict[str, Any]:
        data = super().model_dump(exclude_none=True)
        return data
        
        
        

