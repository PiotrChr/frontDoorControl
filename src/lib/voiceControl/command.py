import re
from pprint import pprint


class Command:
    def __init__(self, name=None, regex_identifiers=None, has_params=None, param_filters=None, handler=None, requires_auth=None):
        self.name = name
        self.regex_identifiers = regex_identifiers
        self.has_params = has_params
        self.param = None
        self.param_filters = param_filters
        self.handler = handler
        self.requires_auth = requires_auth

    def match_and_prepare(self, text):
        pprint(self.regex_identifiers)
        for regex in self.regex_identifiers:
            match = re.search(regex, text)

            if match:
                if self.has_params:
                    command, param = match.groups()

                    if self.param_filters and self.validate_param(param):
                        self.param = param

                print('name', self.name)
                print('param', self.param)
                return True

        return False

    def validate_param(self, param):
        valid = False

        for param_filter in self.param_filters:
            if re.match(param_filter, param):
                valid = True

        return valid

    def handle(self):
        if self.has_params:
            self.handler(self.param)
        else:
            self.handler()
