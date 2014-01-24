# -*- coding: utf-8 -*-
import boto
from boto.s3.connection import S3Connection
from prettytable import PrettyTable as _pretty_table
from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow, red as _red
from global_conf import *
from conf.parse_config import parse_ini
import time

def list_buckets():
    '''List All Buckets'''

    start_time = time.time()
    conn = S3Connection(ec2_key, ec2_secret)
    print(_green("Listing active buckets..."))
    buckets = conn.get_all_buckets()
    x = _pretty_table(["Name", "Connection"])
    for bucket in buckets:
        x.add_row([bucket.name, bucket.connection])

    print(_yellow(x))

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))

def get_bucket(bucket_name):
    '''Get bucket details'''

    start_time = time.time()
    conn = S3Connection(ec2_key, ec2_secret)

    try:
        bucket = conn.get_bucket(bucket_name = bucket_name)
    except Exception, e:
        print(_red('Bucket error: {}'.format(str(e))))

    print bucket
    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))

def create_bucket(bucket_name):
    '''Create a bucket'''

    start_time = time.time()
    conn = S3Connection(ec2_key, ec2_secret)
    print(_green("Creating bucket..."))

    try:
        bucket = conn.create_bucket(bucket_name = bucket_name)
        print _green('Bucket "%s" successfully created'%bucket_name)
    except Exception, e:
        print(_red('Create bucket error: {}'.format(str(e))))

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))



def delete_bucket(bucket_name):
    '''Delete a bucket'''

    start_time = time.time()
    conn = S3Connection(ec2_key, ec2_secret)

    delete = prompt('Are you sure you want to delete this bucket (Y/N): ')
    if delete.upper() == 'Y':
        try:
            bucket = conn.get_bucket(bucket_name = bucket_name)
            print(_green("Deleting bucket..."))
            conn.delete_bucket(bucket)
            print _yellow('Bucket "%s" successfully deleted'%bucket_name)
        except Exception, e:
            print(_red('Delete bucket error: {}'.format(str(e))))

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))




