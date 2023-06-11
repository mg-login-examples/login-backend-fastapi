from playwright.sync_api import expect

from test.admin_app_e2e_tests.users.admin_user import AdminUser

# Test admin login
def test_admin_user_login(admin_user_not_logged_in: AdminUser):
    admin_user_not_logged_in.on_login_view().view_url.open()
    expect(admin_user_not_logged_in.page).to_have_title("vue_admin")
    admin_user_not_logged_in.with_login_tasks().login(admin_user_not_logged_in.email, admin_user_not_logged_in.password)
    admin_user_not_logged_in.on_resources_dashboard().view_url.expect_to_be_open()
