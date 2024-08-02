import unittest
import logging


from unittest.mock import patch
from divs import get_currency_index
from divs import configure_logging
# from divs import main


logger = logging.getLogger(__name__)

def setup_module(module):
    module.logger.setLevel(logging.DEBUG)


@patch('os.environ')
def test__get_currency_index(mock_environ):
    mock_environ.get.return_value = 'debug'
    logger = configure_logging()


    test_data_1 = [{'cad': {0: {'effectiveDate': '2023-01-02', 'mid': 3.2306}, 1: {'effectiveDate': '2023-01-03', 'mid': 3.2593}}}]
    test_data_2 = [{'cad': {0: {'effectiveDate': '2023-01-02', 'mid': 3.2306}}}, {'usd': {0: {'effectiveDate': '2023-01-02', 'mid': 4.3811}}}]
    test_data_3 = []

    result_1 = get_currency_index(test_data_1)
    result_2 = get_currency_index(test_data_2)
    result_3 = get_currency_index(test_data_3)

    expected_result_1 = [{'currency': 'cad', 'index': 0}]
    expected_result_2 = [{'currency': 'cad', 'index': 0}, {'currency': 'usd', 'index': 1}]
    expected_result_3 = []

    assert result_1 == expected_result_1
    assert result_2 == expected_result_2
    assert result_3 == expected_result_3

if __name__ == '__main__':
    unittest.main()
