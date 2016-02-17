from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
import jenkins

from pylarion.test_run import TestRun


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id',
                        required=True,
                        action='store',
                        help="Search in specific project id")
    parser.add_argument('--jenkins',
                        required=True,
                        action='store',
                        help="Jenkins server ip/name")
    parser.add_argument('--jenkins-port',
                        action='store',
                        default='8080',
                        help="Jenkins port")
    parser.add_argument('--jenkins-user',
                        required=True,
                        action='store',
                        help="Login with jenkins user")
    parser.add_argument('--jenkins-pass',
                        required=True,
                        action='store',
                        help="Login with jenkins pass")

    return parser.parse_args()


def collect():
    args = parse()
    trs = TestRun.search("project.id:{0} AND status:notrun AND isautomated:true".format(args.project_id))
    jenkins_url = 'http://{}:{}'.format(args.jenkins, args.jenkins_port)
    jenkins_obj = jenkins.Jenkins(jenkins_url, username=args.jenkins_user, password=args.jenkins_pass)
    for tr in trs:
        jenkins_obj.build_job('PolarionTest', {'PROJECT_ID': args.project_id, 'RUN_ID': tr.test_run_id})

if __name__ == '__main__':
    collect()