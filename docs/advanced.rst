Advanced Features
=================

Django Cruder provides several advanced features for complex applications.

Permissions and Security
------------------------

Role-Based Access Control
~~~~~~~~~~~~~~~~~~~~~~~~~

You can restrict CRUD operations based on user roles or groups:

.. code-block:: python

    def secure_crud(request, pk=None, action='list'):
        return crud_view(
            MyModel,
            permissions={
                'C': ['admin', 'editor'],  # Create: admin or editor
                'R': [],                   # Read: everyone (default)
                'U': ['admin'],           # Update: admin only
                'D': ['admin']            # Delete: admin only
            }
        )(request, pk, action)

Django Permissions
~~~~~~~~~~~~~~~~~~

Use Django's built-in permission system:

.. code-block:: python

    from django.contrib.auth.decorators import login_required, permission_required

    @login_required
    @permission_required('myapp.change_mymodel')
    def crud_view_with_perms(request, pk=None, action='list'):
        return crud_view(MyModel)(request, pk, action)

Read-Only Modes
---------------

Field-Level Read-Only
~~~~~~~~~~~~~~~~~~~~~

Make specific fields read-only while allowing editing of others:

.. code-block:: python

    crud_view(
        Contact,
        readonly_fields=['created_at', 'id', 'email']  # These fields become read-only
    )

Complete Read-Only Mode
~~~~~~~~~~~~~~~~~~~~~~

Make the entire interface read-only (no create, update, or delete):

.. code-block:: python

    crud_view(
        Contact,
        readonly_mode=True  # Disables all C,U,D operations
    )

Multi-Field Search
------------------

Enable search across multiple fields with OR logic:

.. code-block:: python

    crud_view(
        Contact,
        search_fields=['name', 'email', 'phone', 'company']
    )

This allows users to search for "john" and find results where any of those fields contain "john".

Custom Templates
----------------

Override Default Templates
~~~~~~~~~~~~~~~~~~~~~~~~~

You can override the default templates by creating your own in your project:

.. code-block:: text

    templates/
    └── cruder/
        ├── base.html
        ├── list.html
        ├── form.html
        ├── detail.html
        └── delete.html

Custom Base Template
~~~~~~~~~~~~~~~~~~~

Extend your own base template:

.. code-block:: html

    <!-- templates/cruder/base.html -->
    {% extends 'myapp/base.html' %}

    {% block content %}
        {% block cruder_content %}{% endblock %}
    {% endblock %}

Framework Customization
-----------------------

Adding New Frameworks
~~~~~~~~~~~~~~~~~~~~~

You can add support for new CSS frameworks by extending the base framework class:

.. code-block:: python

    from cruder.frameworks.base import BaseFramework

    class TailwindFramework(BaseFramework):
        name = 'tailwind'
        
        form_classes = {
            'form': 'space-y-4',
            'input': 'mt-1 block w-full rounded-md border-gray-300',
            'select': 'mt-1 block w-full rounded-md border-gray-300',
            'textarea': 'mt-1 block w-full rounded-md border-gray-300',
            'checkbox': 'rounded border-gray-300',
            'label': 'block text-sm font-medium text-gray-700',
            'help_text': 'mt-2 text-sm text-gray-500',
            'error': 'mt-2 text-sm text-red-600',
        }
        
        # ... implement other methods

Then register it:

.. code-block:: python

    from cruder.frameworks import register_framework
    register_framework('tailwind', TailwindFramework)

Pagination Customization
------------------------

Custom Page Size
~~~~~~~~~~~~~~~

Control how many items appear per page:

.. code-block:: python

    crud_view(MyModel, per_page=50)  # 50 items per page

The pagination automatically includes:

* Previous/Next navigation
* Page number links
* Item count display
* Search query preservation across pages

URL Customization
-----------------

Custom URL Patterns
~~~~~~~~~~~~~~~~~~~

If you need more control over URLs, you can create them manually:

.. code-block:: python

    # urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('my-custom-list/', views.my_crud, name='custom_list'),
        path('my-custom-list/new/', views.my_crud, {'action': 'create'}, name='custom_create'),
        path('my-custom-list/<int:pk>/', views.my_crud, {'action': 'view'}, name='custom_view'),
        path('my-custom-list/<int:pk>/edit/', views.my_crud, {'action': 'edit'}, name='custom_edit'),
        path('my-custom-list/<int:pk>/delete/', views.my_crud, {'action': 'delete'}, name='custom_delete'),
    ]

Error Handling
--------------

Django Cruder handles common errors gracefully:

* **404 errors**: When objects don't exist
* **Permission errors**: When users lack required permissions
* **Validation errors**: Form validation errors are displayed inline
* **Database errors**: Graceful handling of database constraints

Form Customization
------------------

Custom Form Fields
~~~~~~~~~~~~~~~~~

Django Cruder respects your model's field definitions:

.. code-block:: python

    class Contact(models.Model):
        email = models.EmailField()  # Automatically gets email input type
        age = models.IntegerField()  # Automatically gets number input type
        notes = models.TextField()   # Automatically gets textarea widget
        active = models.BooleanField()  # Automatically gets Yes/No dropdown

Field Ordering
~~~~~~~~~~~~~

Control field order in forms by specifying ``list_fields``:

.. code-block:: python

    crud_view(
        Contact,
        list_fields=['name', 'email', 'phone']  # Fields appear in this order
    )

Performance Considerations
-------------------------

QuerySet Optimization
~~~~~~~~~~~~~~~~~~~~

For large datasets, consider using ``select_related`` or ``prefetch_related``:

.. code-block:: python

    # In your model manager or view
    queryset = Contact.objects.select_related('company').all()
    
    # Pass custom queryset to render_list function
    from cruder.templates import render_list
    list_data = render_list(
        model_class=Contact,
        queryset=queryset,
        # ... other parameters
    )

Database Indexes
~~~~~~~~~~~~~~~

Add database indexes for fields used in search:

.. code-block:: python

    class Contact(models.Model):
        name = models.CharField(max_length=100, db_index=True)
        email = models.EmailField(db_index=True)
        # ...

This improves performance when using ``search_fields=['name', 'email']``.