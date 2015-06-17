What are the changes to consider when you upgrade from 1.0.x to 1.1.x ?
=======================================================================

When upgrading from Cohorte 1.0.x you should take in consideration these changes :

Startup script (run)
--------------------

From Cohorte 1.1, the following arguments where changed (and also their corresponding run.js entries):

* ``--web-admin`` => ``--http-port``
* ``--shell-admin`` => ``--shell-port``
  
By default the node starts without the console activated. To activate it on startup, you should add this argument:

* ``--console``

Run configuration files (e.g., run.js) also updates its content :

* ``application-id`` => ``app-id``
* ``web-admin`` => ``http-port``
* ``shell-admin`` => ``shell-port``

