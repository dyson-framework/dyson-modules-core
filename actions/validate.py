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
                    - is
                    - is_not
                - present
                - not_present
                - text_of
                    - is
                    - is_not
                - value_of
                    - is
                    - is_not
        :return:
        """
        if params:
            if 'title' in params:
                """
                Validate the title_shouldbe of the page
                """
                actual_title = webdriver.title
                title_shouldbe = params['title']
                if 'is' in title_shouldbe:
                    if actual_title != title_shouldbe:
                        self.fail("Title is not \"%s\". Actual: \"%s\"" % (title_shouldbe, actual_title))

                elif 'is_not' in title_shouldbe:
                    if actual_title == title_shouldbe:
                        self.fail("Title is \"%s\" when it shouldn't be" % title_shouldbe)

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
                Validate text (or innerText) of an element
                """
                text_of = params['text_of']
                if 'element' in text_of:
                    self._validate_present(text_of['element'], webdriver)
                else:
                    self.fail("Key \"element\" is required")

                if 'is' in text_of:
                    strategy, selector = translate_selector(text_of['element'], webdriver)
                    actual_text = strategy(selector).text
                    if actual_text != text_of['is']:
                        self.fail("Text of %s is not \"%s\".  Actual: \"%s\"" %
                                  (text_of['element'], text_of['is'], actual_text))
                elif 'is_not' in text_of:
                    strategy, selector = translate_selector(text_of['element'], webdriver)
                    actual_text = strategy(selector).text
                    if actual_text == text_of['is_not']:
                        self.fail("Text of %s is \"%s\" when it shouldn't be" % (
                            text_of['element'], text_of['is_not']
                        ))

            if 'value_of' in params:
                """
                Validate value attribute of an element
                """
                value_of = params['value_of']
                if 'element' in value_of:
                    self._validate_present(value_of['element'], webdriver)
                else:
                    self.fail("Key \"element\" is required")

                if 'is' in value_of:
                    strategy, selector = translate_selector(value_of['element'], webdriver)
                    actual_value = strategy(selector).get_attribute('value')
                    if actual_value != value_of['is']:
                        self.fail("Value of %s is not \"%s\". Actual: \"%s\"" % (
                            value_of['element'], value_of['is'], actual_value
                        ))
                elif 'is_not' in value_of:
                    strategy, selector = translate_selector(value_of['element'], webdriver)
                    actual_value = strategy(selector).get_attribute('value')
                    if actual_value == value_of['is']:
                        self.fail("Value of %s is \"%s\" when it shouldn't be" % (
                            value_of['element'], value_of['is']
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
