from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class UncheckModule(DysonModule):
    def run(self, webdriver, params):
        """
        Unchecks an element on the page.
        ONLY applies to checkbox's
        :param webdriver:
        :param params:
        :return:
        """
        if len(params.keys()) > 0:
            selector, strategy = translate_selector(params, webdriver)

            if selector and strategy:
                element = selector(strategy)

                if element.is_selected():
                    return selector(strategy).click()
            else:
                raise DysonError("You need to specify a valid selector to uncheck")
        else:
            raise DysonError("You need to specify an argument to \"uncheck\"")
