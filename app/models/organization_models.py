from pydantic import BaseModel


class OrganizationRequest(BaseModel):
    name: str
    logo: str


class OrganizationResponse(BaseModel):
    name: str
    access_key: str
    id: int
