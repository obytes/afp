# -*- coding: utf-8 -*-
import time
import boto
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from conf.parse_config import parse_ini
from global_conf import ec2_key, ec2_secret


@task()
def restart(service_name):
    """
    This restarts services on instance (nginx/gunicorn/celery)
    """
    start_time = time.time()

    print(_green("Started..."))
    require('environment', provided_by=('staging', 'production'))

    try:
        fabconf, env_config = parse_ini('appserver', check_all=False)
    except Exception as e:
        print(_red('Exception parsing config file: {}'.format(str(e))))
        exit()
    env.user = fabconf['SERVER_USERNAME']
    env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']

    from recipes.default_appserver import restart_services as recipe
    command = recipe['%s'%service_name]
    from misc import _oven

    conn = boto.connect_ec2(ec2_key, ec2_secret)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for instance in instances:
        tags = instance.tags
        if instance.state == 'running' and 'Env' in tags:
            if tags['Env'] == env.environment:
                print(_yellow('Restarting service on instance: %s' % instance.id))
                env.host_string = instance.public_dns_name
                env.user = fabconf['SERVER_USERNAME']
                env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']
                _oven(command)

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
    print(_green(env.host_string))

@task()
def log(service_name):
    """
    Show logs of nginx/celery/celerybeat/gunicorn
    """
    start_time = time.time()

    print(_green("Started..."))
    env.environment = None
    while env.environment not in ('Staging', 'Production'):
        environment = prompt('Please specify target environment: ')
        setattr(env, 'environment', environment.strip().capitalize())

    try:
        fabconf, env_config = parse_ini('appserver', check_all=False)
    except Exception as e:
        print(_red('Exception parsing config file: {}'.format(str(e))))
        exit()
    env.user = fabconf['SERVER_USERNAME']
    env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']

    from recipes.default_appserver import log_services as recipe
    command = recipe['%s'%service_name]
    from misc import _oven

    conn = boto.connect_ec2(ec2_key, ec2_secret)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for instance in instances:
        tags = instance.tags
        if instance.state == 'running' and 'Env' in tags:
            if tags['Env'] == env.environment:
                print(_yellow('Restarting service on instance: %s' % instance.id))
                env.host_string = instance.public_dns_name
                env.user = fabconf['SERVER_USERNAME']
                env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']
                _oven(command)

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
    print(_green(env.host_string))
