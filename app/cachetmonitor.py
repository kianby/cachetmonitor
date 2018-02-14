#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import subprocess
import requests
from clize import clize, run
from conf import schema
from jsonschema import validate
import cachetclient.cachet as cachet

COMPONENT_STATUS_OK = '1'
COMPONENT_STATUS_KO = '4'

lxcls_pattern = re.compile('(\d+)\s+(\w+)\s+\d\s+')


def check_url(url, regex):

    try:
        response = requests.request("GET", url)
        if re.search(regex, response.text):
            success = True
            cause = ''
        else:
            success = False
            cause = 'not_found'
    except:
        success = False
        cause = 'timeout'
    return {'success': success, 'cause': cause}


def monitor(conf):

    # retrieve component list
    components = cachet.Components(
        endpoint=conf['api_url'], api_token=conf['api_token'])
    json_components = json.loads(components.get())

    # dict where key is id and value is component struct
    component_dict = dict()
    for component in json_components['data']:
        component['processed'] = False
        component['newstatus'] = component['status']
        component_dict[component['name']] = component

    # check LXC
    if conf['lxc']['check']:
        output = str(subprocess.check_output(
            ['lxc-ls', '-f'], universal_newlines=True))
        for line in output.splitlines():
            r = re.match(lxcls_pattern, line)
            if r:
                name = conf['lxc']['component_prefix'] + r.group(1)
                state = r.group(2)
                component = component_dict.get(name, None)
                if component:
                    component['processed'] = True
                    if state == 'RUNNING':
                        component['newstatus'] = COMPONENT_STATUS_OK
                    else:
                        component['newstatus'] = COMPONENT_STATUS_KO

    # check URLs
    if conf['url']['check']:
        for endpoint in conf['url']['endpoints']:
            component = component_dict.get(endpoint['component'], None)
            if component:
                component['processed'] = True
                r = check_url(endpoint['url'], endpoint['regex'])
                if r['success']:
                    component['newstatus'] = COMPONENT_STATUS_OK
                else:
                    component['newstatus'] = COMPONENT_STATUS_KO

    # send status to CacheHQ for changed and unprocessed components
    for component in component_dict.values():

        if not component['processed']:
            component['newstatus'] = COMPONENT_STATUS_KO

        if component['newstatus'] != component['status']:
            # print(component)
            components.put(id=component['id'],
                           status=component['newstatus'])


def load_json(filename):
    jsondoc = None
    with open(filename, 'rt') as json_file:
        jsondoc = json.loads(json_file.read())
    return jsondoc


@clize
def cachet_monitor(config_pathname):

    # load and validate startup config
    conf = load_json(config_pathname)
    json_schema = json.loads(schema.json_schema)
    validate(conf, json_schema)

    monitor(conf)

if __name__ == '__main__':
    run(cachet_monitor)
