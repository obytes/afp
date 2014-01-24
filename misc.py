# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from global_conf import *
import boto
import boto.ec2.networkinterface
import boto.ec2.address
import boto.ec2.elb
import time
from fabulous import  ec2_key, ec2_secret,  recipe

try:
    ec2_amis = env.ec2_amis
    ec2_secgroups = env.ec2_secgroups
    ec2_keypair = env.ec2_keypair
    ec2_instancetype = env.ec2_instancetype
except:
    pass

try:
    env_config = env.env_config
    fabconf = env.fabconf
except:
    pass


def _destroy_instance(instance):
    """
    Destroy's instance
    """
    conn = boto.connect_ec2(ec2_key, ec2_secret)
    try:
        conn.terminate_instances(instance_ids=[instance])
        print(_yellow("Image {} destroyed successfully".format(instance)))
    except Exception as e:
        print(_red("Exception was raised: {}".format(str(e))))


def _get_lb():
    """
    get load balancers
    """
    conn = boto.ec2.elb.ELBConnection(ec2_key, ec2_secret)
    lb = conn.get_all_load_balancers()

    return lb


def _register_instance_in_lb(lb_name, *args):
    """
    set one or more instances to a load balancer
    """
    lb_conn = boto.ec2.elb.ELBConnection(ec2_key, ec2_secret)
    return lb_conn.register_instances(lb_name, *args)


def _deregister_instance_from_lb(lb_name, *args):
    """
    delete
    """
    lb_conn = boto.ec2.elb.ELBConnection(ec2_key, ec2_secret)
    return lb_conn.deregister_instances(lb_name, *args)


def _get_all_instances():
    """
    get list of all running instances
    """
    conn = boto.connect_ec2(ec2_key, ec2_secret)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    return instances


def _oven(recipe):
    """
    Cooks the recipe. Fabulous!
    """
    for ingredient in recipe:
        try:
            print(_yellow(ingredient['message']))
        except KeyError:
            pass
        globals()["_" + ingredient['action']](ingredient['params'])


def _create_server():
    """
    Creates EC2 Instance
    """
    print(_yellow("Creating instance"))
    conn = boto.connect_ec2(ec2_key, ec2_secret)
    assert ec2_amis is not None
    image = conn.get_all_images(ec2_amis)

    reservation = image[0].run(1, 1, ec2_keypair, ec2_secgroups,
                               instance_type=ec2_instancetype)

    instance = reservation.instances[0]
    conn.create_tags([instance.id], {"Name": fabconf['INSTANCE_NAME_TAG']})
    conn.create_tags([instance.id], {"Env": env.environment})
    conn.create_tags([instance.id], {"Recipe": fabconf['INSTANCE_RECIPE']})

    while instance.state == u'pending':
        print(_yellow("Instance state: %s" % instance.state))
        time.sleep(10)
        instance.update()

    print(_green("Instance state: %s" % instance.state))
    print(_green("Public dns: %s" % instance.public_dns_name))

    return instance.public_dns_name, instance.id


def _virtualenv(params):
    """
    Allows running commands on the server
    with an active virtualenv
    """
    with cd(fabconf['APPS_DIR']):
        _virtualenv_command(_render(params))


def _apt(params):
    """
    Runs apt-get install commands
    """
    for pkg in params:
        _sudo("apt-get install -qq %s" % pkg)


def _pip(params):
    """
    Runs pip install commands
    """
    for pkg in params:
        _sudo("pip install %s" % pkg)


def _run(params):
    """
    Runs command with active user
    """
    command = _render(params)
    run(command)


def _sudo(params):
    """
    Run command as root
    """
    command = _render(params)
    sudo(command)


def _put(params):
    """
    Moves a file from local computer to server
    """
    put(_render(params['file']), _render(params['destination']))


def _put_template(params):
    """
    Same as _put() but it loads a file and does variable replacement
    """
    f = open(_render(params['template']), 'r')
    template = f.read()

    run(_write_to(_render(template), _render(params['destination'])))


def _render(template, context=None):
    """
    Does variable replacement
    """
    if context is None:
        context = fabconf
    return template % context


def _write_to(string, path):
    """
    Writes a string to a file on the server
    """
    return "echo '" + string + "' > " + path


def _append_to(string, path):
    """
    Appends to a file on the server
    """
    return "echo '" + string + "' >> " + path


def _export_envs(params):
    """
    Export env to profile
    """
    for c in env_config:
        _run("sudo sh -c 'echo \"%(KEY)s=%(VALUE)s\" >> /etc/environment'" %
             {'KEY': c, 'VALUE': env_config[c]})


def _virtualenv_command(command):
    """
    Activates virtualenv and runs command
    """
    with cd(fabconf['APPS_DIR']):
        run(fabconf['ACTIVATE'] + ' && ' + command)


def _run_command(cmd, *args):
    """
    run manage.py command
    """


def _deploy(recipe):
    """
    deploy changes from github
    """
    conn = boto.connect_ec2(ec2_key, ec2_secret)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for instance in instances:
        tags = instance.tags
        if instance.state == 'running' and 'Env' in tags:
            if tags['Env'] == env.environment:
                print(_yellow('Deploying changes to instance: %s' % instance.id))
                env.host_string = instance.public_dns_name
                env.user = fabconf['SERVER_USERNAME']
                env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']
                _oven(recipe)