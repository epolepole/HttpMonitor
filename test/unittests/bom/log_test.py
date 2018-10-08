import datetime

import pytest

from common.bom.log_parser import LOG_TIMESTAMP_FORMAT, LogParser


def test_create_simple_bom_log():
    a_bom_log_1 = LogParser(r'127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234').parse()
    assert a_bom_log_1.resource == '/report'
    assert a_bom_log_1.timestamp == datetime.datetime.strptime('09/May/2018:16:00:39 +0000', LOG_TIMESTAMP_FORMAT)
    assert a_bom_log_1.timestamp.second == 39
    a_bom_log_2 = LogParser(r'127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234').parse()
    assert a_bom_log_2.resource == '/api/user'
    assert a_bom_log_2.timestamp == datetime.datetime.strptime('09/May/2018:16:00:41 +0000', LOG_TIMESTAMP_FORMAT)
    assert a_bom_log_2.timestamp.second == 41


def test_wrong_common_format_input_raises_exception():
    wrong_log = 'This is a wrong log format'
    with pytest.raises(ValueError) as ex_info:
        LogParser(wrong_log).parse()
    assert 'Wrong log format for {}'.format(wrong_log) in str(ex_info.value)


def test_log_with_missing_element_raises_exception():
    missing_el_log = r'127.0.0.1 james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234'
    with pytest.raises(ValueError) as ex_info:
        LogParser(missing_el_log).parse()
    assert 'Wrong log format for {}'.format(missing_el_log) in str(ex_info.value)
