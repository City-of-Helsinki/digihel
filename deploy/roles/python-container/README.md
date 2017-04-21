# Python container role

This role sets up a container for a Python application talking WSGI.

Initial version uses uWSGI.

Parameters:

pycont_user:
	System user the application should run as. Currently applications
        run under the default web group (www-data in Ubuntu)
pycont_name:
        Name of the application. In practice this is the directory where the
	containers expects to find the application root.
pycont_app_name:
        Directory under "pycont_name", where the wsgi.py is installed
pycont_url_prefix:
        URL-prefix that is stripped from the PATH_INFO passed to
	application. This allows the application to be installed in
	not-root.
pycont_contract_port:
        Port that uwsgi will listen on. "Contract" is from (kind of) 12-factor.
        Exclusive with "pycont_contract_socket"
pycont_contract_socket:
        Socket that uwsgi will listen on.
        Exclusive with "pycont_contract_port"
