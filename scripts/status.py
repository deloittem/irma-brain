#!/usr/bin/env python

import config.parser as config
from celery import Celery

import pymongo
import amqp
import requests
import libvirt

FRONTEND_TEST_URL = "http://frontend.irma.qb/"
FRONTEND_API_TEST_URL = "http://frontend.irma.qb/_api/probe/list"


scan_app = Celery('scan')
config.conf_brain_celery(scan_app)

probe_app = Celery('probe')
config.conf_probe_celery(probe_app)

frontend_app = Celery('frontend')
config.conf_frontend_celery(frontend_app)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

status_ok = 0
status_ko = 1
status_str = [bcolors.OKGREEN + "[+]" + bcolors.ENDC, bcolors.FAIL + "[-]" + bcolors.ENDC]

def print_hdr(msg):
    print
    print bcolors.HEADER + "## {0} ##".format(msg) + bcolors.ENDC
    print

def print_msg(code_msg_list):
    for (status, line) in code_msg_list:
        print '\t',
        print status_str[status], line

def ping_celery_app(celery):
    try:
        res = []
        ping_status = celery.control.ping(timeout=0.5)
        if len(ping_status) == 0:
            res.append((status_ko, 'celery app {0} is down'.format(celery.main)))
        for r in ping_status:
            for host, response in r.items():
                if response['ok'] == u'pong':
                    res.append((status_ok, 'celery app {0} is up and running'.format(host)))
                else:
                    res.append((status_ko, 'celery app {0} is down'.format(host)))
        queues = celery.control.inspect().active_queues()
        for (host, infolist) in queues.items():
            queuenames = "-".join([info['name'] for info in infolist])
            res.append((status_ok, '\t| {0} queue {1}'.format(host, queuenames)))
    except:
        res.append((status_ko, 'no celery running perhaps broker is down on %s' % celery.conf['BROKER_URL']))
    return res

def ping_db(uri):
    try:
        pymongo.Connection(uri)
        return [(status_ok, 'mongodb {0} is up and runnning'.format(uri))]
    except:
        return [(status_ko, 'mongodb {0} is down'.format(uri))]

def ping_rabbitmq(address, port, usr, pwd, vhost):
    try:
        amqp.Connection(host='{address}:{port}'.format(address=address, port=port), userid=usr, password=pwd, virtual_host=vhost)
        return [(status_ok, 'rabbitmq vhost {vhost} on {address} is up and runnning'.format(vhost=vhost, address=address))]
    except:
        return [(status_ko, 'rabbitmq vhost {vhost} on {address} is down'.format(vhost=vhost, address=address))]

def ping_frontend(url):
    try:
        requests.get(url=url)
        return [(status_ok, 'frontend {0} is up and runnning'.format(url))]
    except:
        return [(status_ko, 'frontend {0} is down'.format(url))]

def ping_libvirt(uri):
    try:
        libvirt.open(uri)
        return [(status_ok, 'libvirt {0} is up and runnning'.format(uri))]
    except:
        return [(status_ko, 'libvirt {0} is down'.format(uri))]
    return

print_hdr("RabbitMQ")
for broker in [ 'broker_brain', 'broker_probe', 'broker_frontend']:
    print_msg(ping_rabbitmq(config.brain_config[broker].host, config.brain_config[broker].port, config.brain_config[broker].username, config.brain_config[broker].password, config.brain_config[broker].vhost))

print_hdr("Frontend")
print_msg(ping_frontend(FRONTEND_TEST_URL))

print_hdr("Frontend Api")
print_msg(ping_frontend(FRONTEND_API_TEST_URL))

print_hdr("Celery")
for app in [scan_app, probe_app, frontend_app]:
    print_msg(ping_celery_app(app))
print
