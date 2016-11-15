from six import string_types

from dyson.errors import DysonError
from dyson.modules.core.navigation.goto import GotoModule
from dyson.utils.module import DysonModule


class NavigateModule(DysonModule):
    def run(self, webdriver, params):
        """
        Navigate between pages.
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, string_types):
            if 'forward' is params:
                webdriver.forward()
            elif 'back' is params:
                webdriver.back()
        elif isinstance(params, dict):
            if 'to' in params:
                GotoModule().run(webdriver, {'url': params['to']})
        else:
            raise DysonError("Invalid type")
