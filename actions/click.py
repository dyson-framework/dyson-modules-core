from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class ClickModule(DysonModule):
    def run(self, webdriver, params):
        """
        Click an element on the page
        :param webdriver:
        :param params:
        :return:
        """
        if len(params.keys()) > 0:
            selector, strategy = translate_selector(params, webdriver)

            if selector and strategy:
                return selector(strategy).click()
            else:
                raise DysonError("You need to specify a valid selector to click")
        else:
            raise DysonError("You need to specify an argument to \"click\"")
