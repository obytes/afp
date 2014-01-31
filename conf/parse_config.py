# -*- coding: utf-8 -*-
import os.path
import boto
import boto.ec2.elb
import subprocess
from ConfigParser import SafeConfigParser
from fabric.api import env
from fabric.colors import green as _green, yellow as _yellow, red as _red
from ..global_conf import ec2_key, ec2_secret

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.path.pardir)


def _base(f=''):
    return os.path.join(BASE_DIR, f)


def parse_ini(instance_type, check_all=True):
    parser = SafeConfigParser()
    parser.read(os.path.abspath('fabfile/conf/%s.ini' % instance_type))

    parser.set('CONFIG', 'FABULOUS_PATH',
               os.path.join(os.path.dirname(__file__), os.path.pardir))
    parser.set('CONFIG', 'SSH_SETTING_PATH', _base('settings/ssh'))

    parser.set('PRODUCTION_ENV_CONFIG', 'AWS_ACCESS_KEY_ID', ec2_key)
    parser.set('PRODUCTION_ENV_CONFIG', 'AWS_SECRET_ACCESS_KEY', ec2_secret)

    parser.set('STAGING_ENV_CONFIG', 'AWS_ACCESS_KEY_ID', ec2_key)
    parser.set('STAGING_ENV_CONFIG', 'AWS_SECRET_ACCESS_KEY', ec2_secret)

    fabconf = {}

    _green("Parsing config.ini file")

    for name, value in parser.items('CONFIG'):
        # print '  %s = %s' % (name, value)
        fabconf['%s' % name.upper()] = value

    for name, value in parser.items('%s' % env.environment.upper()):
        # print '  %s = %s' % (name, value)
        fabconf['%s' % name.upper()] = value

    env_config = {}

    for name, value in parser.items('%s_ENV_CONFIG' % env.environment.upper()):
        # print '  %s = %s' % (name, value)
        env_config['%s' % name.upper()] = value

    fabconf['ENV_VARS'] = ','.join('{}="{}"'.format(i, k)
                                   for i, k in env_config.items())

    env.fabconf = fabconf
    env.env_config = env_config

    env.ec2_amis = [fabconf['EC2_AMIS']]
    env.ec2_keypair = fabconf['EC2_KEYPAIR']
    env.ec2_secgroups = [fabconf['EC2_SECGROUPS']]
    env.ec2_instancetype = fabconf['EC2_INSTANCETYPE']

    print(_yellow("SSH private key verification..."))
    try:
        open(fabconf['SSH_PRIVATE_KEY_PATH']).read()
    except Exception, e:
        print(_red("SSH private key does not exist in the provided path %s !" %
              fabconf['SSH_PRIVATE_KEY_PATH']))
        exit()

    print(_yellow("AWS Secret Access and Key verification..."))
    try:
        regions = boto.connect_ec2(ec2_key, ec2_secret).get_all_regions()
        print(_green("EC2 Key and Secret OK"))
    except Exception, e:
        print(_red("Please Check your AWS Secret Access Key !"))
        exit()
    if check_all:
        print(_yellow("MEDIA and STATIC buckets verification..."))
        conn = boto.s3.connection.S3Connection(ec2_key, ec2_secret)
        buckets = [bucket.name for bucket in conn.get_all_buckets()]

        assert env_config['S3_STATIC_BUCKET_STORAGE'] in buckets
        print(_green("S3 STATIC BUCKET STORAGE %s OK") %
              env_config['S3_STATIC_BUCKET_STORAGE'])

        assert env_config['S3_MEDIA_BUCKET_STORAGE'] in buckets
        print(_green("S3 MEDIA BUCKET STORAGE %s OK") %
              env_config['S3_MEDIA_BUCKET_STORAGE'])

        print(_yellow("Load balancers verification..."))
        conn = boto.ec2.elb.ELBConnection(ec2_key, ec2_secret)
        lbs = conn.get_all_load_balancers()
        lb_names = [lb.name for lb in lbs]
        assert fabconf['LB_NAME'] in lb_names
        print(_green("Load balancer name %s OK") % fabconf['LB_NAME'])
        lb_dns_names = [lb.dns_name for lb in lbs]
        assert fabconf['LB_URL'] in lb_dns_names
        print(_green("Load balancer dns name %s OK") % fabconf['LB_URL'])

        print(_yellow("Security group verification..."))

        try:
            groups = boto.connect_ec2(ec2_key, ec2_secret).get_all_security_groups(
                groupnames=env.ec2_secgroups)
            ports = [r.to_port for r in groups[0].rules]
            assert '22' and '80' in ports
            print(
                _green("The security group '%s' exists and has open ports to 22 and 80") %
                fabconf['EC2_SECGROUPS'])
        except Exception, e:
            print(
                _red("The security group '%s' does not exist in default VPC" %
                     fabconf['EC2_SECGROUPS']))
            exit()

    return fabconf, env_config
