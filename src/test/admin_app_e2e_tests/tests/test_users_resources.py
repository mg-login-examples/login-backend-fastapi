from random import randint
from test.admin_app_e2e_tests.users.admin_user import AdminUser
from test.admin_app_e2e_tests.utils.mock_data.mock_user_data import \
    get_mock_user_login

import pytest

# Test create new user


def test_create_new_user(admin_user: AdminUser):
    test_user_email, test_password = get_mock_user_login()
    admin_user.on_users_list_view().view_url.open()
    admin_user.on_users_list_view().users_resources_title.expect_to_be_visible()
    admin_user.with_user_resource_tasks().create_basic_user(
        test_user_email, test_password
    )
    admin_user.on_users_list_view().user_with_email(
        test_user_email
    ).expect_to_be_visible()


def test_edit_user(admin_user: AdminUser):
    # Create user
    test_user_email, test_password = get_mock_user_login()
    admin_user.on_users_list_view().view_url.open()
    admin_user.on_users_list_view().users_resources_title.expect_to_be_visible()
    admin_user.with_user_resource_tasks().create_basic_user(
        test_user_email, test_password
    )
    admin_user.on_users_list_view().user_with_email(
        test_user_email
    ).expect_to_be_visible()

    # Edit user
    test_user_email_updated, _ = get_mock_user_login()
    admin_user.on_users_list_view().user_update_button(test_user_email).click()
    admin_user.on_user_update_dialog().update_user_dialog.expect_to_be_visible()
    admin_user.on_user_update_dialog().user_email_input.expect_to_have_value(
        test_user_email
    )
    admin_user.on_user_update_dialog().update_user_button.expect_to_be_disabled()
    admin_user.on_user_update_dialog().user_email_input.fill(test_user_email_updated)
    admin_user.on_user_update_dialog().user_email_input.expect_to_have_value(
        test_user_email_updated
    )
    admin_user.on_user_update_dialog().update_user_button.expect_to_be_enabled()
    admin_user.on_user_update_dialog().update_user_button.click()
    admin_user.on_user_update_dialog().update_user_dialog.expect_not_to_be_visible()
    admin_user.on_users_list_view().user_with_email(
        test_user_email
    ).expect_not_to_be_visible()
    admin_user.on_users_list_view().user_with_email(
        test_user_email_updated
    ).expect_to_be_visible()


# Test delete user


def test_delete_user(admin_user: AdminUser):
    # Create user
    test_user_email, test_password = get_mock_user_login()
    admin_user.on_users_list_view().view_url.open()
    admin_user.on_users_list_view().users_resources_title.expect_to_be_visible()
    admin_user.with_user_resource_tasks().create_basic_user(
        test_user_email, test_password
    )
    admin_user.on_users_list_view().user_with_email(
        test_user_email
    ).expect_to_be_visible()

    # Delete user
    admin_user.on_users_list_view().user_delete_button(test_user_email).click()
    admin_user.on_user_delete_dialog().delete_user_dialog.expect_to_be_visible()
    admin_user.on_user_delete_dialog().delete_user_message(
        test_user_email
    ).expect_to_be_visible()
    admin_user.on_user_delete_dialog().delete_user_button.click()
    admin_user.on_user_delete_dialog().delete_user_dialog.expect_not_to_be_visible()
    admin_user.on_users_list_view().navigate_to_last_page_button.expect_to_be_disabled()
    admin_user.on_users_list_view().user_with_email(
        test_user_email
    ).expect_not_to_be_visible()


def test_view_user_info(admin_user: AdminUser):
    pass
