#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

def _parameter_form():
    return Dictionary(
        elements = {
            "disk_wearout_upper": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Upper percentage treshold for disk wearout"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(90.0, 95.0)),
                ),
                required = True,
            ),
        }
    )

rule_spec_disk_wearout = CheckParameters(
    name = "disk_wearout",
    title = Title("Host group status"),
    topic = Topic.GENERAL,
    parameter_form = _parameter_form,
    condition = HostAndItemCondition(item_title=Title("Disk wearout parameters")),
)