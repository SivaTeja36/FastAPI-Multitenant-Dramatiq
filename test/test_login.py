from .test_base import TestBase


class TestLogin(TestBase):
    def test_superadmin_logsin_successfully(self):
        self.login_as_super_admin()

    def test_invalid_user_cant_login(self):
        login_result = self.client.post('/login', content=self.invalid_user_credentials.model_dump_json())
        assert login_result.status_code == 404