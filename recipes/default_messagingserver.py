# -*- coding: utf-8 -*-
# cookbook
# This file describes the packages to install and how to set them up.
#
# Ingredients: rabbitmq-server


create_recipe_production = [
    # First command as regular user
    {"action": "run", "params": "whoami"},

    # setup env variables
    {"action": "export_envs", "params": "",
     "message": "Exporting variables"},

    # sudo apt-get update
    {"action": "sudo", "params": "apt-get update -qq",
     "message": "Updating apt-get"},

    # List of APT packages to install
    {"action": "apt",
     "params": ["rabbitmq-server"],
     "message": "Installing apt-get packages"},

    {"action": "sudo", "params": "sudo reboot",
     "message": "Rebooting server"},
]

create_recipe_staging = [
    # First command as regular user
        {"action": "run", "params": "whoami"},

    # setup env variables
        {"action": "export_envs", "params": "",
         "message": "Exporting variables"},

    # sudo apt-get update
        {"action": "sudo", "params": "apt-get update -qq",
         "message": "Updating apt-get"},

    # List of APT packages to install
        {"action": "apt",
         "params": ["rabbitmq-server"],
         "message": "Installing apt-get packages"},

        {"action": "sudo", "params": "sudo reboot",
         "message": "Rebooting server"},
    ]
