from dyson.utils.module import DysonModule


class GotoModule(DysonModule):
    def run(self, webdriver, params):
        if params['url']:
            webdriver.get(params['url'])
