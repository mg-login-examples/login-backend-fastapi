from test.admin_app_e2e_tests.users.admin_user import AdminUser

# Test link "navigate to home"
def test_item_view_go_home(admin_user: AdminUser):
    admin_user.on_resources_dashboard().users_resources_link.click()
    admin_user.on_users_list_views().view_url.expect_to_be_open()
    admin_user.on_users_list_views().users_resources_title.expect_to_contain_text("Users")
    admin_user.on_topbar().home_link.click()
    admin_user.on_resources_dashboard().view_url.expect_to_be_open()

# Test link "navigate to users list"
def test_admin_view_users_resource(admin_user: AdminUser):
    admin_user.on_resources_dashboard().users_resources_link.click()
    admin_user.on_users_list_views().view_url.expect_to_be_open()
    admin_user.on_users_list_views().users_resources_title.expect_to_contain_text("Users")

# Test link "navigate to quotes list"
def test_admin_view_quotes_resource(admin_user: AdminUser):
    admin_user.on_resources_dashboard().quotes_resources_link.click()
    admin_user.on_quotes_list_views().view_url.expect_to_be_open()
    admin_user.on_quotes_list_views().quotes_resources_title.expect_to_contain_text("Quotes")

# Test link "navigate to user notes list"
def test_admin_view_user_notes_resource(admin_user: AdminUser):
    admin_user.on_resources_dashboard().user_notes_resources_link.click()
    admin_user.on_user_notes_list_views().view_url.expect_to_be_open()
    admin_user.on_user_notes_list_views().user_notes_resources_title.expect_to_contain_text("User-notes")
