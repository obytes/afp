# -*- coding: utf-8 -*-
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from global_conf import *
import time


env_config = None
ec2_amis = None
ec2_keypair = None
ec2_secgroups = None
ec2_instancetype = None
fabconf = None
recipe = None


def create_instance(instance_type):
    """
    This does the real work for the ulous() task. Is here to provide backwards compatibility
    """
    start_time = time.time()
    print(_green("Started..."))
    env.environment = None
    while env.environment not in ('Staging', 'Production'):
        environment = prompt('Please specify target environment: ')
        setattr(env, 'environment', environment.strip().capitalize())

    try:
        exec("from recipes.conf_%s_%s import *" % (instance_type, env.environment.lower()), globals())
    except Exception as e:
        print(_red('Exception are using incorrect instance conf name: {}'.format(str(e))))
        exit()
    env.user = fabconf['SERVER_USERNAME']
    env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']

    # import _crate_server and execute
    from misc import _create_server
    env.host_string, instance_id = _create_server()

    print(_green("Waiting 60 seconds for server to boot..."))
    time.sleep(60)
    try:
        exec("from recipes.cook_%s_%s import create_recipe as recipe" %
             (instance_type, env.environment.lower()), globals())
    except Exception as e:
        print(_red('You are using incorrect instance conf name: {}'.format(str(e))))
        exit()

    # import _over and execute
    from misc import _oven
    _oven(recipe)
    if 'LB_NAME' in fabconf:
        register_instance_in_lb(fabconf['LB_NAME'], instance_id)

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
    print(_green(env.host_string))


def get_instance():
    """
    list all instances running on amazon cloud
    """
    start_time = time.time()
    print(_green("Listing active instances..."))
    x = _pretty_table(["Instance ID", "Public DNS", "State", "Tags"])
    # import function
    from misc import _get_all_instances

    for instance in _get_all_instances():
        tags = instance.tags
        x.add_row([instance, instance.public_dns_name, instance.state,
                   ','.join(['%s: %s' % (key, value) for (key, value) in tags.items()])])
    print(_yellow(x))
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))


def destroy_instance(*args):
    """
    distory an instance running on cloud
    """
    start_time = time.time()
    from misc import _destroy_instance

    for instance in args:
        print(_yellow("Destroying active %s..." % instance))
        _destroy_instance(instance)
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))


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


def deploy(instance_type):
    """
    merge and deploy new changes from production
    """
    if 'environment' not in env:
        print(_red('Error must run for an enviroment (e.g fab staging deploy)'))
        exit()
    try:
        exec("from recipes.conf_%s import *" % instance_type, globals())
    except Exception as e:
        print(_red('Exception are using incorrect instance conf name: {}'.format(str(e))))
        exit()

    try:
        exec("from recipes.cook_%s import production_deploy_recipe as recipe" % instance_type, globals())

    except Exception as e:
        print(_red('Exception are using incorrect instance conf name: {}'.format(str(e))))
        exit()

    start_time = time.time()
    print(_green("Deploying changes to all instances of type %s to %s environment" % (instance_type, env.environment)))

    from misc import _deploy, _virtualenv
    _deploy(recipe)
    print(_green('Completed deployment from github'))
    print(_green('Starting DB Migrations...'))

    #_virtualenv('%(PROJECT_NAME)s/./manage.py resetdb') # will refresh the database - new installation(s)
    _virtualenv('%(PROJECT_NAME)s/./manage.py migrate')
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
