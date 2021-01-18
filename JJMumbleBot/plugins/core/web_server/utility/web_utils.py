from pydantic import BaseModel
from typing import Dict, Optional, Any


class StdModel(BaseModel):
    text: str


class ResponseModel:
    status: str
    message: str
    data: Dict[str, str]

    def __init__(self, status, message, data_dict: Optional[Dict[str, Any]] = None):
        self.status = status
        self.message = message
        self.data = {}
        if data_dict:
            self.add_data_dict(data_dict)

    def add_data_dict(self, data):
        self.data.update(data)

    def add_data(self, name, entry):
        self.data[name] = entry

    def toDict(self):
        return self.__dict__
