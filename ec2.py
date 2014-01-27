# -*- coding: utf-8 -*-
import time
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from conf.parse_config import parse_ini


recipe = None


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

    print(_green('Starting Collect Static...'))
    _virtualenv('%(PROJECT_NAME)s/./manage.py collectstatic --noinput')
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
