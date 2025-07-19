"""
CRUD view classes and wrapper functions for Django models
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from .forms import render_form, create_model_form
from .templates import render_list


class CRUDView(View):
    """
    Generic CRUD view class that handles all CRUD operations for a model
    """
    model = None
    framework = 'bootstrap'
    template_name = None
    exclude_fields = None
    list_fields = None
    per_page = 25
    search_fields = None
    search_field = None  # Deprecated, use search_fields
    permission_required = None
    
    # New features
    readonly_fields = None  # List of fields to show as read-only
    permissions = None      # Dict mapping CRUD operations to required roles/groups
                           # Example: {'C': ['admin', 'editor'], 'U': ['admin'], 'D': ['admin']}
    readonly_mode = False   # If True, entire view is read-only (no C,U,D operations)
    
    def has_crud_permission(self, user, operation):
        """
        Check if user has permission for CRUD operation
        
        Args:
            user: Django user object
            operation: 'C', 'R', 'U', or 'D'
        
        Returns:
            bool: True if user has permission
        """
        if self.readonly_mode and operation in ['C', 'U', 'D']:
            return False
            
        if not self.permissions:
            return True  # No restrictions defined, allow all
            
        required_roles = self.permissions.get(operation, [])
        if not required_roles:
            return True  # No roles required for this operation
            
        # Check if user has any of the required roles/groups
        user_groups = [group.name for group in user.groups.all()]
        
        # Also check if user is superuser
        if user.is_superuser:
            return True
            
        # Check if user has any of the required roles
        return any(role in user_groups for role in required_roles)
    
    def dispatch(self, request, *args, **kwargs):
        """Check permissions before processing request"""
        if self.permission_required and not request.user.has_perm(self.permission_required):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk=None, action='list'):
        """Handle GET requests for list, create, edit, view actions"""
        if action == 'list':
            if not self.has_crud_permission(request.user, 'R'):
                raise PermissionDenied("You don't have permission to view this content.")
            return self.list_view(request)
        elif action == 'create':
            if not self.has_crud_permission(request.user, 'C'):
                raise PermissionDenied("You don't have permission to create new items.")
            return self.create_view(request)
        elif action == 'edit' and pk:
            if not self.has_crud_permission(request.user, 'U'):
                raise PermissionDenied("You don't have permission to edit items.")
            return self.edit_view(request, pk)
        elif action == 'view' and pk:
            if not self.has_crud_permission(request.user, 'R'):
                raise PermissionDenied("You don't have permission to view this content.")
            return self.detail_view(request, pk)
        elif action == 'delete' and pk:
            if not self.has_crud_permission(request.user, 'D'):
                raise PermissionDenied("You don't have permission to delete items.")
            return self.delete_view(request, pk)
        else:
            return self.list_view(request)
    
    def post(self, request, pk=None, action='create'):
        """Handle POST requests for create, update, delete actions"""
        if action == 'create':
            if not self.has_crud_permission(request.user, 'C'):
                raise PermissionDenied("You don't have permission to create new items.")
            return self.create_post(request)
        elif action == 'edit' and pk:
            if not self.has_crud_permission(request.user, 'U'):
                raise PermissionDenied("You don't have permission to edit items.")
            return self.edit_post(request, pk)
        elif action == 'delete' and pk:
            if not self.has_crud_permission(request.user, 'D'):
                raise PermissionDenied("You don't have permission to delete items.")
            return self.delete_post(request, pk)
        else:
            return self.list_view(request)
    
    def list_view(self, request):
        """Display list of model objects"""
        page = request.GET.get('page', 1)
        search_query = request.GET.get('search', '')
        
        # Get current URL base for proper action links
        current_url = request.path
        if current_url.endswith('/'):
            base_url = current_url
        else:
            base_url = current_url + '/'
            
        # Check permissions for action buttons
        permissions_context = {
            'can_create': self.has_crud_permission(request.user, 'C'),
            'can_read': self.has_crud_permission(request.user, 'R'),
            'can_update': self.has_crud_permission(request.user, 'U'),
            'can_delete': self.has_crud_permission(request.user, 'D'),
        }
        
        list_data = render_list(
            model_class=self.model,
            framework=self.framework,
            fields=self.list_fields,
            per_page=self.per_page,
            page=page,
            search_fields=self.search_fields,
            search_field=self.search_field,  # For backward compatibility
            search_query=search_query,
            base_url=base_url,
            permissions=permissions_context
        )
        
        context = {
            'list_html': list_data['html'],
            'page_obj': list_data['page_obj'],
            'total_count': list_data['total_count'],
            'model_name': self.model._meta.verbose_name,
            'model_name_plural': self.model._meta.verbose_name_plural,
            'permissions': permissions_context,
        }
        
        template = self.template_name or 'cruder/list.html'
        return render(request, template, context)
    
    def create_view(self, request):
        """Display create form"""
        from .forms import create_model_form
        form_class = create_model_form(self.model, self.framework, self.exclude_fields)
        form = form_class()
        
        context = {
            'form': form,
            'model_name': self.model._meta.verbose_name,
            'action': 'Create',
            'framework': self.framework,
            'readonly_fields': self.readonly_fields or [],
            'readonly_mode': self.readonly_mode,
        }
        
        template = self.template_name or 'cruder/form.html'
        return render(request, template, context)
    
    def create_post(self, request):
        """Handle create form submission"""
        form_class = create_model_form(self.model, self.framework, self.exclude_fields)
        form = form_class(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"{self.model._meta.verbose_name} created successfully!")
            # Redirect back to list view
            current_path = request.path
            if '/create/' in current_path:
                list_url = current_path.replace('/create/', '/')
            elif current_path.endswith('/create'):
                list_url = current_path.replace('/create', '/')
            elif '/edit/' in current_path:
                list_url = current_path.split('/edit/')[0] + '/'
            elif '/delete/' in current_path:
                list_url = current_path.split('/delete/')[0] + '/'
            else:
                list_url = current_path if current_path.endswith('/') else current_path + '/'
            return redirect(list_url)
        else:
            # Re-render form with errors
            context = {
                'form': form,
                'model_name': self.model._meta.verbose_name,
                'action': 'Create',
                'errors': form.errors,
            }
            template = self.template_name or 'cruder/form.html'
            return render(request, template, context)
    
    def edit_view(self, request, pk):
        """Display edit form"""
        obj = get_object_or_404(self.model, pk=pk)
        from .forms import create_model_form
        form_class = create_model_form(self.model, self.framework, self.exclude_fields)
        form = form_class(instance=obj)
        
        context = {
            'form': form,
            'object': obj,
            'model_name': self.model._meta.verbose_name,
            'action': 'Edit',
            'framework': self.framework,
            'readonly_fields': self.readonly_fields or [],
            'readonly_mode': self.readonly_mode,
        }
        
        template = self.template_name or 'cruder/form.html'
        return render(request, template, context)
    
    def edit_post(self, request, pk):
        """Handle edit form submission"""
        obj = get_object_or_404(self.model, pk=pk)
        form_class = create_model_form(self.model, self.framework, self.exclude_fields)
        form = form_class(request.POST, request.FILES, instance=obj)
        
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"{self.model._meta.verbose_name} updated successfully!")
            # Redirect back to list view
            current_path = request.path
            if '/create/' in current_path:
                list_url = current_path.replace('/create/', '/')
            elif current_path.endswith('/create'):
                list_url = current_path.replace('/create', '/')
            elif '/edit/' in current_path:
                list_url = current_path.split('/edit/')[0] + '/'
            elif '/delete/' in current_path:
                list_url = current_path.split('/delete/')[0] + '/'
            else:
                list_url = current_path if current_path.endswith('/') else current_path + '/'
            return redirect(list_url)
        else:
            # Re-render form with errors
            context = {
                'form': form,
                'object': obj,
                'model_name': self.model._meta.verbose_name,
                'action': 'Edit',
                'errors': form.errors,
            }
            template = self.template_name or 'cruder/form.html'
            return render(request, template, context)
    
    def detail_view(self, request, pk):
        """Display object details"""
        obj = get_object_or_404(self.model, pk=pk)
        
        # Get field information for template
        fields_data = []
        for field in self.model._meta.get_fields():
            if not field.name.endswith('_set') and field.name != 'id':
                try:
                    field_name = field.name
                    field_label = getattr(field, 'verbose_name', field_name.replace('_', ' ').title())
                    field_value = getattr(obj, field_name, None)
                    
                    # Format the value
                    if hasattr(field_value, 'strftime'):  # DateTime fields
                        field_value = field_value.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(field_value, bool):
                        field_value = 'Yes' if field_value else 'No'
                    elif field_value is None:
                        field_value = 'Not set'
                    
                    fields_data.append({
                        'name': field_name,
                        'label': field_label,
                        'value': field_value
                    })
                except:
                    continue
        
        context = {
            'object': obj,
            'model_name': self.model._meta.verbose_name,
            'fields_data': fields_data,
        }
        
        template = self.template_name or 'cruder/detail.html'
        return render(request, template, context)
    
    def delete_view(self, request, pk):
        """Display delete confirmation"""
        obj = get_object_or_404(self.model, pk=pk)
        
        # Get field information for template (same as detail view)
        fields_data = []
        for field in self.model._meta.get_fields():
            if not field.name.endswith('_set') and field.name != 'id':
                try:
                    field_name = field.name
                    field_label = getattr(field, 'verbose_name', field_name.replace('_', ' ').title())
                    field_value = getattr(obj, field_name, None)
                    
                    # Format the value
                    if hasattr(field_value, 'strftime'):  # DateTime fields
                        field_value = field_value.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(field_value, bool):
                        field_value = 'Yes' if field_value else 'No'
                    elif field_value is None:
                        field_value = 'Not set'
                    
                    fields_data.append({
                        'name': field_name,
                        'label': field_label,
                        'value': field_value
                    })
                except:
                    continue
        
        context = {
            'object': obj,
            'model_name': self.model._meta.verbose_name,
            'fields_data': fields_data,
        }
        
        template = self.template_name or 'cruder/delete.html'
        return render(request, template, context)
    
    def delete_post(self, request, pk):
        """Handle delete confirmation"""
        obj = get_object_or_404(self.model, pk=pk)
        obj_name = str(obj)
        obj.delete()
        messages.success(request, f"{self.model._meta.verbose_name} '{obj_name}' deleted successfully!")
        # Redirect back to list view
        current_path = request.path
        # For /app/contacts/4/delete/ -> /app/contacts/
        if '/delete/' in current_path:
            # Split on /delete/ and take the first part, then remove the ID
            base_path = current_path.split('/delete/')[0]  # /app/contacts/4
            path_parts = base_path.rstrip('/').split('/')  # ['', 'app', 'contacts', '4']
            if path_parts[-1].isdigit():  # Remove ID if present
                list_url = '/'.join(path_parts[:-1]) + '/'  # /app/contacts/
            else:
                list_url = base_path + '/'
        else:
            list_url = current_path if current_path.endswith('/') else current_path + '/'
        return redirect(list_url)


def crud_view(model_class, framework='bootstrap', **kwargs):
    """
    Create a complete CRUD view for a Django model with one function call.
    
    This function generates a Django view that handles all CRUD operations:
    Create, Read, Update, Delete, and List with search and pagination.
    
    Args:
        model_class (django.db.models.Model): The Django model to create CRUD operations for.
        framework (str, optional): CSS framework to use. Defaults to 'bootstrap'.
            Supported: 'bootstrap', 'bulma'.
        **kwargs: Additional configuration options:
        
            Display Options:
                exclude_fields (list): Fields to exclude from forms.
                list_fields (list): Fields to show in list view.
                readonly_fields (list): Fields that should be read-only in forms.
                readonly_mode (bool): Make entire interface read-only.
                
            Search & Pagination:
                search_fields (list): Fields to enable search across (OR logic).
                per_page (int): Items per page for pagination. Default: 25.
                
            Permissions:
                permissions (dict): Role-based permissions mapping.
                    Example: {'C': ['admin'], 'U': ['admin'], 'D': ['admin']}
                permission_required (str): Django permission required for access.
                
            Templates:
                template_name (str): Custom template to use instead of defaults.
    
    Returns:
        function: A Django view function that handles all CRUD operations.
        
    Example:
        Basic usage:
        
        >>> from cruder import crud_view
        >>> from .models import Contact
        >>> 
        >>> @login_required
        >>> def contact_crud(request, pk=None, action='list'):
        ...     return crud_view(
        ...         Contact,
        ...         search_fields=['name', 'email', 'phone'],
        ...         readonly_fields=['created_at'],
        ...         per_page=10
        ...     )(request, pk, action)
        
        With permissions:
        
        >>> def secure_crud(request, pk=None, action='list'):
        ...     return crud_view(
        ...         MyModel,
        ...         permissions={
        ...             'C': ['admin', 'editor'],
        ...             'U': ['admin'],
        ...             'D': ['admin']
        ...         }
        ...     )(request, pk, action)
    
    Note:
        The returned view function expects three parameters: request, pk (optional), 
        and action (defaults to 'list'). The action parameter determines which 
        CRUD operation to perform: 'list', 'create', 'view', 'edit', or 'delete'.
    """
    class DynamicCRUDView(CRUDView):
        model = model_class
    
    # Set framework and other attributes after class creation
    DynamicCRUDView.framework = framework
    
    # Override any provided kwargs
    for key, value in kwargs.items():
        setattr(DynamicCRUDView, key, value)
    
    return DynamicCRUDView.as_view()


def render_crud_list(model_class, request, framework='bootstrap', **kwargs):
    """
    Function to render just the list view
    
    Args:
        model_class: Django model class
        request: Django request object
        framework: CSS framework name
        **kwargs: Additional arguments for render_list
    
    Returns:
        HttpResponse with rendered list
    """
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    
    list_data = render_list(
        model_class=model_class,
        framework=framework,
        page=page,
        search_query=search_query,
        **kwargs
    )
    
    context = {
        'list_html': list_data['html'],
        'page_obj': list_data['page_obj'],
        'total_count': list_data['total_count'],
        'model_name': model_class._meta.verbose_name,
        'model_name_plural': model_class._meta.verbose_name_plural,
    }
    
    return render(request, 'cruder/list.html', context)


def render_crud_form(model_class, request, pk=None, framework='bootstrap', **kwargs):
    """
    Function to render just the form view
    
    Args:
        model_class: Django model class
        request: Django request object
        pk: Primary key for editing (None for create)
        framework: CSS framework name
        **kwargs: Additional arguments for render_form
    
    Returns:
        HttpResponse with rendered form
    """
    instance = None
    if pk:
        instance = get_object_or_404(model_class, pk=pk)
    
    if request.method == 'POST':
        form_class = create_model_form(model_class, framework)
        form = form_class(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            obj = form.save()
            action = "updated" if instance else "created"
            messages.success(request, f"{model_class._meta.verbose_name} {action} successfully!")
            # Redirect back to list view
            current_path = request.path
            if '/create/' in current_path:
                list_url = current_path.replace('/create/', '/')
            elif current_path.endswith('/create'):
                list_url = current_path.replace('/create', '/')
            elif '/edit/' in current_path:
                list_url = current_path.split('/edit/')[0] + '/'
            elif '/delete/' in current_path:
                list_url = current_path.split('/delete/')[0] + '/'
            else:
                list_url = current_path if current_path.endswith('/') else current_path + '/'
            return redirect(list_url)
    
    form_html = render_form(
        model_class=model_class,
        instance=instance,
        framework=framework,
        **kwargs
    )
    
    context = {
        'form_html': form_html,
        'object': instance,
        'model_name': model_class._meta.verbose_name,
        'action': 'Edit' if instance else 'Create',
    }
    
    return render(request, 'cruder/form.html', context)