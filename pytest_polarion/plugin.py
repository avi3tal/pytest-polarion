from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pytest
import datetime

from pylarion.test_run import TestRun
from pylarion.exceptions import PylarionLibException

from _pytest.runner import runtestprotocol


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
        "polarion_id(id): mark test to run only on polarion id enabled by --polarion-run")


def pytest_addoption(parser):
    group = parser.getgroup('Polarion')
    group.addoption('--polarion-project',
                    default=None,
                    action='store',
                    help='Polarion project name (default: %default)')
    group.addoption('--polarion-run',
                    default=None,
                    action='store',
                    help='Polarion TestRun name (default: %default)')


def polarion_collect_items(config):
    polarion_run = config.getoption('polarion_run')
    polarion_proj = config.getoption('polarion_project')
    tr = TestRun(project_id=polarion_proj, test_run_id=polarion_run)

    # caching TestRun
    config.option.test_run_obj = tr

    items = {rec.test_case_id: rec for rec in tr.records}
    if not items:
        pytest.fail('Failed to collect items from polarion {} run'.format(polarion_run))

    # caching test records
    config.option.test_run_records = items
    return items


def pytest_collection_modifyitems(items, config):
    if config.getoption('polarion_run') is not None:
        politems = polarion_collect_items(config)
        remaining = [colitem for colitem in items if colitem.get_marker('polarion_id').args[0] in politems]
        deselected = set(items) - set(remaining)
        if deselected:
            config.hook.pytest_deselected(items=deselected)
            items[:] = remaining


def pytest_sessionfinish(session, exitstatus):
    # TODO: Generate a final report
    pass


def polarion_set_record(tr, tc):
    try:
        tr.add_test_record_by_object(tc)
    except PylarionLibException:
        tr.reload()
        tr.update_test_record_by_object(tc.test_case_id, tc)


def pytest_runtest_protocol(item, nextitem):
    if item.config.getoption('polarion_run') is not None:
        reports = runtestprotocol(item, nextitem=nextitem)

        # get polarion objects
        tr = item.config.getoption('test_run_obj')
        tc = item.config.getoption('test_run_records')[item.get_marker("polarion_id").args[0]]

        for report in reports:
            if report.when == 'call':
                # print '\n%s --- %s --- %s' % (item.name, item.get_marker("polarion_id"), report.outcome)

                # Build up traceback massage
                trace = ''
                if not report.passed:
                    trace = '{0}:{1}\n{2}'.format(report.location, report.when, report.longrepr)

                tc.result = report.outcome
                tc.executed = datetime.datetime.now()
                tc.executed_by = tc.logged_in_user_id
                tc.duration = report.duration
                tc.comment = trace
                polarion_set_record(tr, tc)
            elif report.when == 'setup' and report.skipped:
                tc.result = 'blocked'
                tc.executed_by = tc.logged_in_user_id
                tc.comment = item.get_marker('skipif').kwargs['reason']
                polarion_set_record(tr, tc)
        # Final polarion record update
        return True


# Currently unable to post only comment since it seem to require status as well
# @pytest.mark.tryfirst
# def pytest_runtest_setup(item):
#     if item.config.getoption('polarion_run') is not None:
#         tr = item.config.getoption('test_run_obj')
#         tc = item.config.getoption('test_run_records')[item.get_marker("polarion_id").args[0]]
#         tc.comment = 'WIP'
#         polarion_set_record(tr, tc)
#     return
