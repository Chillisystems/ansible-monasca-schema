#!/usr/bin/python
#
# (c) 2016, Adam Hamsik <haaaad () gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

DOCUMENTATION = '''
---
module: kafka_topics
version_added: "2.2"
short_description: Use kafka-topics.sh tool to create/destroy topics.
description:
  - This is a wrapper module around kafka-topics.sh to create/destroy topics with given configuration.
options:
  zookeeper_server:
    description:
      - Zookeeper server url in form <ip>:<port>, where kafka is connected to.
    required: True
    default: localhost:2181
  replication_factor:
    description:
      - Defined replication factor for kafka topic.
    required: False
    default: 1
    aliases: ['replication']
  partitions:
    description:
      - Number of partitions to create for given kafka topic.
    required: False
    default: 1
  topic:
    description:
      - Name of topic to create/destroy.
    required: True
    default: null
  executable:
    description:
      - Path to kafka-topics.sh script if it's not installed in standard path.
    required: False
  state:
    description:
      - Defines action which can be either certificate import or removal.
    choices: [ 'present', 'absent' ]
    default: 'present'
    required: false
author: Adam Hamsik
'''

EXAMPLES = '''
# Create new kafka topic called test on zookeeper server running on localhost.
kafka_topics:
  state: present
  executable: /opt/kafka/bin/kafka_topics.sh
  topic: test
  partitions: 2
  replication_factor: 2
  zookeeper_server: localhost:2181
'''

RETURN = '''

'''

try:
    import json
except ImportError:
    import simplejson as json

import sys

def check_kafka_topic_present(module, cmd, topic, zookeeper):
    ''' Check if kafka topic exists '''
    cmd = "%s --list --zookeeper %s --topic %s" % (cmd, zookeeper, topic)

    (rc, out, err) = module.run_command(cmd, check_rc=True)


def kafka_create_topic(module, cmd, topic, zookeeper, partitions, replication):
    ''' Create new kafka topic '''
    cmd = "%s --create --zookeeper %s --replication-factor %d --partitions %d --topic %s" % (cmd, zookeeper, replication, partitions, topic)
    # stdout: Created topic "test2".
    (rc, out, err) = module.run_command(cmd, check_rc=True)
    return True

def kafka_delete_topic(module, cmd, topic, zookeeper):
    ''' Delete existing kafka-topic '''
    cmd = "%s --create --zookeeper %s --topic %s" % (cmd, zookeeper, topic)
    # Topic test2 is marked for deletion.
    # Note: This will have no impact if delete.topic.enable is not set to true.
    (rc, out, err) = module.run_command(cmd, check_rc=True)

    return True

def test_kafka_topics(module, cmd):
    ''' Test if kafka-topics.sh is actuall executable or not '''

    (rc, del_out, del_err) = module.run_command(cmd, check_rc=True)


def main():
    argument_spec = dict(
            zookeeper = dict(required=True, type='str'),
            executable = dict(required=False, default='kafka-topics.sh', type='str'),
            topic = dict(required=True, type='str'),
            partitions = dict(required=False, default=1, type='int'),
            replication_factor = dict(required=False, default=1, type='int'),
            state = dict(required=False, default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    filter = {}
    zookeeper = module.params.get('zookeeper')
    cmd = module.params.get('executable')
    topic = module.params.get('topic')
    partitions = module.params.get('partitions')
    replication_factor = module.params.get('replication_factor')
    state = module.params.get('state')

    test_kafka_topics(module, cmd)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()