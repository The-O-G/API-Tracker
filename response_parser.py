import json

from models import URLList
class ResponseParser:

    def __init__(self):
        pass


    def parse(self, response: dict, pattern: list):    
        local_vars = {}
        exec(pattern, {}, local_vars)
        parse_func = local_vars["filter"]

        return parse_func(response)

    def parse_all(self, response_content:list, filter_info:list[URLList]):
            return [
                self.parse(resp, filter.filter) for resp, filter in zip(response_content, filter_info)
            ]