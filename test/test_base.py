from fastapi.testclient import TestClient
from app.main import app
from app.models.auth_models import LoginRequest, LoginResponse
from app.models.organization_models import OrganizationResponse
class TestBase:
    client:TestClient
    superadmin_user_credentials = LoginRequest(userName="superadmin@unittest.com",password="superadminPasswd")
    valid_user_credentials = LoginRequest(userName="admin@unittest.com",password="adminPasswd")
    invalid_user_credentials = LoginRequest(userName="invaliduser@unittest.com",password="invalid")

    def login_as_super_admin(self):
        login_result = self.client.post('/login', data=self.superadmin_user_credentials.model_dump_json())
        assert login_result.status_code == 200
        response = LoginResponse(**login_result.json())
        assert response.name == self.superadmin_user_credentials.userName.split('@')[0]
        assert response.role == 'SuperAdmin'
        assert response.id == 1
        assert response.contact == '0987654321'
        return response

    def get_default_org(self):
        super_admin = self.login_as_super_admin()
        org_result = self.client.get('/admin/org/1',auth=("Authorization",f"Bearer {super_admin.access_token}"))
        return OrganizationResponse(**org_result.json())
    
    def get_authenticated_client(self,super_admin_auth=True):
        loggedinUser = {'access_token':''}
        if super_admin_auth:
            loggedinUser = self.login_as_super_admin()
        self.client.headers.clear()
        self.client.headers.update({"Authorization":f"Bearer {loggedinUser.access_token}"})
        return self.client

    def setup_class(self):
        self.client = TestClient(app)
        self.login_as_super_admin(self)

    def teardown_class(self):
        pass