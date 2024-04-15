#!/usr/lib/env python3

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Percentage,
    TextInput,
    Tuple,
)
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)

# rule title
def _item_valuespec_disk_wearout():
    return TextInput(
        title="Disk wearout parameters",
        help="Change the parameters of the disk wearout check",
    )

# rule parameters
def _parameter_valuespec_disk_wearout():
    return Dictionary(
        elements=[
            ("disk_wearout_upper",
                Tuple(
                    title=_("Upper percentage treshold for disk wearout"),
                    elements=[
                        Percentage(title=_("Warning"), default_value=90.0),
                        Percentage(title=_("Critical"), default_value=95.0),
                    ],
                )
            ),
        ],
    )

# register rule
rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="disk_wearout",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        item_spec=_item_valuespec_disk_wearout,
        parameter_valuespec=_parameter_valuespec_disk_wearout,
        title=lambda:_("Disk wearout parameters"),
    )
)