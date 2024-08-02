import unittest

from divs import get_yesterday


def test__get_yesterday():
    test_date = '2023-01-06'
    except_date = '2023-01-05'
    assert get_yesterday(test_date) == except_date

if __name__ == '__main__':
    unittest.main()