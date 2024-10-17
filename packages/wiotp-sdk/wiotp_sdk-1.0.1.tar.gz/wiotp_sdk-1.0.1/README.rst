Python for IBM Watson IoT Platform
==================================

|GitHub issues| |GitHub| |PyPI| |Project Status| |Downloads| |image1|
|Code Style: Black|

Python module for interacting with **Maximo IoT** and `IBM Watson IoT
Platform <https://internetofthings.ibmcloud.com>`__

- Python 3.11
- Python 3.10
- Python 3.9

Product Withdrawal Notice
-------------------------

Per the September 8, 2020
`announcement <https://www-01.ibm.com/common/ssi/cgi-bin/ssialias?subtype=ca&infotype=an&appname=iSource&supplier=897&letternum=ENUS920-136#rprodnx>`__
IBM Watson IoT Platform (5900-A0N) has been withdrawn from marketing
effective **December 9, 2020**. As a result, updates to this project
will be limited.

Dependencies
------------

- `paho-mqtt <https://pypi.python.org/pypi/paho-mqtt>`__
- `iso8601 <https://pypi.python.org/pypi/iso8601>`__
- `pytz <https://pypi.python.org/pypi/pytz>`__
- `requests <https://pypi.python.org/pypi/requests>`__

Installation
------------

Install the `latest version <https://pypi.org/project/wiotp-sdk/>`__ of
the library with pip

::

   # pip install wiotp-sdk

Uninstall
---------

Uninstalling the module is simple.

::

   # pip uninstall wiotp-sdk

Documentation
-------------

https://ibm-watson-iot.github.io/iot-python/

Supported Features
------------------

- **Device Connectivity**: Connect your device(s) to Watson IoT Platform
  with ease using this library
- **Gateway Connectivity**: Connect your gateway(s) to Watson IoT
  Platform with ease using this library
- **Application connectivity**: Connect your application(s) to Watson
  IoT Platform with ease using this library
- **Watson IoT API**: Support for the interacting with the Watson IoT
  Platform through REST APIs
- **SSL/TLS**: By default, this library connects your devices, gateways
  and applications securely to Watson IoT Platform registered service.
  Ports ``8883`` (default) and ``443`` support secure connections using
  TLS with the MQTT and HTTP protocol. Support for MQTT with TLS
  requires at least Python v2.7.9 or v3.5, and openssl v1.0.1
- **Device Management for Device**: Connects your device(s) as managed
  device(s) to Watson IoT Platform.
- **Device Management for Gateway**: Connects your gateway(s) as managed
  device(s) to Watson IoT Platform.
- **Device Management Extensions**: Provides support for custom device
  management actions.
- **Scalable Applications**: Supports load balancing of MQTT
  subscriptions over multiple application instances.
- **Auto Reconnect**: All clients support automatic reconnect to the
  Platform in the event of a network interruption.
- **Websockets**: Support device/gateway/application connectivity to
  Watson IoT Platform using WebSocket

.. |GitHub issues| image:: https://img.shields.io/github/issues/ibm-watson-iot/iot-python.svg
   :target: https://github.com/ibm-watson-iot/iot-python/issues
.. |GitHub| image:: https://img.shields.io/github/license/ibm-watson-iot/iot-python.svg
   :target: https://github.com/ibm-watson-iot/iot-python/blob/master/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/wiotp-sdk.svg
   :target: https://pypi.org/project/wiotp-sdk/
.. |Project Status| image:: https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue
.. |Downloads| image:: https://pepy.tech/badge/ibmiotf
   :target: https://pepy.tech/project/ibmiotf
.. |image1| image:: https://pepy.tech/badge/wiotp-sdk
   :target: https://pepy.tech/project/wiotp-sdk
.. |Code Style: Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
