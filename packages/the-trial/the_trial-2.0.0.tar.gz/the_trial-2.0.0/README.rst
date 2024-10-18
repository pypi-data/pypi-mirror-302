========
theTrial
========

.. DYNAMIC

.. image:: https://img.shields.io/pypi/v/TODO
   :target: https://pypi.org/project/TODO
   :alt: pypi

.. image:: https://github.com/donMichaelL/test_package/actions/workflows/main.yaml/badge.svg?branch=main
    :target: https://github.com/donMichaelL/test_package/actions/workflows/main.yaml
    :alt: Main Workflow Status

.. image:: https://img.shields.io/github/actions/workflow/status/donMichaelL/test_package/main.yaml.svg?branch=main&style=for-the-badge
    :target: https://github.com/donMichaelL/test_package/actions/workflows/main.yaml
    :alt: Main Workflow Status

.. STATIC

.. image:: https://img.shields.io/badge/pre--commit-enabled-%2300A36C%09
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. image:: https://img.shields.io/badge/Code_Style-black-black?color=black
   :target: https://github.com/psf/black
   :alt: black

.. image:: https://img.shields.io/badge/License-MIT-blue
   :target: https://github.com/donMichaelL/theTrial/blob/master/LICENSE
   :alt: license

``theTrial`` is a microframework designed to provide a simple interface for interacting with Kafka.
It simplifies the process of setting up consumers and producers for Kafka topics using Pythonic decorators.
Under the hood, it uses `confluent-kafka <https://github.com/confluentinc/confluent-kafka-python>`_ to communicate synchronously with Kafka clusters.

Installation
------------

Install from pip:

.. code-block:: bash

   python -m pip install theTrial

Quick Start
-----------

Here's a simple example to get you started:

.. code-block:: python

   from theTrial import TheTrial

   app = TheTrial()


Settings Configuration
----------------------

For a detailed explanation and additional configuration options, refer to the official Confluent documentation: `Confluent Kafka Python Documentation <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html>`_.

User-Defined Settings
^^^^^^^^^^^^^^^^^^^^^


Logging Configuration
---------------------

``theTrial`` employs and extends Python's built-in logging module for system logging.

CLI Commands
------------

`theTrial` includes a set of CLI commands to set up and manage your projects.

Start Command
^^^^^^^^^^^^^

To initialize a new project structure, use the `start` command:

.. code-block:: bash

   theTrial start --name [YOUR_APP_NAME]

By default, the main app file will be named `app.py`. You can specify a different name using the ``--name`` option.

This command will:

- Create the main app file (`[YOUR_APP_NAME].py`).
