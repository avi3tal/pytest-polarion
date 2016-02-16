from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pytest

from pylarion.test_run import TestRun
from pytest_polarion.utils import id_generator


def pytest_addoption(parser):
    group = parser.getgroup('Polarion')
    group.addoption('--polarion-template',
                    default=None,
                    action='store',
                    help='Polarion TestTemplate name (default: %default)')
    group.addoption('--field',
                    default=[],
                    action='append',
                    help='Parameterized fields')


@pytest.mark.tryfirst
def pytest_cmdline_main(config):
    if config.getoption('polarion_template') is not None and \
            not config.getoption('collectonly'):
        fields = {field.split('=')[0]: field.split('=')[1] for field in config.getoption('field')}

        # generate TestRun name out of given Fields
        # otherwise, adding random 4 chars string as suffix
        tr_name = config.getoption('polarion_template')
        for f in fields.items():
            tr_name += '-{0}_{1}'.format(*f)
        if tr_name == config.getoption('polarion_template'):
            tr_name += '-random_{}'.format(id_generator())

        tr_name = tr_name.replace('.', '_')

        tr = TestRun.create(project_id=config.getoption('polarion_project'),
                            test_run_id=tr_name,
                            template=config.getoption('polarion_template'))

        for k, v in fields.iteritems():
            try:
                setattr(tr, k, v)
            except AttributeError:
                print('Failed to set attribute {}={}'.format(k, v))
        # tr.build = fields.get('build', '')
        tr.update()
        config.option.polarion_run = tr_name