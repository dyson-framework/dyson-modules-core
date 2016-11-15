from six import string_types

from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector


class SwitchToModule(DysonModule):
    ACTIONS = frozenset(['frame', 'default_content', 'window'])

    def run(self, webdriver, params):
        """
        Collection of switch_to actions with selenium.
        Available actions:
        - switch_to
            - frame <selector>
            - alert
                - action
                    - dismiss
                    - accept
                    - send_keys
                    - authenticate
        :param webdriver:
        :param params:
        :return:
        """

        if isinstance(params, dict):
            if 'frame' in params:
                """
                Switch to a frame / iframe
                """
                selector, strategy = translate_selector(params['frame'], webdriver)
                return webdriver.switch_to.frame(selector(strategy))

            elif 'alert' in params:
                """
                Switch to an alert window
                """
                if 'action' in params['alert']:
                    alert_action = params['alert']['action']
                    valid_actions = frozenset(['accept', 'dismiss', 'authenticate', 'send_keys'])

                    if alert_action in valid_actions:
                        if 'accept' is alert_action:
                            return webdriver.switch_to.alert.accept()
                        elif 'dismiss' is alert_action:
                            return webdriver.switch_to.alert.dismiss()
                        elif 'get_text' is alert_action:
                            return webdriver.switch_to.alert.text
                    else:
                        raise DysonError("Invalid action \"%s\". Valid actions are %s" %
                                  (alert_action, ','.join(valid_actions)))
                elif 'username' in params['alert']:
                    username = params['alert']['username']
                    password = ""

                    if params['alert']['password']:
                        password = params['alert']['password']

                    return webdriver.switch_to.alert.authenticate(username, password)
                else:
                    return webdriver.switch_to.alert()
            elif 'window' in params:
                return webdriver.switch_to.window(params['window'])
            else:
                raise DysonError("Unsure how to switch to \"%s\". Valid options are %s" % (params, ','.join(self.ACTIONS)))

        elif isinstance(params, string_types):
            if "default_content" == params:
                return webdriver.switch_to.default_content()
            else:
                raise DysonError("Unsure how to switch to \"%s\". Valid options are %s" % (params, ','.join(self.ACTIONS)))

