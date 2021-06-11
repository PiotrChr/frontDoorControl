from dateutil.parser import parse


class Helpers:

    @staticmethod
    def is_date(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False
