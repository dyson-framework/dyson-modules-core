from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class SetTextModule(DysonModule):
    def run(self, webdriver, params):
        """
        Set the text of an input
        :param webdriver:
        :param params:
        :return:
        """
        if 'of' in params and 'to' in params:
            strategy, selector = translate_selector(params['of'], webdriver=webdriver)
            return strategy(selector).send_keys(params['to'])
        else:
            raise DysonError("Keys \"of\" and \"to\" are required")

