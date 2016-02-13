import pytest
from _pytest.runner import runtestprotocol
from _pytest.main import EXIT_OK, EXIT_TESTSFAILED


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
        "polarion_id(id): mark test to run only on polarion id enabled by --polarion-run")


def pytest_addoption(parser):
    group = parser.getgroup('Polarion')
    group.addoption('--polarion-run',
                    default=None,
                    action='store',
                    help='Polarion TestRun name (default: %default)')


def polarion_collect_items(polarion_run):
    print 'Collecting test cases IDs from', polarion_run
    # FIXME: collect items from polarion using pylarion
    items = ['polarion-id-foo-good', 'polarion-id-foo-bed']
    if not items:
        pytest.fail('Failed to collect items from polarion {} run'.format(polarion_run))
    return items


def pytest_collection_modifyitems(items, config):
    if config.getoption('polarion_run') is not None:
        politems = polarion_collect_items(config.getoption('polarion_run'))
        remaining = [colitem for colitem in items if colitem.get_marker('polarion_id').args[0] in politems]
        deselected = set(items) - set(remaining)
        if deselected:
            config.hook.pytest_deselected(items=deselected)
            items[:] = remaining


def pytest_sessionstart(session):
    # move TestRun status to IN PROGRESS
    # FIXME: use pylarion to notify polarion run status
    print "Test Run IN PROGRESS"


def pytest_sessionfinish(session, exitstatus):
    # move TestRun status to DONE
    if exitstatus in [EXIT_OK, EXIT_TESTSFAILED]:
        # FIXME: use pylarion to notify polarion run status
        print "Test Run DONE"
    # TODO: generate a report


# @pytest.mark.hookwrapper
def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    # yield True
    for report in reports:
        if report.when == 'call':
            # move test case to the relevant status
            # FIXME: use pylarion to notify polarion case status
            print '\n%s --- %s --- %s' % (item.name, item.get_marker("polarion_id"), report.outcome)
            print "Test Case DONE"
    # return True


@pytest.mark.hookwrapper
def pytest_runtest_logreport(report):
    if report.when == 'setup':
        # move test case to IN PROGRESS
        # FIXME: use pylarion to notify polarion case status
        print "Test Case IN PROGRESS"
    yield
    if report.outcome == "skipped":
        # move test case to relevant mode
        # FIXME: use pylarion to notify polarion case status
        print "Test Case IGNORED"