Django Cruder Documentation
===========================

Django Cruder is a powerful CRUD operations library for Django that provides instant, production-ready CRUD interfaces with minimal code. It supports multiple CSS frameworks and advanced features like permissions, read-only modes, and multi-field search.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   advanced
   examples

Quick Start
-----------

Install Django Cruder:

.. code-block:: bash

   pip install django-cruder

Add to your Django settings:

.. code-block:: python

   INSTALLED_APPS = [
       # ... your other apps
       'cruder',
   ]

Create a complete CRUD interface in just a few lines:

.. code-block:: python

   # models.py
   from django.db import models

   class Contact(models.Model):
       name = models.CharField(max_length=100)
       email = models.EmailField()
       phone = models.CharField(max_length=20)
       active = models.BooleanField(default=True)

   # views.py
   from cruder import crud_view
   from .models import Contact

   def contact_crud(request, pk=None, action='list'):
       return crud_view(
           Contact,
           search_fields=['name', 'email', 'phone'],
           readonly_fields=['name'],
           per_page=10
       )(request, pk, action)

   # urls.py
   from cruder.urls import crud_urlpatterns
   from . import views

   urlpatterns = [
       # ... your other URLs
   ] + crud_urlpatterns('contacts', views.contact_crud)

Features
--------

* **One-line CRUD**: Complete CRUD operations with minimal code
* **Multi-framework support**: Bootstrap 5, Bulma, and extensible for more
* **Advanced permissions**: Role-based access control for operations
* **Multi-field search**: OR search across multiple model fields
* **Read-only modes**: Full read-only or field-level read-only controls
* **Auto-generated forms**: Dynamic form generation from Django models
* **Smart pagination**: Configurable pagination with search preservation
* **Template integration**: Works seamlessly with your existing Django templates

Requirements
------------

* Python 3.8+
* Django 3.2+

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`