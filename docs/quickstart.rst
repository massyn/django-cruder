Quick Start Guide
=================

This guide will help you get Django Cruder up and running in minutes.

Installation
------------

Install Django Cruder using pip:

.. code-block:: bash

    pip install django-cruder

Add to your Django project's ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # Add django-cruder
        'cruder',
        
        # Your apps
        'myapp',
    ]

Basic Usage
-----------

1. Create Your Model
~~~~~~~~~~~~~~~~~~~~

First, create a Django model as you normally would:

.. code-block:: python

    # models.py
    from django.db import models

    class Contact(models.Model):
        name = models.CharField(max_length=100, verbose_name="Full Name")
        email_address = models.EmailField(verbose_name="Email")
        phone_number = models.CharField(max_length=20, verbose_name="Phone")
        active_client = models.BooleanField(default=True, verbose_name="Active")
        notes = models.TextField(blank=True, verbose_name="Notes")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.name

        class Meta:
            verbose_name = "Contact"
            verbose_name_plural = "Contacts"

2. Create Your CRUD View
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a view function that uses ``crud_view``:

.. code-block:: python

    # views.py
    from django.contrib.auth.decorators import login_required
    from cruder import crud_view
    from .models import Contact

    @login_required
    def contact_crud(request, pk=None, action='list'):
        return crud_view(
            Contact, 
            framework='bootstrap',
            exclude_fields=['created_at', 'updated_at'],
            list_fields=['name', 'email_address', 'phone_number', 'active_client'],
            readonly_fields=['name'],
            per_page=10,
            search_fields=['name', 'email_address', 'phone_number']
        )(request, pk, action)

3. Add URL Patterns
~~~~~~~~~~~~~~~~~~~

Use the ``crud_urlpatterns`` helper to automatically generate all CRUD URLs:

.. code-block:: python

    # urls.py
    from django.urls import path
    from cruder.urls import crud_urlpatterns
    from . import views

    app_name = 'myapp'

    urlpatterns = [
        path('', views.dashboard, name='dashboard'),
        # Add CRUD URLs - this creates 5 URL patterns automatically
    ] + crud_urlpatterns('contacts', views.contact_crud)

That's it! You now have a complete CRUD interface with:

* List view with search and pagination (``/contacts/``)
* Create form (``/contacts/create/``)
* Detail view (``/contacts/1/``)
* Edit form (``/contacts/1/edit/``)
* Delete confirmation (``/contacts/1/delete/``)

Available Parameters
--------------------

The ``crud_view`` function accepts many parameters to customize behavior:

Core Parameters
~~~~~~~~~~~~~~~

* ``model_class``: The Django model to create CRUD operations for
* ``framework``: CSS framework ('bootstrap' or 'bulma')

Display Parameters
~~~~~~~~~~~~~~~~~~

* ``exclude_fields``: List of fields to exclude from forms
* ``list_fields``: Fields to show in list view (defaults to all non-excluded)
* ``readonly_fields``: Fields that should be read-only in forms

Pagination & Search
~~~~~~~~~~~~~~~~~~~

* ``per_page``: Number of items per page (default: 25)
* ``search_fields``: List of fields to enable search across (OR logic)

Advanced Features
~~~~~~~~~~~~~~~~~

* ``readonly_mode``: Make entire interface read-only
* ``permissions``: Dict mapping CRUD operations to required roles
* ``permission_required``: Django permission required for access

Framework Support
-----------------

Bootstrap 5 (Default)
~~~~~~~~~~~~~~~~~~~~~

Django Cruder comes with built-in Bootstrap 5 support:

.. code-block:: python

    crud_view(MyModel, framework='bootstrap')

Bulma
~~~~~

Bulma framework support is also included:

.. code-block:: python

    crud_view(MyModel, framework='bulma')

Next Steps
----------

* Read the :doc:`api` documentation for full parameter reference
* Check out :doc:`advanced` features like permissions and custom templates
* Browse :doc:`examples` for more complex use cases