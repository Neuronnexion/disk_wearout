#!/usr/bin/env python3

# Exemple of raw data from agent
#
# <<<disk_wearout:sep(59)>>>
# /dev/sda;CT1000MX500SSD1;2152E5F6FEB6;22;56;0
# /dev/sdb;CT1000MX500SSD1;2152E5F6D6E6;22;48;0
# /dev/sdc;CT1000MX500SSD1;2152E5F6E85B;23;51;0
# /dev/sdd;CT1000MX500SSD1;2152E5F6C8B0;25;33;0
# /dev/sde;CT1000MX500SSD1;2248E68C7DA4;2;49;0
# /dev/sdf;CT1000MX500SSD1;2210E616E034;105;63;0
# /dev/sdg;CT1000MX500SSD1;2152E5F6C89A;23;59;0
# /dev/sdh;CT1000MX500SSD1;2152E5F6C89D;31;54;0

from .agent_based_api.v1 import check_levels, Metric, register, Result, Service, State

# parse raw data from agent on host into a dict
def parse_disk_wearout(string_table):
    parsed = {}
    column_names=[
        "model",
        "serial",
        "wearout",
        "unused",
        "rain",
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

    unused=int(percent_wear['unused'])
    rain=int(percent_wear['rain'])

    # get parameters
    crit_wearout=int(params["disk_wearout_upper"][1])
    warn_wearout=int(params["disk_wearout_upper"][0])

    if int_wearout >= crit_wearout:
        yield Result(state=State.CRIT, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%. Available spare blocks: {unused}. Number of RAIN events: {rain}")
    elif int_wearout >= warn_wearout:
        yield Result(state=State.WARN, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%. Available spare blocks: {unused}. Number of RAIN events: {rain}")
    else:
        yield Result(state=State.OK, summary=f"Wearout of disk {model}-{serial} at {int_wearout}%. Available spare blocks: {unused}. Number of RAIN events: {rain}")

    # metrics

    yield Metric(
        name="Disk_wearout",
        value=int_wearout,
        boundaries=(0.0, 100.0)
    )

    yield Metric(
        name="Available_spare_blocks",
        value=unused,
        boundaries=(0.0, None),
    )

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