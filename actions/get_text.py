from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class GetTextModule(DysonModule):
    def run(self, webdriver, params):
        """
        Get the text of a specific element (return innerText)
        :param webdriver:
        :param params:
        :return:
        """
        if 'of' in params:
            strategy, selector = translate_selector(params['of'], webdriver)
            return strategy(selector).text
        else:
            raise DysonError("Key \"of\" is required")
