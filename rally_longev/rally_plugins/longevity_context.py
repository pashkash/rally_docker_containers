from rally.common.i18n import _
from rally.common import logging
from rally.common import utils as rutils
from rally import consts
from rally.plugins.openstack.cleanup import manager as resource_manager
from rally.plugins.openstack.scenarios.heat import utils as heat_utils
from rally.task import context

LOG = logging.getLogger(__name__)

@context.configure(name="do_not_cleanup", order=900)
class DoNotCleanupContext(context.Context):

    @logging.log_task_wrapper(LOG.info, _("Exit context: `DoNotCleanupContext`"))
    def cleanup(self):
        pass

@context.configure(name="longevity_stacks", order=901)
class LongevityStackGenerator(context.Context):

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,

        "properties": {
            "nof_stacks": {
                "type": "integer",
                "minimum": 1
            },
            "nof_instances_per_stack": {
                "type": "integer",
                "minimum": 1
            },
            "template_path": {
                "type": "string",
                "min_length": 1
            }
        },
        "additionalProperties": False
    }

    DEFAULT_CONFIG = {
    	"nof_stacks": 1,
        "nof_instances_per_stack": 1,
        "template_path": ""
    }

    @logging.log_task_wrapper(LOG.info, _("Enter context: `LongevityStackGenerator`"))
    def setup(self):
        with open(self.config["template_path"], "r") as template_file:
            template_data = template_file.read()
        for user, tenant_id in rutils.iterate_per_tenants(self.context["users"]):
            heat_scenario = heat_utils.HeatScenario({"user": user, "task": self.context["task"]})
            self.context["tenants"][tenant_id]["stacks"] = []
            for i in range(self.config["nof_stacks"]):
                stack = heat_scenario._create_stack(template_data, parameters={"nof_instances": self.config["nof_instances_per_stack"]})
                self.context["tenants"][tenant_id]["stacks"].append(stack.id)
    
    @logging.log_task_wrapper(LOG.info, _("Exit context: `LongevityStackGenerator`"))
    def cleanup(self):
        resource_manager.cleanup(names=["heat.stacks"],
                                 users=self.context.get("users", []))

