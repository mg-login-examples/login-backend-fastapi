import logging

import allure

logger = logging.getLogger(__name__)

class ResourceListTasks:
    def __init__(self, user):
        from test.admin_app_e2e_tests.users.admin_user import AdminUser # Import inside to avoid cyclic import error
        self.user: AdminUser = user

    def navigate_to_last_page(self):
        step_desc = f"User '{self.user.name}' navigate to last page in resource list"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            if self.user.on_resource_list_view().navigate_to_last_page_button.check_if_enabled():
                self.user.on_resource_list_view().navigate_to_last_page_button.click()
            self.user.on_resource_list_view().navigate_to_last_page_button.expect_to_be_disabled()
        step_wrapper()
