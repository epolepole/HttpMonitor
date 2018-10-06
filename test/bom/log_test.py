import pytest

from bom.log_builder import LogBuilder


def test_create_simple_bom_log():
    a_bom_log_1 = LogBuilder(r'127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234').get_log()
    assert a_bom_log_1.section == 'report'
    a_bom_log_2 = LogBuilder(r'127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234').get_log()
    assert a_bom_log_2.section == 'api'


def test_wrong_common_format_input_raises_exception():
    wrong_log = 'This is a log without section'
    with pytest.raises(ValueError) as ex_info:
        LogBuilder(wrong_log).get_log()
    assert 'Section not found in {}'.format(wrong_log) in str(ex_info.value)
