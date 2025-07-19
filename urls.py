"""
URL helper functions for Django Cruder
"""

from django.urls import path


def crud_urlpatterns(url_prefix, view_func, name_prefix=None):
    """
    Automatically generate all 5 CRUD URL patterns for a view function.
    
    This helper function creates URL patterns for all standard CRUD operations:
    list, create, view, edit, and delete. This eliminates the need to manually
    define multiple URL patterns for each CRUD interface.
    
    Args:
        url_prefix (str): URL prefix for the CRUD routes (e.g., 'contacts', 'products').
            Should not include leading/trailing slashes.
        view_func (callable): The view function that handles CRUD operations.
            This should be a function created with crud_view() or compatible.
        name_prefix (str, optional): Prefix for URL names. If None, derived from url_prefix.
            Example: 'contacts' -> 'contacts', 'contacts_create', etc.
    
    Returns:
        list: List of Django URL patterns for all CRUD operations:
            - GET  /{url_prefix}/                    (list)
            - GET  /{url_prefix}/create/            (create form)
            - POST /{url_prefix}/create/            (create form submission)
            - GET  /{url_prefix}/<int:pk>/          (view details)
            - GET  /{url_prefix}/<int:pk>/edit/     (edit form)
            - POST /{url_prefix}/<int:pk>/edit/     (edit form submission)
            - GET  /{url_prefix}/<int:pk>/delete/   (delete confirmation)
            - POST /{url_prefix}/<int:pk>/delete/   (delete confirmation)
    
    Example:
        Basic usage:
        
        >>> # urls.py
        >>> from cruder.urls import crud_urlpatterns
        >>> from . import views
        >>> 
        >>> urlpatterns = [
        ...     path('', views.dashboard, name='dashboard'),
        ... ] + crud_urlpatterns('contacts', views.contact_crud)
        
        Multiple CRUD interfaces:
        
        >>> urlpatterns = [
        ...     path('', views.dashboard, name='dashboard'),
        ... ] + crud_urlpatterns('contacts', views.contact_crud) \
        ...   + crud_urlpatterns('products', views.product_crud) \
        ...   + crud_urlpatterns('orders', views.order_crud)
        
        Custom name prefix:
        
        >>> urlpatterns = crud_urlpatterns(
        ...     'admin/users', 
        ...     views.user_crud, 
        ...     name_prefix='admin_users'
        ... )
        
    Note:
        The view function must accept the parameters (request, pk=None, action='list')
        where action can be 'list', 'create', 'view', 'edit', or 'delete'.
    """
    # Clean up url_prefix and generate name_prefix
    url_prefix = url_prefix.rstrip('/')
    if name_prefix is None:
        name_prefix = url_prefix.replace('/', '_').strip('_')
    
    return [
        path(f'{url_prefix}/', view_func, name=f'{name_prefix}'),
        path(f'{url_prefix}/create/', view_func, {'action': 'create'}, name=f'{name_prefix}_create'),
        path(f'{url_prefix}/<int:pk>/', view_func, {'action': 'view'}, name=f'{name_prefix}_detail'),
        path(f'{url_prefix}/<int:pk>/edit/', view_func, {'action': 'edit'}, name=f'{name_prefix}_edit'),
        path(f'{url_prefix}/<int:pk>/delete/', view_func, {'action': 'delete'}, name=f'{name_prefix}_delete'),
    ]