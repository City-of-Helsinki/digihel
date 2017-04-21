# How to use these files to deploy digiedu locally

You will need a Linux-style server and root-account

1. Open a SSH-connection to the server
   ssh root@server
2. Install the necessary packages for installing Ansible:
   (Ansible is not yet Python 3 safe)
   These commands are for Ubuntu 16.04:
   apt-get install python-openssl
   apt-get install python-pip
   apt-get install libssl-dev
3. Install ansible itself:
   pip install ansible
4. Run ansible in this directory:
   ansible-playbook -i local.inventory playbook.yml
5. The service should now listen on http port using name
   digiedu.dev.hel.ninja 

The installation roles are configured in config/digiedu-cms-dev.yml
Change django_external_name to change the user visible name of the server.

# Testing using Vagrant

If you have Vagrant installed you can test the deployment:

vagrant up