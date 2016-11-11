from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from dyson import constants
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector_to_by


class WaitForModule(DysonModule):
    VALID_ACTIONS = frozenset(['visibility_of', 'invisibility_of'])

    def run(self, webdriver, params):
        """
        Wait for things
        :param webdriver:
        :param params:
        :return:
        """

        if isinstance(params, dict):
            if 'visibility_of' in params:
                """
                Wait for the visibility of an element
                """
                if 'element' in params['visibility_of']:
                    element = params['visibility_of']['element']
                else:
                    return self.fail("Key \"element\" is required")

                timeout = int(constants.DEFAULT_TIMEOUT)  # seconds

                if 'timeout' in params['visibility_of']:
                    timeout = int(params['visibility_of']['timeout'])

                return self._wait_for(element, expected_conditions.visibility_of_element_located, timeout, webdriver)

            if 'invisibility_of' in params:
                """
                Wait for the invisibility of an element
                """
                if 'element' in params['invisibility_of']:
                    element = params['invisibility_of']['element']
                else:
                    return self.fail("Key \"element\" is required")

                timeout = int(constants.DEFAULT_TIMEOUT)  # seconds

                if 'timeout' in params['invisibility_of']:
                    timeout = int(params['invisibility_of']['timeout'])

                return self._wait_for(element, expected_conditions.invisibility_of_element_located, timeout, webdriver)

            if 'presence_of' in params:
                """
                Wait for the presence of an element
                """
                if 'element' in params['presence_of']:
                    element = params['presence_of']['element']
                else:
                    return self.fail("Key \"element\" is required")

                timeout = int(constants.DEFAULT_TIMEOUT)  # seconds

                if 'timeout' in params['presence_of']:
                    timeout = int(params['presence_of']['timeout'])

                return self._wait_for(element, expected_conditions.presence_of_element_located, timeout, webdriver)

        else:
            self.fail("Invalid type. You must specify a valid action")

    def _wait_for(self, element, expected_condition, timeout, webdriver):
        """
        Helper method to wait for a specific condition of an element
        :param element: the element as it's passed from the test (e.g. "css=something")
        :param expected_condition: the ExpectedCondition from Selenium
        :return:
        """
        strategy, selector = translate_selector_to_by(element)

        try:
            e = WebDriverWait(webdriver, timeout).until(
                expected_condition((strategy, selector))
            )
            return e
        except:
            return self.fail("%s could not be satisifed for \"%s\" in %s seconds"
                             % (expected_condition.__name__, element, timeout))
