from dyson.utils.module import DysonModule


class GotoModule(DysonModule):
    def run(self, webdriver, params):
        if isinstance(params, dict):
            if params['url']:
                return webdriver.get(params['url'])
            else:
                self.fail("You need to specify a valid URL to go to")
        else:
            self.fail("Key \"url\" is required")
