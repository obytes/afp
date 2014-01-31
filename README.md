Amazon Fabric Package
Introduction
-----
AFP is a fabric package to install, deploy and manage django applications on amazon cloud

Instalation
-----
Clone the repository, Rename afp folder to fabfile the repository and Install project requirements :

    1-git clone git@github.com:mo-mughrabi/afp.git
    2-mv afp fabfile
    3-pip install -r requirements

Configuration
-----
    1-Put your AWS Secret Access and Key in global_conf.py
    2-Edit conf/appserver.ini with your credentials
    3-Put your amazon ssh private key, github private and public keys inside settings/ssh folder
Note that your remote git repository must contain 3 branches, development, staging and production

Available commands
-----
    production                      Set production environment
    staging                         Set staging environment
    ec2                             list all instances running on amazon cloud
    ec2.create                      This creates a new instance in amazon cloud
    ec2.deploy                      merge and deploy new changes from production
    ec2.destroy                     distory an instance running on cloud
    ec2.get_instance                list all instances running on amazon cloud
    lb                              list load balancers
    lb.deregister_instance_from_lb  delete instance from load balancer
    lb.list                         list load balancers
    lb.register_instance_in_lb      set load balancer, assigns an instance to a given load balancer
    rds                             List All Relational Data Service
    s3                              List All Buckets
    s3.create_bucket                Create a bucket
    s3.delete_bucket                Delete a bucket
    s3.get_bucket                   Get bucket details
    s3.list_buckets                 List All Buckets
    service.log                     Show logs of nginx/celery/celerybeat/gunicorn
    service.restart                 This restarts services on instance (nginx/gunicorn/celery)
Contributors
-----
    * Mo Mughrabi - Lead developer
    * Ahmed Elhamidi - Django Developer
