import pytest
import time


@pytest.mark.polarion_id("CMP-9301")
def test_foo_good():
    print "This test is a good one"
    time.sleep(3)
    assert True


@pytest.mark.polarion_id("CMP-9307")
def test_foo_bad():
    print "This test is a bad one"
    time.sleep(3)
    assert False, "just being bad"


@pytest.mark.skipif('A' != 'B', reason='Just like that')
@pytest.mark.polarion_id("CMP-9306")
def test_foo_skip():
    print "This test should be skipped"
    time.sleep(2)
    assert False, "just being skip"