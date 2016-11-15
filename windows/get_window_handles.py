from dyson.utils.module import DysonModule


class GetWindowHandlesModule(DysonModule):
    def run(self, webdriver, params):
        """
        Return the available window handles
        :param webdriver:
        :param params:
        :return:
        """
        return webdriver.window_handles
