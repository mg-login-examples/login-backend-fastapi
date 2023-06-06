from test.admin_app_e2e_tests.users.admin_user import AdminUser

# Test admin login
def test_admin_user_login(admin_user_not_logged_in: AdminUser):
    admin_user_not_logged_in.open_app_and_login()
