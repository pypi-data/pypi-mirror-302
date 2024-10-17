========================
drf-spectecular-json-api
========================

open api 3 schema generator for `drf-json-api <https://github.com/django-json-api/django-rest-framework-json-api>`_ package based on `drf-spectacular <https://github.com/tfranzel/drf-spectacular>`__ package.

Tested with various dependency version
--------------------------------------

.. list-table:: Tested for versions in combination:
   :widths: 25 25 50
   :header-rows: 1

   * - python
     - django
     - drf-spectacular
   * - 3.8
     - 4.0
     - 0.25.x
   * - 3.9
     - 4.1
     - 0.26.x
   * - 3.10
     - 4.2
     - 0.27.x
   * - 3.11
     - 5.0
     - 

Installation
------------

.. note::
    Install `django-rest-framework <https://www.django-rest-framework.org/>`_, `django-rest-framework-json-api <https://django-rest-framework-json-api.readthedocs.io/en/stable/>`_ and `drf-spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`__ as described by them first.

Install using ``pip``\ ...

.. code:: bash

    $ pip install drf-spectacular-jsonapi

then configure the rest framework and drf-spectacular with the following settings inside your project ``settings.py``

.. code:: python

    REST_FRAMEWORK = {
        # YOUR SETTINGS
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular_jsonapi.schemas.openapi.JsonApiAutoSchema",
        "DEFAULT_PAGINATION_CLASS": "drf_spectacular_jsonapi.schemas.pagination.JsonApiPageNumberPagination",
    }
    SPECTACULAR_SETTINGS = {
        # To provide different schema components for patch and post
        "COMPONENT_SPLIT_REQUEST": True
        # to fix path parameter names for nested routes https://chibisov.github.io/drf-extensions/docs/#nested-routes
        "PREPROCESSING_HOOKS": [
            "drf_spectacular_jsonapi.hooks.fix_nested_path_parameters"
        ],
    }


Release management
^^^^^^^^^^^^^^^^^^

Same as the based *drf-spectacular* package, we provide versions below sem version *1.x.x* to signal that every new version may potentially break you.
