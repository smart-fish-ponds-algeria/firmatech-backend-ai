from pydantic import BaseModel

class DiseaseRequest(BaseModel):
    pass


class DiseaseResponse(BaseModel):
    isSick: bool
