from app.models.auth_models import LoginResponse
from app.models.organization_models import OrganizationRequest, OrganizationResponse
from .test_base import TestBase


class TestLogin(TestBase):
    admin_base = '/admin/org/'
    
    def execute_org_request(self, endpoint:str,payload:str):
        return self.get_authenticated_client().post(f'{self.admin_base}{endpoint}', content=payload)
    
    def execute_unauthenticated_org_request(self, endpoint:str,payload:str):
        self.client.headers.clear()
        return self.client.post(f'{self.admin_base}{endpoint}', content=payload)

    def test_organization_created_successfully(self):
        org_payload = OrganizationRequest(name="test org",logo="")
        creation_result = self.execute_org_request('create',org_payload.model_dump_json())
        assert creation_result.status_code == 201
        result = OrganizationResponse(**creation_result.json())
        result.name == 'test org'
    
    def test_organization_cant_create_when_not_authenticated(self):
        org_payload = OrganizationRequest(name="test org",logo="")
        creation_result = self.execute_unauthenticated_org_request('create',org_payload.model_dump_json())
        assert creation_result.status_code == 403