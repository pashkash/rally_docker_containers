import time
import re

from rally import consts
from rally.common import logging
from rally import exceptions
from rally.plugins.openstack import scenario
from rally.task import atomic
from rally.task import utils
from rally.task import validation

LOG = logging.getLogger(__name__)

class LongevityScenario(scenario.OpenStackScenario):
    
    @atomic.action_timer("longevity.sleep")
    def _sleep(self, seconds):
        time.sleep(seconds)

    @atomic.action_timer("longevity.list_stacks")
    def _list_stacks(self):
        return list(self.clients("heat").stacks.list())

    @atomic.action_timer("longevity.list_servers")
    def _list_servers(self):
        return list(self.clients("nova").servers.list())

    @validation.required_services(consts.Service.HEAT)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def check_stack_status_and_sleep(self, seconds, stack_status):
        passed = True
        try:
            stacks = self._list_stacks()
        except Exception:
            LOG.error("Failed to list stacks")
            passed = False
        if passed:
            for stack in stacks:
                if stack.stack_status != stack_status:
                    passed = False
        LOG.debug("Sleeping {} seconds...".format(seconds))
        self._sleep(seconds)
        if not passed:
            raise Exception()

    @validation.required_services(consts.Service.NOVA)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def check_server_logs_and_sleep(self, seconds, log_regexp):
        m = re.compile(log_regexp, re.DOTALL)
        passed = True
        try:
            servers = self._list_servers()
        except Exception:
            LOG.error("Failed to list servers")
            passed = False
        if passed:
            for server in servers:
                log = server.get_console_output()
                LOG.debug("Server {} log:\n{}".format(server, log))
                if m.match(log) is None:
                    passed = False
        LOG.debug("Sleeping {} seconds...".format(seconds))
        self._sleep(seconds)
        if not passed:
            raise Exception()
