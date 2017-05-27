# -*- coding: utf8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import re
import collections
import posixpath
import threading
import time

import six
from six.moves import configparser

from rally.common.i18n import _  # noqa
from rally.common import logging
from rally.common.plugin import plugin
from rally.common import sshutils
from rally.task import sla


CONFIG_FILENAME = "rackspacetruck.cfg"
"""
Filename of the config. This is not a filepath, this is just a name of
the config.
"""

CONFIG_PATHS = (
    CONFIG_FILENAME,
    posixpath.join(posixpath.expanduser("~"), ".config", CONFIG_FILENAME),
    posixpath.join(posixpath.expanduser("~"), "resources", CONFIG_FILENAME),
    posixpath.join("/", "etc", CONFIG_FILENAME))
"""Paths where to search configs."""

LOG = logging.getLogger(__name__)
"""Logger."""


@six.python_2_unicode_compatible
class Incident(object):
    """Incident contains data about incident on cluster which has to happen."""

    IS_NOT_EXECUTED = -1
    IS_EXECUTION_OK = 0
    IS_EXECUTION_FAILED = 1
    IS_REGEXP_MATCH_FAILED = 2

    SSH_SESSIONS = {}
    """
    Dictionary for SSH sessions (cache). Keys are hostnames, values
    are instances.
    """

    SSH_USER = "root"
    """
    Login of SSH user for cluster nodes. Basically you do not want to
    modify it.
    """

    SSH_PORT = 22
    """
    Port of SSH on cluster nodes. If you change it, it means that you
    definitly doing something wrong. Keep on!
    """

    SESSION_LOCK = threading.RLock()
    """
    Internal lock for sessions. This is required to prevent race
    conditions on session create.
    """

    def __init__(self, action, node, iteration,
                 times, timeout, stdout_regexp, config):
        """Constructor.

        Args:
            action    (str):  A command to execute on remote node.
            node      (str):  A nodename (node-X, compute_1) to refer to.
            iteration (int):  Number of iteration to perform action on.
            config    (dict): Mapping between nodes and IPs.
        """

        self.action = action
        self.node = node
        self.iteration = iteration
        self.stdout_regexp = stdout_regexp
        self.times = times
        self.timeout = timeout
        self.nodes = {}

        # TODO: extract _all to parameter
        if self.node is None or self.node == "localhost":
            self.nodes["localhost"] = "127.0.0.1"
        else:
            if ("_all" in node):
                node_prefix = node[:-len("_all")]
                for node_name, node_ip in config.items():
                    if node_prefix in node_name:
                        self.nodes[node_name] = node_ip
            else:
                self.nodes[self.node] = config[self.node]

        self.status_code = self.IS_NOT_EXECUTED

        # LOG.info("%s: iteration=%s, node=%s, hostname=%s, action=%s",
        #          self.pid, self.iteration, self.node, self.hostname,
        #          self.action)

    def perform(self):
        """Perform action on remote node."""

        class PseudoFile(object):

            def __init__(self):
                self.data = ""

            def write(self, chunk):
                self.data += chunk

        try:
            for node_name, node_ip in self.nodes.items():
                stdout = PseudoFile()
                stderr = PseudoFile()

                LOG.info("Execute action %s on %s(%s)", self.action, node_name, node_ip)
                
                ssh_client = self.get_ssh_client(node_ip)
                code = ssh_client.run(self.action, stdout=stdout, stderr=stderr)
                self.status_code = self.IS_EXECUTION_OK

                LOG.info("Finished execution of '%s' on %s(%s): %s", self.action, node_name, node_ip, code)
                LOG.debug("Incident stdout: %s", stdout.data)
                LOG.debug("Incident stderr: %s", stderr.data)

                if self.stdout_regexp is not None:
                    m = re.compile(self.stdout_regexp, re.DOTALL)
                    if m.match(stdout.data) is None:
                        LOG.error("Regexp {} is not matched".format(self.stdout_regexp))
                        self.status_code = self.IS_EXECUTION_FAILED
        except Exception, e:
            LOG.error(str(e))
            self.status_code = self.IS_EXECUTION_FAILED

    @property
    def id(self):
        """Unique identifier to present incident.

        This id will might be used to present incident (better than id(*)).
        """

        return "\x00".join([self.action, self.node, self.iteration])

    @property
    def pid(self):
        """Unique identifier to present incident within one test run.

        This id might be used to present incident for humans.
        """

        return "incident-{0}".format(id(self))

    @property
    def done(self):
        """Is this incident was performed?"""
        return self.status_code != self.IS_NOT_EXECUTED

    def get_ssh_client(self, node_ip):
        return sshutils.SSH(user=self.SSH_USER, port=self.SSH_PORT, host=node_ip)

    def __str__(self):
        # return six.u(
        #     ("<Incident(id={0}, action='{1}', node='{2}', hostname='{3}', "
        #      "iteration='{4}')>").format(
        #          id(self), self.action, self.node, self.hostname,
        #          self.iteration))
        return ""


@plugin.configure(namespace="openstack", name="truck")
class RackspaceTruck(sla.SLA):
    """Plugin to for long-haul testing.

    RackspaceTruck is a plugin for long-haul testing. Basically it allows to
    perform some actions in cluster during test execution. Actions may
    be performed on certain iterations.
    """

    CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "incidents": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "after_iteration": {
                            "type": "number",
                            "minimum": 0,
                            "exclusiveMinimum": True},
                        "node": {
                            "type": "string",
                            "format": "hostname"},
                        "action": {
                            "type": "string",
                            "minLength": 1},
                        "stdout_regexp" : {
                             "type": "string",
                             "minLength": 1},
                        "times" : {
                             "type": "number",
                             "minimum": 0,
                             "exclusiveMinimum": True},
                        "timeout" : {
                             "type": "number",
                             "minimum": 0,
                             "exclusiveMinimum": True}},
                    "required": ["after_iteration", "node", "action"],
                    "additionalProperties": False}]},
            "context_slas": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "iteration_start": {
                            "type": "number",
                            "minimum": 0,
                            "exclusiveMinimum": True},
                        "iteration_finish": {
                            "type": "number",
                            "minimum": 0,
                            "exclusiveMinimum": True},
                        "sla": {"type": "string"},
                        "parameters": {}},
                    "required": ["iteration_start", "iteration_finish", "sla"],
                    "additionalProperties": False}]}},
        "required": ["incidents", "context_slas"],
        "additionalProperties": False}
    """JSON schema of SLA plugin."""

    CONFIG = {}
    """This has present config for plugin: mapping of nodes to IPs."""

    @classmethod
    def get_config(cls):
        """This reads and returns mapping of nodes to IPs from FS."""

        if cls.CONFIG:
            return cls.CONFIG

        parser = configparser.RawConfigParser()
        parsed = parser.read(CONFIG_PATHS)
        if not parsed:
            LOG.error("Can't read any config from %s", ", ".join(CONFIG_PATHS))
            raise ValueError("Cannot load any config!")
        else:
            LOG.info("Read data from %s", ", ".join(parsed))

        cls.CONFIG.update(parser.items("nodes"))
        LOG.debug("Config for %s is %s", cls.__name__, cls.CONFIG)

        return cls.CONFIG

    def __init__(self, config):
        super(RackspaceTruck, self).__init__(config)

        self.incident_success = True
        self.current_iteration = 1
        self.iteration_lock = threading.RLock()
        self.incidents = self.prepare_incidents(config["incidents"])
        self.context_slas = self.prepare_context_slas(config["context_slas"])
        self.success = True

    def prepare_incidents(self, config):
        """Prepares and creates incident instances.

        Args:
            config (dict): Mapping between nodes and IPs.

        Returns:
            Mapping. Keys are iteration when incident has to be performed.
            Values are corresponding incident instances.

            Please be noticed that incident is performed AFTER iteration.
            This is only possibility to implement such feature.
        """

        incidents = collections.defaultdict(list)

        for incident in config:
            node = incident.get("node", "localhost")
            stdout_regexp = incident.get("stdout_regexp", None)
            times = incident.get("times", 1)
            timeout = incident.get("timeout", 1)
            incidents[incident["after_iteration"]].append(
                Incident(incident["action"], node, incident["after_iteration"],
                         times, timeout, stdout_regexp, self.get_config()))

        return incidents

    def prepare_context_slas(self, config):
        """Prepares and creates SLA instances.

        Args:
            config (dict): Mapping between nodes and IPs.

        Returns:
            Mapping. Keys are tuples (start_iteration, finish_iteration).
            Values are corresponding SLA instances.
        """

        slas = {}

        for cs in config:
            plugin = sla.SLA.get(cs["sla"])

            LOG.debug("Add plugin %s %s", cs["sla"], plugin)

            start = min(cs["iteration_start"], cs["iteration_finish"])
            finish = max(cs["iteration_start"], cs["iteration_finish"])
            slas[(start, finish)] = plugin(cs["parameters"])

        return slas

    def add_iteration(self, iteration):
        self.success = True
        with self.iteration_lock:
            LOG.info("Manage %d iteration.", self.current_iteration)

            for incident in self.incidents[self.current_iteration]:
                for i in range(incident.times):
                    incident.perform()
                    if incident.status_code == incident.IS_EXECUTION_FAILED or incident.status_code == incident.IS_REGEXP_MATCH_FAILED:
                        self.incident_success = False
                    LOG.debug("Sleeping %s seconds...", incident.timeout)
                    time.sleep(incident.timeout)

            for (start, finish), csla in six.iteritems(self.context_slas):
                if start <= self.current_iteration <= finish:
                    self.success &= csla.add_iteration(iteration)

            self.current_iteration += 1

        self.success &= self.incident_success
        return self.success

    def merge(self, other):
        # TODO(sarkhipov): Have no idea how to implement merge function
        #                  on structure which is not semilattice.
        return self

    def details(self):
        slas = [_("SLA ({0}, {1}): {2}").format(start, finish, sla.details())
                for (start, finish), sla
                in sorted(six.iteritems(self.context_slas))]

        incidents = []
        for it, actions in sorted(six.iteritems(self.incidents)):
            for action in actions:
                code = action.status_code if action.done else "N/A"
                incidents.append(_("Incident at {0}: {1}").format(it, code))

        return "\n".join(slas + incidents)
