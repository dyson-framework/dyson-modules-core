from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from dyson import constants
from dyson.constants import to_boolean
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector_to_by


class WaitForModule(DysonModule):
    VALID_ACTIONS = frozenset([
        'visibility_of',
        'invisibility_of',
        'presence_of',
        'title_to_be',
        'title_to_contain',
        'alert',
        'text_to_be_present',
        'clickable',
        'value_to_be',
        'staleness_of',
        'presence_of_all',
        'element_to_be_selected',
        'selection_state_to_be',
        'frame_and_switch'
    ])

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
                    raise DysonError("Key \"element\" is required")

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
                    raise DysonError("Key \"element\" is required")

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
                    raise DysonError("Key \"element\" is required")

                timeout = int(constants.DEFAULT_TIMEOUT)  # seconds

                if 'timeout' in params['presence_of']:
                    timeout = int(params['presence_of']['timeout'])

                return self._wait_for(element, expected_conditions.presence_of_element_located, timeout, webdriver)

            if 'title_to_be' in params:
                """
                Wait for the title to be something
                """
                title = params['title_to_be']
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['title_to_be']:
                    timeout = int(params['title_to_be']['timeout'])

                return WebDriverWait(webdriver, timeout).until(
                    expected_conditions.title_is(title)
                )

            if 'title_to_contain' in params:
                """
                Wait for the title to contain
                """
                title = params['title_to_contain']
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['title_to_contain']:
                    timeout = int(params['title_to_contain']['timeout'])

                return WebDriverWait(webdriver, timeout).until(
                    expected_conditions.title_contains(title)
                )

            if 'alert' in params:
                """
                Wait for an alert to be present
                """
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['alert']:
                    timeout = int(params['alert']['timeout'])

                return WebDriverWait(webdriver, timeout).until(
                    expected_conditions.alert_is_present()
                )

            if 'text_to_be_present' in params:
                """
                Wait for text to be present in an element
                """
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['text_to_be_present']:
                    timeout = int(params['text_to_be_present']['timeout'])

                if 'in_element' in params['text_to_be_present']:
                    in_element = params['text_to_be_present']['in_element']

                    if 'text' in params['text_to_be_present']:
                        text = in_element['text']

                        strategy, selector = translate_selector_to_by(in_element)

                        return WebDriverWait(webdriver, timeout).until(
                            expected_conditions.text_to_be_present_in_element(
                                (strategy, selector), text
                            )
                        )
                    else:
                        raise DysonError("Key \"text\" is required")
                else:
                    raise DysonError("Key \"in_element\" is required")

            if 'clickable' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['clickable']:
                    timeout = int(params['clickable']['timeout'])

                return self._wait_for(params['clickable']['element'],
                                      expected_conditions.element_to_be_clickable, timeout, webdriver)

            if 'value_to_be' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['value_to_be']:
                    timeout = int(params['value_to_be']['timeout'])

                if 'in_element' in params['value_to_be']:
                    in_element = params['value_to_be']['in_element']

                    if 'value' in params['value_to_be']:
                        value = in_element['value']

                        strategy, selector = translate_selector_to_by(in_element)

                        return WebDriverWait(webdriver, timeout).until(
                            expected_conditions.text_to_be_present_in_element_value(
                                (strategy, selector), value
                            )
                        )
                    else:
                        raise DysonError("Key \"text\" is required")
                else:
                    raise DysonError("Key \"in_element\" is required")

            if 'staleness_of' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['staleness_of']:
                    timeout = int(params['staleness_of']['timeout'])

                if 'element' in params['staleness_of']:
                    element = params['staleness_of']['element']

                    return self._wait_for(element, expected_conditions.staleness_of, timeout, webdriver)
                else:
                    raise DysonError("Key \"element\" is required")

            if 'presence_of_all' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['presence_of_all']:
                    timeout = int(params['presence_of_all']['timeout'])

                if 'elements' in params['presence_of_all']:
                    elements = params['presence_of_all']

                    return self._wait_for(elements, expected_conditions.presence_of_all_elements_located, timeout,
                                          webdriver)
                else:
                    raise DysonError("Key \"elements\" is required")

            if 'element_to_be_selected' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['element_to_be_selected']:
                    timeout = int(params['element_to_be_selected']['timeout'])

                if 'element' in params['element_to_be_selected']:
                    element = params['element_to_be_selected']['element']

                    return self._wait_for(element, expected_conditions.element_located_to_be_selected, timeout,
                                          webdriver)
                else:
                    raise DysonError("Key \"element\" is required")

            if 'selection_state_to_be' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['selection_state_to_be']:
                    timeout = int(params['selection_state_to_be']['timeout'])

                if 'in_element' in params['selection_state_to_be']:
                    in_element = params['selection_state_to_be']['in_element']

                    if 'state' in params['selection_state_to_be']:
                        state = to_boolean(params['selection_state_to_be']['state'])

                        strategy, selector = translate_selector_to_by(in_element)
                        return WebDriverWait(webdriver, timeout).until(
                            expected_conditions.element_located_selection_state_to_be(
                                (strategy, selector), state
                            )
                        )
                    else:
                        raise DysonError("Key \"state\" is required")
                else:
                    raise DysonError("Key \"in_element\" is required")

            if 'frame_and_switch' in params:
                timeout = int(constants.DEFAULT_TIMEOUT)

                if 'timeout' in params['frame_and_switch']:
                    timeout = int(params['frame_and_switch']['timeout'])

                if 'frame' in params['frame_and_switch']:
                    frame = params['frame_and_switch']['frame']

                    return self._wait_for(frame, expected_conditions.frame_to_be_available_and_switch_to_it, timeout,
                                          webdriver)
                else:
                    raise DysonError("Key \"frame\" is required")

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

        return WebDriverWait(webdriver, timeout).until(
            expected_condition((strategy, selector))
        )
