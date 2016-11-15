from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class GetAttributeModule(DysonModule):
    def run(self, webdriver, params):
        """
        Get an attribute of an element
        :param webdriver:
        :param params:
        :return:
        """

        if 'of' in params:
            if 'attribute' in params:
                element = params['of']
                attribute = params['attribute']

                strategy, selector = translate_selector(element, webdriver)

                return strategy(selector).get_attribute(attribute)
            else:
                raise DysonError("Key \"attribute\" required")
        else:
            raise DysonError("Key \"of\" required")
