
================ Development setup ====================

$ Install required system packages:

    sudo apt-get install python3-pip
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libpq-dev
    sudo apt-get install postgresql postgresql-contrib

$ Create www directory where project sites and environment dir

    mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

$ Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

$ Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
    source /usr/local/bin/virtualenvwrapper.sh

$ Create virtualenv

    cd /var/envs && mkvirtualenv listentome --python=python3

$ Install requirements for a project.

    cd /var/www/listentome && pip install -r requirements/local.txt

