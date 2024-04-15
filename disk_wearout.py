#!/usr/bin/env python3

# Exemple of raw data from agent
#
# <<<disk_wearout:sep(59)>>>
# /dev/sda;20,CT1000MX500SSD1,2152E5F6FEB6
# /dev/sdb;19,CT1000MX500SSD1,2152E5F6D6E6
# /dev/sdc;21,CT1000MX500SSD1,2152E5F6E85B
# /dev/sdd;22,CT1000MX500SSD1,2152E5F6C8B0
# /dev/sde;99,CT1000MX500SSD1,2152E5F6D1C8
# /dev/sdf;95,CT1000MX500SSD1,2210E616E034
# /dev/sdg;20,CT1000MX500SSD1,2152E5F6C89A
# /dev/sdh;28,CT1000MX500SSD1,2152E5F6C89D

from .agent_based_api.v1 import check_levels, Metric, register, Result, Service, State

# parse raw data from agent on host into a dict
def parse_disk_wearout(string_table):
    parsed = {}
    column_names=[
        "wearout",
        "model",
        "serial",
    ]
    for line in string_table:
        parsed [line[0]] = {}
        for n in range(0, len(column_names)):
            parsed[line[0]][column_names[n]]=line[n+1]
    return parsed

# discovery function for creating multiple services
def discover_disk_wearout(section):
    for group in section:
        yield Service(item=group)

# the actual check function
def check_disk_wearout(item, params, section):
    # get all items from a dict column into a var
    percent_wear = section.get(item)

    # convert disk wearout % into an int
    int_wearout=int(percent_wear['wearout'])

    model=percent_wear['model']
    serial=percent_wear['serial']

    # get parameters
    crit_wearout=int(params["disk_wearout_upper"][1])
    warn_wearout=int(params["disk_wearout_upper"][0])

    if int_wearout >= crit_wearout:
        yield Result(state=State.CRIT, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%")
    elif int_wearout >= warn_wearout:
        yield Result(state=State.WARN, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%")
    else:
        yield Result(state=State.OK, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%")

    # metrics
    yield from check_levels(
        int_wearout,
        levels_upper=(float(warn_wearout),float(crit_wearout)),
        label="Disk wearout",
        boundaries=(0.00,100.00),
        notice_only=True,
    )

    yield Metric(name="Wearout", value=int_wearout)

# register agent
register.agent_section(
    name = "disk_wearout",
    parse_function = parse_disk_wearout,
)

# register check for multiple services (%s is the header of a dict column)
register.check_plugin(
    name = "disk_wearout",
    sections = ["disk_wearout"],
    service_name = "Disk wearout %s",
    discovery_function = discover_disk_wearout,
    check_function = check_disk_wearout,
    check_default_parameters={"disk_wearout_upper": (90,95)},
    check_ruleset_name="disk_wearout",
)