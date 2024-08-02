import unittest

from divs import get_currency_index


def test__get_yesterday():
    test_data_1 = [{'cad': {0: {'effectiveDate': '2023-01-02', 'mid': 3.2306}, 1: {'effectiveDate': '2023-01-03', 'mid': 3.2593}}}]
    test_data_2 = [{'cad': {0: {'effectiveDate': '2023-01-02', 'mid': 3.2306}}}, {'usd': {0: {'effectiveDate': '2023-01-02', 'mid': 4.3811}}}]
    test_data_3 = []
    expected_result_1 = [{'currency': 'cad', 'index': 0}]
    expected_result_2 = [{'currency': 'cad', 'index': 0}, {'currency': 'usd', 'index': 1}]
    expected_result_3 = []
    assert get_currency_index(test_data_1) == expected_result_1
    assert get_currency_index(test_data_2) == expected_result_2
    assert get_currency_index(test_data_3) == expected_result_3

if __name__ == '__main__':
    unittest.main()