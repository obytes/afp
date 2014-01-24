# -*- coding: utf-8 -*-
import os.path
from ConfigParser import SafeConfigParser
from fabric.api import env
from fabric.api import prompt
from fabric.colors import green as _green

ec2_key = ""
ec2_secret = ""

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.pardir)


def _base(f=''):
    return os.path.join(BASE_DIR, f)

global ec2_amis
global ec2_keypair
global ec2_secgroups
global ec2_instancetype

def parse_ini():
    parser = SafeConfigParser()
    parser.read(os.path.abspath('fabfile/conf/config.ini'))

    parser.set('CONFIG', 'FABULOUS_PATH', os.path.join(os.path.dirname(__file__), os.path.pardir))
    parser.set('CONFIG', 'SSH_SETTING_PATH', _base('settings/ssh'))

    parser.set('PRODUCTION_ENV_CONFIG', 'AWS_ACCESS_KEY_ID', ec2_key)
    parser.set('PRODUCTION_ENV_CONFIG', 'AWS_SECRET_ACCESS_KEY', ec2_secret)

    parser.set('STAGING_ENV_CONFIG', 'AWS_ACCESS_KEY_ID', ec2_key)
    parser.set('STAGING_ENV_CONFIG', 'AWS_SECRET_ACCESS_KEY', ec2_secret)


    fabconf={}

    _green("Parsing config.ini file")

    for name, value in parser.items('CONFIG'):
        print '  %s = %s' % (name, value)
        fabconf['%s'%name.upper()] = value

    for name, value in parser.items('%s'%env.environment.upper()):
        print '  %s = %s' % (name, value)
        fabconf['%s'%name.upper()] = value

    env_config = {}

    for name, value in parser.items('%s_ENV_CONFIG'%env.environment.upper()):
        print '  %s = %s' % (name, value)
        env_config['%s'%name.upper()] = value


    fabconf['ENV_VARS'] = ','.join('{}="{}"'.format(i, k) for i, k in env_config.items())

    env.fabconf = fabconf
    env.env_config = env_config

    env.ec2_amis = [fabconf['EC2_AMIS']]
    env.ec2_keypair = fabconf['EC2_KEYPAIR']
    env.ec2_secgroups = [fabconf['EC2_SECGROUPS']]
    env.ec2_instancetype = fabconf['EC2_INSTANCETYPE']

    return fabconf, env_config
