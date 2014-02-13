# -*- coding: utf-8 -*-
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _base(f=''):
    return os.path.join(BASE_DIR, f)


# EC2 key.
ec2_key = ''

# EC2 secret.
ec2_secret = ''
