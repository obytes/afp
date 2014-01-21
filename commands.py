# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from prettytable import PrettyTable
from global_conf import *
import boto
import boto.ec2.networkinterface
import boto.ec2.address
import time

