# -*- coding: utf-8 -*-
import os.path
from fabric.api import env
from ..global_conf import ec2_key, ec2_secret

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.pardir)


def _base(f=''):
    return os.path.join(BASE_DIR, f)

fabconf = {}

#  Do not edit
fabconf['FABULOUS_PATH'] = os.path.join(os.path.dirname(__file__), os.path.pardir)

# Username for connecting to EC2 instaces
fabconf['SERVER_USERNAME'] = "ubuntu"


# Full local path for .ssh
fabconf['SSH_PATH'] = "~/.ssh"


# Name of the private key file you use to connect to EC2 instance
fabconf['EC2_KEY_NAME'] = "aws.pem"


# Don't edit. Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (_base('settings/ssh'), fabconf['EC2_KEY_NAME'])


# Project name: polls
fabconf['PROJECT_NAME'] = "dlap"

# Where to install apps
fabconf['APPS_DIR'] = "/home/%s/webapps" % fabconf['SERVER_USERNAME']

# Where you want your project installed: /APPS_DIR/PROJECT_NAME
fabconf['PROJECT_PATH'] = "%s/%s" % (fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

# App domains
fabconf['DOMAINS'] = "www.diwaniyalabs.com diwaniyalabs.com"


# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/home/%s/.virtualenvs" % fabconf['SERVER_USERNAME']

# Email for the server admin
fabconf['ADMIN_EMAIL'] = "webmaster@diwaniyalabs.com"

# Git username for the server
fabconf['GIT_USERNAME'] = "server-a"


# Name of the private key file used for github deployments
fabconf['GITHUB_DEPLOY_KEY_NAME'] = "github"


# Don't edit. Local path for deployment key you use for github
fabconf['GITHUB_DEPLOY_KEY_PATH'] = "%s/%s" % (_base('settings/ssh'), fabconf['GITHUB_DEPLOY_KEY_NAME'])


# Path to the repo of the application you want to install
fabconf['GITHUB_REPO'] = "git@github.com:mo-mughrabi/dlap.git"

fabconf['GITHUB_BRANCH'] = "master"

fabconf['GITBUH_STAGING_BRANCH'] = "staging"

fabconf['GITBUH_DEV_BRANCH'] = "development"


# Virtualenv activate command
fabconf['ACTIVATE'] = "source /home/%s/.virtualenvs/%s/bin/activate" % (
    fabconf['SERVER_USERNAME'], fabconf['PROJECT_NAME'])

# Name tag for your server instance on EC2
fabconf['INSTANCE_NAME_TAG'] = "AppServer"
fabconf['INSTANCE_RECIPE'] = "appserver"

# load balancer url
fabconf['LB_URL'] = 'api-load-balancer-1351515642.us-east-1.elb.amazonaws.com'

# load balancer name
fabconf['LB_NAME'] = 'api-load-balancer'

# AMI name. http://bit.ly/liLKxj
ec2_amis = ['ami-1335f37a']

# Name of the keypair you use in EC2. http://bit.ly/ldw0HZ
ec2_keypair = 'default'


# Name of the security group. http://bit.ly/kl0Jyn
ec2_secgroups = ['default']


# API Name of instance type. http://bit.ly/mkWvpn
ec2_instancetype = 't1.micro'

env_config = {'AWS_ACCESS_KEY_ID': ec2_key, 'AWS_SECRET_ACCESS_KEY': ec2_secret,
              'S3_STATIC_BUCKET_STORAGE': 'assets.diwaniyalabs.com',
              'S3_MEDIA_BUCKET_STORAGE': 'media.diwaniyalabs.com',
              'DATABASE_URL': 'postgres://root:frogman123@dlap-production.cypujmmjpinm.us-east-1.rds.amazonaws.com:'
                              '5432/dlap',
              'STATIC_URL': 'http://assets.diwaniyalabs.com.s3-website-us-east-1.amazonaws.com/',
              'MEDIA_URL': 'http://media.diwaniyalabs.com.s3-website-us-east-1.amazonaws.com/',
              'SETTING_FILE': 'production'}

fabconf['ENV_VARS'] = ','.join('{}="{}"'.format(i, k) for i, k in env_config.items())