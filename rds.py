# -*- coding: utf-8 -*-
import boto
import time
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from global_conf import *
from conf.parse_config import parse_ini


@task(default=True)
def list():
    '''List All Relational Data Service'''
    print(_green("Listing databases..."))
    rds = boto.connect_rds(ec2_key, ec2_secret)
    instances = rds.get_all_dbinstances()

    x = _pretty_table(
        ["RDS ID", "Create date", "Engine", "Status", "Port", "Address"])
    for i in instances:
        x.add_row(
            [i.id, i.create_time, i.engine, i.status, i._port, i._address])

    print(_yellow(x))
