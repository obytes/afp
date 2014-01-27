# -*- coding: utf-8 -*-
import time
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from conf.parse_config import parse_ini


recipe = None


@task()
def get_lb():
    """
    get/list load balancer's
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

@task()
def deploy(instance_type):
    """
    merge and deploy new changes from production
    """
    if 'environment' not in env:
        print(_red('Error must run for an enviroment (e.g fab staging deploy)'))
        exit()
    try:
        fabconf, env_config = parse_ini(instance_type)
    except Exception as e:
        print(_red('Exception parsing config file: {}'.format(str(e))))
        exit()

    try:
        exec("from recipes.default_%s import deploy_recipe_%s as recipe" %
             (instance_type, env.environment.lower()), globals())

    except Exception as e:
        print(_red('Exception are using incorrect instance conf name: {}'.format(str(e))))
        exit()

    start_time = time.time()
    print(_green("Deploying changes to all instances of type webapp to %s environment" % ( env.environment)))

    from misc import _deploy, _virtualenv
    _deploy(recipe)
    print(_green('Completed deployment from github'))
    print(_green('Starting DB Migrations...'))

    #_virtualenv('%(PROJECT_NAME)s/./manage.py resetdb') # will refresh the database - new installation(s)
    _virtualenv('%(PROJECT_NAME)s/./manage.py migrate')
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
