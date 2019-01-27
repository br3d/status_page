#! /usr/bin/env python3
#https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

# import requests, boto3
from jinja2 import Template

# namespace = 'status'
# name_purpose = 'github.com'
# url = 'https://github.com'
# aws_region = 'eu-west-1'

# status_template = 'template.html'


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




def make_statuspage():
	template = Template(open(status_template,'r').read())
	return (template.render(allhosts = allhosts)
	
def write_status_page(body):
	f = open(report_name,'rb+')
	f.write(bytes(body, 'UTF-8'))
	f.close

host1.status = False
host1.url = 'http://falsecheck.ru'
host2.status = True
host2.url = 'http://truecheck.ru'
host3.status = True
host3.url = 'http://truetruecheck.ru'


allhosts = [host1,host2,host3]

write_status_page(make_statuspage())
