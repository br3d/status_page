#! /usr/bin/env python3
#https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

# import requests, boto3
from jinja2 import Template
import time

# namespace = 'status'
# name_purpose = 'github.com'
# url = 'https://github.com'
# aws_region = 'eu-west-1'

report_name = 'index.html'
status_template = 'template.html'


# def cw_report(namespace, name, val):
# 	conn_cw = boto3.client('cloudwatch')
# 	conn_cw.put_metric_data(
#     MetricData=[
#         {
#             'MetricName': 'response code',
#             'Unit': 'Count',
#             'Value': val
#         },
#     ],
#     Namespace = namespace
# )
	
# def check_status(url):
# 	response = requests.get(url)
# 	return response

# def lambda_handler(var, var2):
#     status = check_status(url)
#     cw_report(namespace, name_purpose, status.status_code)
#     print(status.status_code)




def make_statuspage(allhosts, dtime):
	template = Template(open(status_template,'r').read())
	return template.render(hosts = allhosts, gtime = dtime )
	
def write_status_page(body):
	f = open(report_name,'w+')
	f.write(body)
	f.close

def time_now():
	return time.strftime("%Y-%m-%d %H:%M")

class hosto():
	status = True
	url = ''


host1 = hosto()
host2 = hosto()
host3 = hosto()
host1.status = False
host1.url = 'http://falsecheck.ru'
host2.status = True
host2.url = 'http://truecheck.ru'
host3.status = True
host3.url = 'http://truetruecheck.ru'


allhosts = [host1,host2,host3]
# print(make_statuspage(allhosts))
write_status_page(make_statuspage(allhosts, time_now()))
