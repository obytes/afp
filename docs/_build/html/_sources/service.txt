Service command interface
===============================

The service command interface contains 2 fabric commands to restart and show logs of Nginx, Gunicorn or Celery

Restart a service : fab service.restart:service_name
********************************************************

service_name param can take following values:
    #) nginx
    #) gunicorn
    #) celery

Show logs : fab service.log:service_name
************************************************
service_name takes the same values as restart command.
Example:
    >>> fab service.log:nginx
    Started...
    Please specify target environment: production
    SSH private key verification...
    AWS Secret Access and Key verification...
    EC2 Key and Secret OK
    Restarting service on instance: i-295b735
    Nginx logs
    [ec2-54-84-2-20.compute-1.amazonaws.com] sudo: sudo tail /tmp/nginx.access.log
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:08:34 +0000] "GET /aws/ping.html HTTP/1.1" 200 0 "-" "ELB-HealthChecker/1.0"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:09:03 +0000] "-" 400 0 "-" "-"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:09:04 +0000] "GET /aws/ping.html HTTP/1.1" 200 0 "-" "ELB-HealthChecker/1.0"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:09:33 +0000] "-" 400 0 "-" "-"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:09:34 +0000] "GET /aws/ping.html HTTP/1.1" 200 0 "-" "ELB-HealthChecker/1.0"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:09:44 +0000] "HEAD / HTTP/1.1" 200 0 "-" "-"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:10:04 +0000] "-" 400 0 "-" "-"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:10:04 +0000] "GET /aws/ping.html HTTP/1.1" 200 0 "-" "ELB-HealthChecker/1.0"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:10:33 +0000] "-" 400 0 "-" "-"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out: 172.31.36.35 - - [07/Feb/2014:22:10:34 +0000] "GET /aws/ping.html HTTP/1.1" 200 0 "-" "ELB-HealthChecker/1.0"
    [ec2-54-84-2-20.compute-1.amazonaws.com] out:
    Runtime: 0.209646 minutes
    ec2-54-84-2-20.compute-1.amazonaws.com
    Done.
    Disconnecting from ec2-54-84-2-20.compute-1.amazonaws.com... done.

