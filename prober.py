#! /usr/bin/env python3
# https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

import requests
import boto3
from jinja2 import Template
import time

cw_namespace = 'status'
purpose_list = {'github.com': 'https://github.com',
                'keencode.net': 'http://keencode.net'}
result_list = []
url = 'https://github.com'
aws_region = 'eu-west-1'

report_name = 'index.html'
status_template = 'static/template.html'


class host_o():
    name = ''
    url = ''
    status = False


def cw_report(cw_namespace, name, val):
    conn_cw = boto3.client('cloudwatch')
    conn_cw.put_metric_data(
        MetricData=[
            {
                'MetricName': name,
                'Unit': 'Count',
                'Value': val
            },
        ],
        Namespace=cw_namespace
    )


def check_status(url):
    response = requests.get(url)
    return response


def check_successful(response):
    if response.status_code == 200:
        return True
    else:
        return False

def make_statuspage(allhosts, dtime):
    template = Template(open(status_template, 'r').read())
    return template.render(hosts=allhosts, gtime=dtime)


def write_status_page(body):
    f = open(report_name, 'w+')
    f.write(body)
    f.close


def time_now():
    return time.strftime("%Y-%m-%d %H:%M")


def lambda_handler(var, var2):
    for purpose in purpose_list:
        item = host_o()
        response = check_status(purpose_list[purpose])
    # build CW metric
        cw_report(cw_namespace, purpose, response.status_code)
    # fill object fields
        item.name = purpose
        item.url = purpose_list[purpose]
        item.status = check_successful(response)
    # collect results
        result_list.append(item)
    # generate status page
    print(make_statuspage(result_list, time_now()))
