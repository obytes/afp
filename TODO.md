1. Enhance the project structure
===
recipes should be a configuration folder, we should also replace python configuration with ini, conf or any
alternative configuration file.


2. Project must have main.py which should contain main class initiator
===
the class initiator should take ec2 key and ec2 secret as minimum parameter to initiate. the class should be able to
execute other classes. For instance, the afp main class will be used to call Instance class

Instance class:

    we should be able to list, get instance, set load balancer, create instance, destroy instance, list recipes,
    deploy, etc

Load balancer class:

    should be able to create, list, delete, view instances inside a given load balancer, refresh laod balancer

RDS class:

    show rds health, show rds statistics, list rds


S3 class:

    show all buckets, get buckets details, create bucket, delete bucket


Main (afp) class:

    should validate recipes before execution, execute methods from instance class and other classes




