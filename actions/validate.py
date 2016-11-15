from six import string_types

from dyson.constants import to_boolean
from dyson.errors import DysonError
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
                - is_checked
                - is_unchecked
        :return:
        """
        if params and isinstance(params, dict):
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
                strategy, selector = translate_selector(params['present'], webdriver)
                return strategy(selector)

            if 'not_present' in params:
                """
                Validate the absence of an element
                """
                element = None
                strategy, selector = translate_selector(params['not_present'], webdriver)
                return strategy(selector)

            if 'text_of' in params:
                """
                Validate text (or innerText) of an element
                """
                text_of = params['text_of']
                if 'element' not in text_of:
                    raise DysonError("Key \"element\" is required")

                if 'is' in text_of:
                    strategy, selector = translate_selector(text_of['element'], webdriver)
                    actual_text = strategy(selector).text
                    if actual_text != text_of['is']:
                        self.fail("Text of %s is not \"%s\".  Actual: \"%s\"" %
                                  (text_of['element'], text_of['is'], actual_text))
                    else:
                        return actual_text
                elif 'is_not' in text_of:
                    strategy, selector = translate_selector(text_of['element'], webdriver)
                    actual_text = strategy(selector).text
                    if actual_text == text_of['is_not']:
                        self.fail("Text of %s is \"%s\" when it shouldn't be" % (
                            text_of['element'], text_of['is_not']
                        ))
                    else:
                        return actual_text

            if 'value_of' in params:
                """
                Validate value attribute of an element
                """
                value_of = params['value_of']
                if 'element' not in value_of:
                    raise DysonError("Key \"element\" is required")

                if 'is' in value_of:
                    strategy, selector = translate_selector(value_of['element'], webdriver)
                    actual_value = strategy(selector).get_attribute('value')
                    if actual_value != value_of['is']:
                        self.fail("Value of %s is not \"%s\". Actual: \"%s\"" % (
                            value_of['element'], value_of['is'], actual_value
                        ))
                    else:
                        return actual_value
                elif 'is_not' in value_of:
                    strategy, selector = translate_selector(value_of['element'], webdriver)
                    actual_value = strategy(selector).get_attribute('value')
                    if actual_value == value_of['is']:
                        self.fail("Value of %s is \"%s\" when it shouldn't be" % (
                            value_of['element'], value_of['is']
                        ))
                    else:
                        return actual_value

            if 'is_checked' in params:
                """
                Validate that a checkbox / radio button is checked
                """
                element = params['is_checked']
                strategy, selector = translate_selector(element, webdriver)
                status = strategy(selector).is_selected()
                if not status:
                    self.fail("Element %s is not checked" % element)
                else:
                    return status

            if 'is_not_checked' in params:
                """
                Validate that a checkbox / radio button is unchecked
                """
                element = params['is_not_checked']
                strategy, selector = translate_selector(element, webdriver)

                status = strategy(selector).is_selected()
                if status:
                    self.fail("Element %s is checked" % element)
                else:
                    return status

        elif isinstance(params, string_types):
            result = eval(params)
            if not to_boolean(result):
                self.fail("\"%s\" has a result of False" % params)
            return result
