from dyson.errors import DysonError
from dyson.utils.module import DysonModule


class GotoModule(DysonModule):
    def run(self, webdriver, params):
        if isinstance(params, dict):
            if params['url']:
                return webdriver.get(params['url'])
            else:
                raise DysonError("You need to specify a valid URL to go to")
        else:
            raise DysonError("Key \"url\" is required")
