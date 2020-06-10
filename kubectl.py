#!/bin/python

import yaml
import pprint
import os
import sys
import subprocess
from pathlib import Path

EXE_PATH = '/usr/bin/kubectl'
PROXY_DICT = {'cluster': 'proxy'}
NO_PROXY = 'googleapis.com'
conf = None

def pretty_print_conf(yaml):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(yaml)

def get_current_context(yaml):
    return yaml['current-context']

def get_current_cluster(ctx, yaml):
    for context in yaml['contexts']:
        if ctx == context['name']:
            return context['context']['cluster']

def get_proxy(cluster_name):
    if not cluster_name in PROXY_DICT:
        return None
    return PROXY_DICT[cluster_name]

def set_proxy_env_var(proxy):
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['NO_PROXY'] = NO_PROXY

def launch_kubectl():
    # print(os.environ.copy())
    subprocess.run([EXE_PATH] + sys.argv[1:])

with open(Path.home().as_posix() + "/.kube/config", 'r') as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# pretty_print_conf(conf)
cc = get_current_context(conf)
cl = get_current_cluster(cc, conf)
proxy = get_proxy(cl)
# print(proxy)

if proxy:
    set_proxy_env_var(proxy)

launch_kubectl()
