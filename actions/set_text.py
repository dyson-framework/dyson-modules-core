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
        if 'of' in params:
            if 'to' in params:
                strategy, selector = translate_selector(params['of'], webdriver=webdriver)
                strategy(selector).send_keys(params['to'])

                actual_value = strategy(selector).get_attribute('value')

                if actual_value != params['to']:
                    self.fail("Text of %s failed to set to \"%s\".  Actual value: \"%s\"" %
                              (params['of'], params['to'], actual_value))

