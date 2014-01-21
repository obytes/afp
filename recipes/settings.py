# -*- coding: utf-8 -*-
from fabric.api import env


def staging():
    """ Set staging environment """
    env.environment = 'Staging'


def production():
    """ Set production environment """
    env.environment = 'Production'