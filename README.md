# Django Cruder

Advanced CRUD operations for Django with multiple CSS framework support and powerful features.

[![Documentation Status](https://readthedocs.org/projects/django-cruder/badge/?version=latest)](https://django-cruder.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/django-cruder.svg)](https://badge.fury.io/py/django-cruder)

## 🚀 Quick Start

### Installation

```bash
pip install django-cruder
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'cruder',
]
```

### 1. Create Your Model

```python
# models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email_address = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Phone")
    active_client = models.BooleanField(default=True, verbose_name="Active")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
```

### 2. Create Your View (One Line!)

```python
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
```

### 3. Add URLs (One Line!)

```python
# urls.py
from cruder.urls import crud_urlpatterns
from . import views

urlpatterns = [
    # ... your other URLs
] + crud_urlpatterns('contacts', views.contact_crud)
```

**That's it!** You now have a complete CRUD interface with:
- ✅ List view with multi-field search and pagination
- ✅ Create form with validation
- ✅ View details
- ✅ Edit form with read-only fields
- ✅ Delete confirmation
- ✅ Bootstrap 5 styling
- ✅ Permission-based access control

## 🌟 Features

### Core Features
- **One-line CRUD**: Complete CRUD operations with minimal code
- **Multi-framework support**: Bootstrap 5, Bulma, and extensible for more
- **Auto-generated forms**: Dynamic form generation from Django models
- **Smart list views**: Automatic table generation with pagination and search
- **Template integration**: Works seamlessly with your existing Django templates

### Advanced Features
- **Multi-field search**: OR search across multiple model fields
- **Read-only modes**: Full read-only or field-level read-only controls
- **Permission system**: Role-based access control for CRUD operations
- **Framework flexibility**: Easy switching between CSS frameworks
- **Custom templates**: Override any template for full customization

## 📚 Documentation

Full documentation is available at [django-cruder.readthedocs.io](https://django-cruder.readthedocs.io/)

## 🔧 API Reference

### `crud_view(model_class, framework='bootstrap', **kwargs)`

**Core Parameters:**
- `model_class`: Django model class
- `framework`: CSS framework ('bootstrap' or 'bulma')

**Display Parameters:**
- `exclude_fields`: List of fields to exclude from forms
- `list_fields`: Fields to show in list view (defaults to all non-excluded)
- `readonly_fields`: Fields that should be read-only in forms

**Search & Pagination:**
- `search_fields`: List of fields to enable search across (OR logic)
- `per_page`: Items per page for pagination (default: 25)

**Advanced Features:**
- `readonly_mode`: Make entire interface read-only
- `permissions`: Dict mapping CRUD operations to required roles
- `permission_required`: Django permission required for access

### URL Helper

```python
crud_urlpatterns(url_prefix, view_func, name_prefix=None)
```

Automatically generates all 5 CRUD URL patterns:
- List: `/{url_prefix}/`
- Create: `/{url_prefix}/create/`
- View: `/{url_prefix}/<int:pk>/`
- Edit: `/{url_prefix}/<int:pk>/edit/`
- Delete: `/{url_prefix}/<int:pk>/delete/`

## 🎨 Framework Support

### Bootstrap 5 (Default)
```python
crud_view(MyModel, framework='bootstrap')
```

### Bulma
```python
crud_view(MyModel, framework='bulma')
```

### Custom Frameworks
Easily add support for any CSS framework by extending `BaseFramework`.

## 🔒 Security Features

### Role-Based Permissions
```python
crud_view(
    MyModel,
    permissions={
        'C': ['admin', 'editor'],  # Create: admin or editor
        'R': [],                   # Read: everyone
        'U': ['admin'],           # Update: admin only
        'D': ['admin']            # Delete: admin only
    }
)
```

### Django Permissions
```python
@permission_required('myapp.change_mymodel')
def my_crud_view(request, pk=None, action='list'):
    return crud_view(MyModel)(request, pk, action)
```

## 🔍 Advanced Search

Multi-field search with OR logic:
```python
crud_view(
    Contact,
    search_fields=['name', 'email', 'phone', 'company']
)
```

## 📝 Field Type Support

Django Cruder automatically handles all Django field types:

- **Text Fields**: CharField, TextField, EmailField, URLField
- **Numeric Fields**: IntegerField, FloatField, DecimalField
- **Date/Time Fields**: DateField, DateTimeField, TimeField
- **Boolean Fields**: BooleanField with Yes/No dropdown
- **Choice Fields**: Automatic dropdown generation
- **Foreign Keys**: Basic support with proper display
- **File Fields**: FileField and ImageField support

## 🛠️ Requirements

- Python 3.8+
- Django 3.2+

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

## 📞 Support

- Documentation: [django-cruder.readthedocs.io](https://django-cruder.readthedocs.io/)
- Issues: [GitHub Issues](https://github.com/massyn/django-cruder/issues)
- Discussions: [GitHub Discussions](https://github.com/massyn/django-cruder/discussions)