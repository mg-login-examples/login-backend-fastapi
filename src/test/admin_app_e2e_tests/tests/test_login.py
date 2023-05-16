from test.admin_app_e2e_tests.users.admin_user import AdminUser

def test_admin_user_login(admin_user_not_logged_in: AdminUser):
    admin_user_not_logged_in.open_app_and_login()

def test_admin_view_users_resource(admin_user: AdminUser):
    admin_user.on_resources_dashboard().users_resources_link.click()
    admin_user.on_users_list_views().view_url.expect_to_be_open()
