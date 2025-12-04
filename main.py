from model_ops import Model_Operations
from url_processor import URLProcessor
from response_parser import ResponseParser


def run_all_urls():
    db = Model_Operations()

    list_urls = db.get_all_active_urls()

    processor = URLProcessor()

    res = processor.check_urls(list_urls)

    parsed_values = ResponseParser().parse_all(res, list_urls)
    return parsed_values