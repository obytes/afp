# -*- coding: utf-8 -*-
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from conf.parse_config import parse_ini
import time


recipe = None

@task()
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
        fabconf, env_config = parse_ini(instance_type)
    except Exception as e:
        print(_red('Exception parsing config file: {}'.format(str(e))))
        exit()
    env.user = fabconf['SERVER_USERNAME']
    env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']

    # import _crate_server and execute
    from misc import _create_server
    env.host_string, instance_id = _create_server()

    print(_green("Waiting 60 seconds for server to boot..."))
    time.sleep(60)
    try:
        exec("from recipes.default_%s import create_recipe_%s as recipe" %
             (instance_type, env.environment.lower()), globals())
    except Exception as e:
        print(_red('You are using incorrect instance conf name: {}'.format(str(e))))
        exit()

    # import _over and execute
    from misc import _oven
    _oven(recipe)
    if 'LB_NAME' in fabconf:
        from lb import register_instance_in_lb
        register_instance_in_lb(fabconf['LB_NAME'], instance_id)

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
    print(_green(env.host_string))

@task()
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

@task()
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

