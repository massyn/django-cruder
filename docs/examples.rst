Examples
========

This page contains practical examples of using Django Cruder in real-world scenarios.

Basic Contact Management
-----------------------

A simple contact management system:

.. code-block:: python

    # models.py
    from django.db import models

    class Contact(models.Model):
        name = models.CharField(max_length=100, verbose_name="Full Name")
        email = models.EmailField(verbose_name="Email Address")
        phone = models.CharField(max_length=20, verbose_name="Phone Number")
        company = models.CharField(max_length=100, blank=True)
        active = models.BooleanField(default=True)
        notes = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

    # views.py
    from django.contrib.auth.decorators import login_required
    from cruder import crud_view
    from .models import Contact

    @login_required
    def contact_crud(request, pk=None, action='list'):
        return crud_view(
            Contact,
            exclude_fields=['created_at'],
            list_fields=['name', 'email', 'phone', 'company', 'active'],
            search_fields=['name', 'email', 'phone', 'company'],
            per_page=20
        )(request, pk, action)

    # urls.py
    from cruder.urls import crud_urlpatterns
    urlpatterns = crud_urlpatterns('contacts', views.contact_crud)

E-commerce Product Catalog
--------------------------

A product catalog with different permission levels:

.. code-block:: python

    # models.py
    class Category(models.Model):
        name = models.CharField(max_length=100)
        slug = models.SlugField(unique=True)

        def __str__(self):
            return self.name

    class Product(models.Model):
        name = models.CharField(max_length=200)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        stock = models.IntegerField(default=0)
        description = models.TextField()
        active = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

    # views.py
    from django.contrib.auth.decorators import login_required
    from cruder import crud_view

    @login_required
    def product_crud(request, pk=None, action='list'):
        return crud_view(
            Product,
            exclude_fields=['created_at'],
            list_fields=['name', 'category', 'price', 'stock', 'active'],
            search_fields=['name', 'description'],
            permissions={
                'C': ['admin', 'manager'],  # Only admin/manager can create
                'U': ['admin', 'manager'],  # Only admin/manager can update  
                'D': ['admin']              # Only admin can delete
            },
            per_page=25
        )(request, pk, action)

    @login_required
    def category_crud(request, pk=None, action='list'):
        return crud_view(
            Category,
            permissions={'C': ['admin'], 'U': ['admin'], 'D': ['admin']},
            search_fields=['name']
        )(request, pk, action)

Project Management System
-------------------------

A project tracking system with read-only fields:

.. code-block:: python

    # models.py
    class Project(models.Model):
        STATUS_CHOICES = [
            ('planning', 'Planning'),
            ('active', 'Active'),
            ('on_hold', 'On Hold'),
            ('completed', 'Completed'),
        ]

        name = models.CharField(max_length=200)
        description = models.TextField()
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
        start_date = models.DateField()
        end_date = models.DateField(null=True, blank=True)
        budget = models.DecimalField(max_digits=10, decimal_places=2)
        manager = models.ForeignKey('auth.User', on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.name

    # views.py
    @login_required
    def project_crud(request, pk=None, action='list'):
        return crud_view(
            Project,
            exclude_fields=['created_at', 'updated_at'],
            list_fields=['name', 'status', 'start_date', 'manager', 'budget'],
            readonly_fields=['created_at', 'manager'],  # Manager set on creation
            search_fields=['name', 'description'],
            per_page=15
        )(request, pk, action)

Multi-Framework Example
----------------------

Using different frameworks for different sections:

.. code-block:: python

    # Admin interface with Bootstrap
    @user_passes_test(lambda u: u.is_staff)
    def admin_users_crud(request, pk=None, action='list'):
        return crud_view(
            User,
            framework='bootstrap',
            list_fields=['username', 'email', 'first_name', 'last_name', 'is_active'],
            readonly_fields=['username', 'date_joined'],
            permissions={'D': ['admin']},
            search_fields=['username', 'email', 'first_name', 'last_name']
        )(request, pk, action)

    # Public-facing interface with Bulma
    @login_required
    def public_profile_crud(request, pk=None, action='list'):
        return crud_view(
            UserProfile,
            framework='bulma',
            exclude_fields=['user'],
            readonly_mode=True  # Users can only view, not edit
        )(request, pk, action)

Read-Only Dashboard
------------------

A dashboard view that only allows viewing data:

.. code-block:: python

    # models.py
    class SalesReport(models.Model):
        date = models.DateField()
        total_sales = models.DecimalField(max_digits=10, decimal_places=2)
        orders_count = models.IntegerField()
        top_product = models.CharField(max_length=200)
        region = models.CharField(max_length=100)

        class Meta:
            ordering = ['-date']

    # views.py
    @login_required
    def sales_dashboard(request, pk=None, action='list'):
        return crud_view(
            SalesReport,
            readonly_mode=True,  # No create/edit/delete
            list_fields=['date', 'total_sales', 'orders_count', 'top_product', 'region'],
            search_fields=['region', 'top_product'],
            per_page=50
        )(request, pk, action)

Custom URL Structure
-------------------

Using custom URL patterns instead of the helper:

.. code-block:: python

    # urls.py
    from django.urls import path
    from . import views

    app_name = 'inventory'

    urlpatterns = [
        # Custom URL structure
        path('items/', views.item_crud, name='item_list'),
        path('items/add/', views.item_crud, {'action': 'create'}, name='item_add'),
        path('items/<int:pk>/view/', views.item_crud, {'action': 'view'}, name='item_view'),
        path('items/<int:pk>/modify/', views.item_crud, {'action': 'edit'}, name='item_modify'),
        path('items/<int:pk>/remove/', views.item_crud, {'action': 'delete'}, name='item_remove'),
        
        # Categories with standard URLs
    ] + crud_urlpatterns('categories', views.category_crud)

Blog Management
--------------

A blog with different access levels:

.. code-block:: python

    # models.py
    class BlogPost(models.Model):
        title = models.CharField(max_length=200)
        slug = models.SlugField(unique=True)
        content = models.TextField()
        author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
        published = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title

    # views.py
    # Authors can edit their own posts
    @login_required
    def my_posts_crud(request, pk=None, action='list'):
        return crud_view(
            BlogPost,
            queryset=BlogPost.objects.filter(author=request.user),
            exclude_fields=['author', 'created_at', 'updated_at'],
            readonly_fields=['slug'],
            search_fields=['title', 'content']
        )(request, pk, action)

    # Editors can manage all posts
    @user_passes_test(lambda u: u.groups.filter(name='editors').exists())
    def all_posts_crud(request, pk=None, action='list'):
        return crud_view(
            BlogPost,
            list_fields=['title', 'author', 'published', 'created_at'],
            search_fields=['title', 'content', 'author__username'],
            per_page=30
        )(request, pk, action)

Navigation Integration
---------------------

Integrating with a navigation system:

.. code-block:: python

    # views.py with navigation decorator
    from myapp.navigation import nav_item

    @nav_item('app:contacts', 'Contacts', 'bi-people', order=30)
    @login_required
    def contact_crud(request, pk=None, action='list'):
        return crud_view(Contact, search_fields=['name', 'email'])(request, pk, action)

    @nav_item('app:projects', 'Projects', 'bi-kanban', order=40)
    @login_required  
    def project_crud(request, pk=None, action='list'):
        return crud_view(Project, search_fields=['name'])(request, pk, action)

These examples demonstrate the flexibility and power of Django Cruder for various use cases, from simple contact management to complex multi-user systems with permissions and custom workflows.