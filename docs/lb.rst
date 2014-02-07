LB command interface
===============================

LB command interface contains fab commands to manage Load Balancers.

List load balancers : fab lb or fab lb.list
*****************************************************
This command lists your load balancers in a list with 3 columns: "Load balancer ID", "Public DNS", "Instances"
    >>> fab lb

Register instance in lb : fab lb.register_instance_in_lb: lb_name:instance_id
*******************************************************************************

This command assigns an instance to a given load balancer, example:
    >>> fab fab lb.register_instance_in_lb:api-load-balancer-154545642.us-east-1.elb.amazonaws.com:i-456f3445

Delete instance from lb : fab lb.deregister_instance_in_lb: lb_name:instance_id
********************************************************************************

This command deletes an instance from a given load balancer, example:
    >>> fab fab lb.deregister_instance_in_lb:api-load-balancer-154545642.us-east-1.elb.amazonaws.com:i-456f3445
    De-assigning instance from load balancer api-load-balancer-154545642.us-east-1.elb.amazonaws.com...
    Instance(s) de-registered from load balancer
    Runtime: 0.115201 minutes