from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class CheckModule(DysonModule):
    def run(self, webdriver, params):
        """
        Check an element on the page.
        Usually only applies to radio and
        checkbox's
        :param webdriver:
        :param params:
        :return:
        """
        if len(params.keys()) > 0:
            selector, strategy = translate_selector(params, webdriver)

            if selector and strategy:
                element = selector(strategy)

                if not element.is_selected():
                    selector(strategy).click()
            else:
                self.fail("You need to specify a valid selector to check")
        else:
            self.fail("You need to specify an argument to \"check\"")
