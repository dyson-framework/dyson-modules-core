from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class ValidateModule(DysonModule):
    def run(self, webdriver, params):
        """
        Validate things
        :param webdriver:
        :param params:
            allowed validations:
                - title
                - present
                - not_present
                - text_is
                - text_is_not
        :return:
        """

        if params:
            if 'title' in params:
                """
                Validate the title of the page
                """
                actual_title = webdriver.title
                try:
                    assert params['title'] == actual_title
                except AssertionError:
                    self.fail("Title is not \"%s\". Actual: \"%s\"" % (params['title'], actual_title))

            if 'present' in params:
                """
                Validate the presence of an element
                """
                self._validate_present(params['present'], webdriver)

            if 'not_present' in params:
                """
                Validate the absence of an element
                """
                self._validate_not_present(params['not_present'], webdriver)

            if 'text_of' in params:
                """
                Validate text of an element
                """
                if 'element' in params['text_of']:
                    self._validate_present(params['text_of']['element'], webdriver)
                else:
                    self.fail("Key \"element\" is required")

                if 'is' in params['text_of']:
                    strategy, selector = translate_selector(params['text_of']['element'], webdriver)
                    actual_text = strategy(selector).text
                    if actual_text != params['text_of']['is']:
                        self.fail("Text of %s is not \"%s\".  Actual: \"%s\"" %
                                  (params['text_of']['element'], params['text_of']['is'], actual_text))

            if 'value_of' in params:
                """
                Validate value of an element
                """
                if 'element' in params['value_of']:
                    self._validate_present(params['value_of']['element'], webdriver)
                else:
                    self.fail("Key \"element\" is required")

                if 'is' in params['value_of']:
                    strategy, selector = translate_selector(params['value_of']['element'], webdriver)
                    actual_value = strategy(selector).get_attribute('value')
                    if actual_value != params['value_of']['is']:
                        self.fail("Value of %s is not \"%s\". Actual: \"%s\"" % (
                            params['value_of']['element'], params['value_of']['is'], actual_value
                        ))

    def _validate_present(self, param, webdriver):
        """
        Helper method.  Validate present
        :param param:
        :param webdriver:
        :return:
        """
        strategy, selector = translate_selector(param, webdriver)
        try:
            assert strategy(selector) is not None
        except:
            self.fail("Element with selector \"%s\" is not present" % param)

    def _validate_not_present(self, param, webdriver):
        """
        Helper method.  Validate not present
        :param param:
        :param webdriver:
        :return:
        """
        strategy, selector = translate_selector(param, webdriver)
        try:
            strategy(selector)
            self.fail("Element with selector \"%s\" is present" % param)
        except:
            # pass
            pass
