"""
Django Cruder - Advanced CRUD Operations for Django

A powerful Django package that provides instant, production-ready CRUD interfaces
with minimal code. Supports multiple CSS frameworks, advanced permissions, 
read-only modes, and multi-field search capabilities.

Features:
    - One-line CRUD: Complete CRUD operations with minimal code
    - Multi-framework support: Bootstrap 5, Bulma, and extensible for more
    - Advanced permissions: Role-based access control for operations
    - Multi-field search: OR search across multiple model fields
    - Read-only modes: Full read-only or field-level read-only controls
    - Auto-generated forms: Dynamic form generation from Django models
    - Smart pagination: Configurable pagination with search preservation
    - Template integration: Works seamlessly with existing Django templates

Example:
    Basic usage with a Django model:
    
    >>> from cruder import crud_view
    >>> from .models import Contact
    >>> 
    >>> def contact_crud(request, pk=None, action='list'):
    ...     return crud_view(
    ...         Contact,
    ...         search_fields=['name', 'email', 'phone'],
    ...         readonly_fields=['created_at'],
    ...         per_page=10
    ...     )(request, pk, action)

Requirements:
    - Python 3.8+
    - Django 3.2+
"""

__version__ = "1.0.0"
__author__ = "Phil Massyn"
__email__ = "phil.massyn@icloud.com"

from .views import CRUDView, crud_view
from .forms import CRUDForm, render_form
from .templates import render_list

__all__ = [
    'CRUDView',
    'crud_view', 
    'CRUDForm',
    'render_form',
    'render_list',
]