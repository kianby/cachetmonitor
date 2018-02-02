#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import subprocess
from clize import clize, run
from conf import schema
from jsonschema import validate
import cachetclient.cachet as cachet

COMPONENT_STATUS_OK = 1
COMPONENT_STATUS_KO = 4

lxcls_pattern = re.compile('(\d+)\s+(\w+)\s+\d\s+')


def monitor(conf):

    # /ping
    #ping = cachet.Ping(endpoint=conf['api_url'])
    # print(ping.get())

    # retrieve component list
    components = cachet.Components(
        endpoint=conf['api_url'], api_token=conf['api_token'])
    json_components = json.loads(components.get())

    # a dict where key is id and value is component struct
    component_dict = dict()
    for component in json_components['data']:
        #print('id {} name {}'.format(component['id'], component['name']))
        component['processed'] = False
        component_dict[component['name']] = component

    # check LXC
    if conf['lxc_check']:
        output = str(subprocess.check_output(
            ['lxc-ls', '-f'], universal_newlines=True))
        for line in output.splitlines():
            r = re.match(lxcls_pattern, line)
            if r:
                name = 'container-' + r.group(1)
                state = r.group(2)
                #print('name {} state {}'.format(name, state))
                component = component_dict.get(name, None)
                if component:
                    status = COMPONENT_STATUS_KO
                    if state == 'RUNNING':
                        status = COMPONENT_STATUS_OK
                    print('update {} => {}'.format(name, status))
                    components.put(id=component['id'], status=status)
                    component['processed'] = True

    # test URL

    # scrap Web page

    # assume all unprocessed components are KO
    for component in component_dict.values():
        if not component['processed']:
            components.put(id=component['id'], status=COMPONENT_STATUS_KO)


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
