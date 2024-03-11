import json

class JSONArgumentParser:
    @staticmethod
    def parse_arguments( json_arguments ):
        return json.loads( json_arguments )