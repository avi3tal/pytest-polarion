import pytest
import time


@pytest.mark.polarion_id("polarion-id-foo-good")
def test_foo_good():
    print "This test is a good one"
    time.sleep(2)
    assert True


@pytest.mark.polarion_id("polarion-id-foo-bed")
def test_foo_bed():
    print "This test is a bed one"
    time.sleep(2)
    assert False, "just being bed"


@pytest.mark.skipif('A' != 'B', reason='Just like that')
@pytest.mark.polarion_id("polarion-id-foo-skipped")
def test_foo_skip():
    print "This test should be skipped"
    time.sleep(2)
    assert False, "just being skip"