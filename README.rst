===============
pytest-polarion
===============
pytest-polarion is a pytest plugin to collect test cases and report result in realtime.
The plugin will support different Polarion modes such as executing specific TestRun or even generate a TestRun out of given Template.
It will also support parametrizing test runs out of Template.

Basically, the plugin is divided to two phases:
The first phase related to how pytest collect test cases. Originally, pytest uses specific test pattern while reading filesystem (test files and test directories).
This plugin will extend this pattern matcher and compare the collected test cases with the test cases assign to given TestRun.
This way, we'll be able to define a TestRun along with the desired test cases and then call ``py.test --polarion-run <run name>`` to execute specifically what the Run describes.

The second phase is actually the reporting engine that executed in realtime. The intention is to show WIP report to TestRun and test cases.
Meaning that when executing pytest with specific TestRun, assuming test run status is "Not Run", the status will immediately moved to "In Progress" and also
every test cases will move to "In Progress" while start executing it and then to "Done" when it is finished.

Also at the end of entire session execution, pytest-polarion will be capable of generating a Report.

The awesome part of this plugin is the fact that it can simply triggered by Jenkins job so we can basically define a CI process to collect all TestRuns that are in "Not Run" status
and make it execute/report automatically.


Documentation
-------------
...

Commands
--------
Trigger test from TestRun::

    $ py.test --polarion-project <name> --polarion-run <run name>

Generate TestRun from template and trigger automatically::

    $ py.test --polarion-project <name> --polarion-template <temp name> --field "build=5.5.2" --field "provider=OSE"

Note that ``--field`` is an append type argument, supporting multiple fields

Authors
-------
`Avi Tal <atal@redhat.com>`_
