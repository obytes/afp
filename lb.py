# -*- coding: utf-8 -*-
import time
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from conf.parse_config import parse_ini


recipe = None


@task(default=True)
def list():
    """
    list load balancers
    """
    start_time = time.time()
    print(_green("Listing load balancers..."))
    x = _pretty_table(["Load balancer ID", "Public DNS", "Instances"])
    from misc import _get_lb

    for lb in _get_lb():
        x.add_row([lb.name, lb.dns_name, lb.instances])
    print(_green(x))
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))

@task()
def register_instance_in_lb(lb_name, *args):
    """
    set load balancer, assigns an instance to a given load balancer
    """
    start_time = time.time()
    print(_green("Assigning instance to load balancer %s..." % lb_name))

    from misc import _register_instance_in_lb
    if _register_instance_in_lb(lb_name, *args):
        print(_green('Instance(s) registered to load balancer'))
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))

@task()
def deregister_instance_from_lb(lb_name, *args):
    """
    delete instance from load balancer
    """
    start_time = time.time()
    print(_green("De-assigning instance from load balancer %s..." % lb_name))

    from misc import _deregister_instance_from_lb
    if _deregister_instance_from_lb(lb_name, *args):
        print(_green('Instance(s) de-registered from load balancer'))
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))

