# -*- coding: utf-8 -*-
from fabric.api import env, task
__all__ = ['settings']

@task()
def staging():
    """ Set staging environment """
    env.environment = 'Staging'


@task()
def production():
    """ Set production environment """
    env.environment = 'Production'