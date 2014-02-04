# -*- coding: utf-8 -*-
# cookbook
# This file describes the packages to install and how to set them up.
#
# Ingredients: nginx, memecached, gunicorn, supervisord, virtualenv, git


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
     "params": ["nginx", "memcached", "git", "python-pip", "python-virtualenv", "postgresql-client",
                "python-setuptools", "python-dev", "build-essential", "libpq-dev"],
     "message": "Installing apt-get packages"},

    # List of pypi packages to install
    {"action": "pip", "params": ["virtualenvwrapper", "supervisor"],
     "message": "Installing pip packages"},

    # nginx
    {"action": "put", "params": {"file": "%(FABULOUS_PATH)s/recipes/templates/nginx.conf",
                                 "destination": "/home/%(SERVER_USERNAME)s/nginx.conf"},
     "message": "Configuring nginx"},
    {"action": "sudo", "params":
     "mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old"},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/nginx.conf /etc/nginx/nginx.conf"},
    {"action": "sudo", "params": "chown root:root /etc/nginx/nginx.conf"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/nginx-app-proxy",
                                          "destination": "/home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s"}},
    {"action": "sudo", "params":
     "rm -rf /etc/nginx/sites-enabled/default"},
    {"action": "sudo",
     "params": "mv /home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s"},
    {"action": "sudo",
     "params": "ln -s /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s"},
    {"action": "sudo", "params":
     "chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s"},
    {"action": "sudo", "params": "/etc/init.d/nginx restart",
     "message": "Restarting nginx"},

    # virtualenvwrapper
    {"action": "sudo", "params":
     "mkdir %(VIRTUALENV_DIR)s", "message": "Configuring virtualenvwrapper"},
    {"action": "sudo", "params":
     "chown -R %(SERVER_USERNAME)s: %(VIRTUALENV_DIR)s"},
    {"action": "run", "params":
     "echo 'export WORKON_HOME=%(VIRTUALENV_DIR)s' >> /home/%(SERVER_USERNAME)s/.profile"},
    {"action": "run",
     "params": "echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/%(SERVER_USERNAME)s/.profile"},
    {"action": "run", "params":
     "source /home/%(SERVER_USERNAME)s/.profile"},

    # webapps alias
    {"action": "run", "params": """echo "alias webapps='cd %(APPS_DIR)s'" >> /home/%(SERVER_USERNAME)s/.profile""",
     "message": "Creating webapps alias"},

    # webapps dir
    {"action": "sudo", "params":
     "mkdir %(APPS_DIR)s", "message": "Creating webapps directory"},
    {"action": "sudo", "params":
     "chown -R %(SERVER_USERNAME)s: %(APPS_DIR)s"},

    # git setup
    {"action": "run", "params": "git config --global user.name '%(GIT_USERNAME)s'",
     "message": "Configuring git"},
    {"action": "run", "params":
     "git config --global user.email '%(ADMIN_EMAIL)s'"},
    {"action": "put", "params": {"file": "%(GITHUB_DEPLOY_KEY_PATH)s",
                                 "destination": "/home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"}},
    {"action": "run", "params":
     "chmod 600 /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"},
    {"action": "run",
     "params": """echo 'IdentityFile /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s' >> /home/%(SERVER_USERNAME)s/.ssh/config"""},
    {"action": "run", "params":
     "ssh-keyscan github.com >> /home/%(SERVER_USERNAME)s/.ssh/known_hosts"},

    # Create virtualevn
    {"action": "run", "params": "mkvirtualenv --no-site-packages %(PROJECT_NAME)s",
     "message": "Creating virtualenv"},

    # install imaging tools
    {"action": "sudo", "params":
     "apt-get install -qq libjpeg62 libjpeg62-dev zlib1g-dev"},
    {"action": "sudo", "params":
     "sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib"},

    # install django in virtual env
    {"action": "virtualenv", "params": "git clone -b %(GITHUB_BRANCH)s %(GITHUB_REPO)s",
     "message": "Cloning project"},

    {"action": "virtualenv", "params": "pip install -r %(PROJECT_NAME)s/requirements.txt",
     "message": "Install project requirements"},

    # install gunicorn in virtual env's
    {"action": "virtualenv", "params": "pip install gunicorn",
     "message": "Installing gunicorn"},

    # Setup supervisor
    {"action": "run", "params": "echo_supervisord_conf > /home/%(SERVER_USERNAME)s/supervisord.conf",
     "message": "Configuring supervisor"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/supervisord.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/my.supervisord.conf"}},
    {"action": "run",
     "params": "cat /home/%(SERVER_USERNAME)s/my.supervisord.conf >> /home/%(SERVER_USERNAME)s/supervisord.conf"},
    {"action": "run", "params":
     "rm /home/%(SERVER_USERNAME)s/my.supervisord.conf"},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/supervisord.conf /etc/supervisord.conf"},
    #{"action":"sudo", "params":"supervisord"},
    {"action": "put", "params": {"file": "%(FABULOUS_PATH)s/recipes/templates/supervisord-init",
                                 "destination": "/home/%(SERVER_USERNAME)s/supervisord-init"}},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/supervisord-init /etc/init.d/supervisord"},
    {"action": "sudo", "params": "chmod +x /etc/init.d/supervisord"},
    {"action": "sudo", "params": "update-rc.d supervisord defaults"},
    {"action": "sudo", "params": "sudo /etc/init.d/supervisord start"},
    {"action": "sudo", "params":
     "sudo supervisorctl restart %(PROJECT_NAME)s"},
    # Install and setup celery
    {"action": "virtualenv", "params": "pip install celery django-celery",
     "message": "Install celery requirements"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/celeryd.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/celeryd.conf"}},
    {"action": "sudo", "params":
     "cat /home/%(SERVER_USERNAME)s/celeryd.conf >> /etc/supervisord.conf"},

    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/celerybeat.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/celerybeat.conf"}},
    {"action": "sudo", "params":
     "cat /home/%(SERVER_USERNAME)s/celerybeat.conf >> /etc/supervisord.conf"},
    {"action": "sudo", "params": "sudo supervisorctl update"},
    {"action": "sudo", "params": "sudo supervisorctl restart celery"},
    {"action": "sudo", "params": "sudo supervisorctl restart celerybeat"},

    {"action": "sudo", "params": "sudo reboot",
     "message": "Rebooting server"},


]

deploy_recipe_production = [
    # First command as regular user
    {"action": "run", "params": "whoami"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git checkout %(GITBUH_STAGING_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git pull"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git checkout %(GITHUB_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git merge %(GITBUH_STAGING_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git push"},

    {"action": "virtualenv", "params": "pip install -r %(PROJECT_NAME)s/requirements.txt",
     "message": "Install project requirements"},

    {"action": "sudo", "params": "sudo supervisorctl restart celery",
     "message": "Restarting celery"},

    {"action": "sudo", "params": "sudo supervisorctl restart celerybeat",
     "message": "Restarting celerybeat"},

    {"action": "sudo", "params": "sudo supervisorctl restart %(PROJECT_NAME)s",
     "message": "Restart supvervisord instance"},

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
     "params": ["nginx", "memcached", "git", "python-pip", "python-virtualenv", "postgresql-client",
                "python-setuptools", "python-dev", "build-essential", "libpq-dev"],
     "message": "Installing apt-get packages"},

    # List of pypi packages to install
    {"action": "pip", "params": ["virtualenvwrapper", "supervisor"],
     "message": "Installing pip packages"},

    # nginx
    {"action": "put", "params": {"file": "%(FABULOUS_PATH)s/recipes/templates/nginx.conf",
                                 "destination": "/home/%(SERVER_USERNAME)s/nginx.conf"},
     "message": "Configuring nginx"},
    {"action": "sudo", "params":
     "mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old"},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/nginx.conf /etc/nginx/nginx.conf"},
    {"action": "sudo", "params": "chown root:root /etc/nginx/nginx.conf"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/nginx-app-proxy",
                                          "destination": "/home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s"}},
    {"action": "sudo", "params":
     "rm -rf /etc/nginx/sites-enabled/default"},
    {"action": "sudo",
     "params": "mv /home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s"},
    {"action": "sudo",
     "params": "ln -s /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s"},
    {"action": "sudo", "params":
     "chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s"},
    {"action": "sudo", "params": "/etc/init.d/nginx restart",
     "message": "Restarting nginx"},

    # virtualenvwrapper
    {"action": "sudo", "params":
     "mkdir %(VIRTUALENV_DIR)s", "message": "Configuring virtualenvwrapper"},
    {"action": "sudo", "params":
     "chown -R %(SERVER_USERNAME)s: %(VIRTUALENV_DIR)s"},
    {"action": "run", "params":
     "echo 'export WORKON_HOME=%(VIRTUALENV_DIR)s' >> /home/%(SERVER_USERNAME)s/.profile"},
    {"action": "run",
     "params": "echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/%(SERVER_USERNAME)s/.profile"},
    {"action": "run", "params":
     "source /home/%(SERVER_USERNAME)s/.profile"},

    # webapps alias
    {"action": "run", "params": """echo "alias webapps='cd %(APPS_DIR)s'" >> /home/%(SERVER_USERNAME)s/.profile""",
     "message": "Creating webapps alias"},

    # webapps dir
    {"action": "sudo", "params":
     "mkdir %(APPS_DIR)s", "message": "Creating webapps directory"},
    {"action": "sudo", "params":
     "chown -R %(SERVER_USERNAME)s: %(APPS_DIR)s"},

    # git setup
    {"action": "run", "params": "git config --global user.name '%(GIT_USERNAME)s'",
     "message": "Configuring git"},
    {"action": "run", "params":
     "git config --global user.email '%(ADMIN_EMAIL)s'"},
    {"action": "put", "params": {"file": "%(GITHUB_DEPLOY_KEY_PATH)s",
                                 "destination": "/home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"}},
    {"action": "run", "params":
     "chmod 600 /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"},
    {"action": "run",
     "params": """echo 'IdentityFile /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s' >> /home/%(SERVER_USERNAME)s/.ssh/config"""},
    {"action": "run", "params":
     "ssh-keyscan github.com >> /home/%(SERVER_USERNAME)s/.ssh/known_hosts"},

    # Create virtualevn
    {"action": "run", "params": "mkvirtualenv --no-site-packages %(PROJECT_NAME)s",
     "message": "Creating virtualenv"},

    # install imaging tools
    {"action": "sudo", "params":
     "apt-get install -qq libjpeg62 libjpeg62-dev zlib1g-dev"},
    {"action": "sudo", "params":
     "sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib"},

    # install django in virtual env
    {"action": "virtualenv", "params": "git clone -b %(GITBUH_STAGING_BRANCH)s %(GITHUB_REPO)s",
     "message": "Cloning project"},

    {"action": "virtualenv", "params": "pip install -r %(PROJECT_NAME)s/requirements.txt",
     "message": "Install project requirements"},

    # install gunicorn in virtual env's
    {"action": "virtualenv", "params": "pip install gunicorn",
     "message": "Installing gunicorn"},

    # Setup supervisor
    {"action": "run", "params": "echo_supervisord_conf > /home/%(SERVER_USERNAME)s/supervisord.conf",
     "message": "Configuring supervisor"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/supervisord.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/my.supervisord.conf"}},
    {"action": "run",
     "params": "cat /home/%(SERVER_USERNAME)s/my.supervisord.conf >> /home/%(SERVER_USERNAME)s/supervisord.conf"},
    {"action": "run", "params":
     "rm /home/%(SERVER_USERNAME)s/my.supervisord.conf"},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/supervisord.conf /etc/supervisord.conf"},
    #{"action":"sudo", "params":"supervisord"},
    {"action": "put", "params": {"file": "%(FABULOUS_PATH)s/recipes/templates/supervisord-init",
                                 "destination": "/home/%(SERVER_USERNAME)s/supervisord-init"}},
    {"action": "sudo", "params":
     "mv /home/%(SERVER_USERNAME)s/supervisord-init /etc/init.d/supervisord"},
    {"action": "sudo", "params": "chmod +x /etc/init.d/supervisord"},
    {"action": "sudo", "params": "update-rc.d supervisord defaults"},
    {"action": "sudo", "params": "sudo /etc/init.d/supervisord start"},
    {"action": "sudo", "params":
     "sudo supervisorctl restart %(PROJECT_NAME)s"},
    # Install and setup celery
    {"action": "virtualenv", "params": "pip install celery django-celery",
     "message": "Install celery requirements"},
    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/celeryd.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/celeryd.conf"}},
    {"action": "sudo", "params":
     "cat /home/%(SERVER_USERNAME)s/celeryd.conf >> /etc/supervisord.conf"},

    {"action": "put_template", "params": {"template": "%(FABULOUS_PATH)s/recipes/templates/celerybeat.conf",
                                          "destination": "/home/%(SERVER_USERNAME)s/celerybeat.conf"}},
    {"action": "sudo", "params":
     "cat /home/%(SERVER_USERNAME)s/celerybeat.conf >> /etc/supervisord.conf"},
    {"action": "sudo", "params": "sudo supervisorctl update"},
    {"action": "sudo", "params": "sudo supervisorctl restart celery"},
    {"action": "sudo", "params": "sudo supervisorctl restart celerybeat"},

    {"action": "sudo", "params": "sudo reboot",
     "message": "Rebooting server"},
]

deploy_recipe_staging = [
    # First command as regular user
    {"action": "run", "params": "whoami"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git checkout %(GITBUH_STAGING_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git pull"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git checkout %(GITHUB_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git merge %(GITBUH_STAGING_BRANCH)s"},

    {"action": "run", "params":
     "cd %(APPS_DIR)s/%(PROJECT_NAME)s; git push"},

    {"action": "virtualenv", "params": "pip install -r %(PROJECT_NAME)s/requirements.txt",
     "message": "Install project requirements"},

    {"action": "sudo", "params": "sudo supervisorctl restart celery",
     "message": "Restarting celery"},

    {"action": "sudo", "params": "sudo supervisorctl restart celerybeat",
     "message": "Restarting celerybeat"},

    {"action": "sudo", "params": "sudo supervisorctl restart %(PROJECT_NAME)s",
     "message": "Restart supvervisord instance"},

]

restart_services = \
    {"nginx": [{"action": "sudo", "params": "sudo service nginx restart",
               "message": "Restarting nginx"}],
     "gunicorn": [{"action": "sudo", "params": "sudo supervisorctl restart %(PROJECT_NAME)s",
                   "message": "Restarting gunicorn"}],
     "celery": [{"action": "sudo", "params": "sudo supervisorctl restart celery",
                 "message": "Restarting celery"},
                {"action": "sudo", "params": "sudo supervisorctl restart celerybeat",
                 "message": "Restarting celerybeat"}]
     }

log_services = \
    {"nginx": [{"action": "sudo", "params": "sudo tail /tmp/nginx.access.log",
                "message": "Nginx logs"}],
     "gunicorn": [{"action": "sudo", "params": "sudo tail /tmp/%(PROJECT_NAME)s.log",
                   "message": "Gunicorn logs"}],
     "celery": [{"action": "sudo", "params": "sudo tail /var/log/celeryd.log",
                 "message": "Celery logs"}],
     "celerybeat": [{"action": "sudo", "params": "sudo tail /var/log/celerybeat.log",
                     "message": "Celerybeat logs"}]
     }
