EC2 command interface
===============================

The EC2 command interface contains very useful fabric commands that list, create or destroy instance on amazon cloud.

List instances : fab ec2 or fab ec2.get_instance
*****************************************************

    >>> fab ec2
    Listing active instances...
    +---------------------+-----------------------------------------+---------+---------------------------------------------------------------+
    |     Instance ID     |                Public DNS               |  State  |                              Tags                             |
    +---------------------+-----------------------------------------+---------+---------------------------------------------------------------+
    | Instance:i-295b4567 | ec2-54-84-2-120.compute-1.amazonaws.com | running |       Recipe: appserver,Name: AppServer,Env: Production       |
    | Instance:i-735f1234 | ec2-54-84-14-37.compute-1.amazonaws.com | running | Recipe: messagingserver,Name: MessagingServer,Env: Production |
    +---------------------+-----------------------------------------+---------+---------------------------------------------------------------+
    Runtime: 0.036777 minutes


Create appserver instance : fab ec2.create:appserver
*********************************************************

This fab command creates a full instance, it installs and configures nginx, supervisor, celery and gunicorn, all the requirements
are also installed and the instance is ready for use in few minutes.
The install progression is printed in the console during the process.

    >>> fab ec2.create:appserver:staging
    Started...
    Please specify target environment: staging
    SSH private key verification...
    AWS Secret Access and Key verification...
    EC2 Key and Secret OK
    MEDIA and STATIC buckets verification...
    S3 STATIC BUCKET STORAGE assets.diwaniyalabs.com OK
    S3 MEDIA BUCKET STORAGE media.diwaniyalabs.com OK
    Load balancers verification...
    Load balancer name api-load-balancer-staging OK
    Load balancer dns name api-load-balancer-staging-1793786200.us-east-1.elb.amazonaws.com OK
    Security group verification...
    The security group 'default' exists and has open ports to 22 and 80
    Creating instance

Note that you can use the same command to create a messaging server for celery.
    >>> fab ec2.create:messagingserver


Destroy instance : fab ec2.destroy:instance_id
******************************************************

This command deletes the instance from amazon cloud, example :
    >>> fab ec2.destroy:i-123f4567

Deploy changes : fab production ec2.deploy:appserver
**********************************************************

This command allows to deploy the changes to your staging/production WebApps.
When deploying to staging, it merges development branch with staging, and when deploying to production it merges changes from
staging with branch master.
When deploying to production, the program asks for a release version.
Deployment steps :

    #) Pull changes.
    #) Merge
    #) install requirements
    #) restart celery
    #) restart supervisor
    #) Migrate database
    #) Collect static