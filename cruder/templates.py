"""
Template rendering for list views and data tables
"""

from django.db import models
from django.core.paginator import Paginator
from .frameworks import get_framework


def render_list(model_class, queryset=None, framework='bootstrap', fields=None, 
                per_page=25, page=1, search_fields=None, search_query=None, 
                base_url=None, url_pattern=None, permissions=None, search_field=None):
    """
    Render a list/table view for a Django model
    
    Args:
        model_class: Django model class
        queryset: QuerySet to display (defaults to all objects)
        framework: CSS framework to use
        fields: List of fields to display (defaults to all)
        per_page: Number of items per page
        page: Current page number
        search_fields: List of fields to search in (OR logic)
        search_query: Search query string
        search_field: Single field to search in (deprecated, use search_fields)
    
    Returns:
        Dict with HTML and pagination info
    """
    framework_class = get_framework(framework)()
    
    # Get queryset
    if queryset is None:
        queryset = model_class.objects.all()
    
    # Handle backward compatibility for search_field
    if search_field and not search_fields:
        search_fields = [search_field]
    
    # Apply search filter with OR logic across multiple fields
    if search_fields and search_query:
        from django.db.models import Q
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(q_objects)
    
    # Get field information
    if fields is None:
        fields = [f.name for f in model_class._meta.get_fields() 
                 if not f.name.endswith('_set') and f.name not in ['id']]
    
    # Generate headers
    headers = []
    for field_name in fields:
        try:
            field = model_class._meta.get_field(field_name)
            verbose_name = getattr(field, 'verbose_name', field_name.replace('_', ' ').title())
            headers.append(verbose_name)
        except:
            headers.append(field_name.replace('_', ' ').title())
    
    headers.append('Actions')  # Add actions column
    
    # Paginate queryset
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    # Generate table rows
    rows = []
    for obj in page_obj:
        row = []
        for field_name in fields:
            try:
                value = getattr(obj, field_name)
                # Format the value based on field type
                if hasattr(value, 'strftime'):  # DateTime fields
                    value = value.strftime('%Y-%m-%d %H:%M')
                elif isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                elif value is None:
                    value = '-'
                row.append(str(value))
            except:
                row.append('-')
        
        # Add action buttons with proper URLs based on permissions
        obj_id = getattr(obj, 'pk', getattr(obj, 'id', ''))
        if base_url:
            view_url = f"{base_url}{obj_id}/"
            edit_url = f"{base_url}{obj_id}/edit/"
            delete_url = f"{base_url}{obj_id}/delete/"
        else:
            view_url = f"?pk={obj_id}&action=view"
            edit_url = f"?pk={obj_id}&action=edit"
            delete_url = f"?pk={obj_id}&action=delete"
        
        # Build action buttons based on permissions
        action_buttons = []
        
        if not permissions or permissions.get('can_read', True):
            action_buttons.append(f'<a href="{view_url}" class="{framework_class.button_classes["info"]} btn-sm">View</a>')
        
        if not permissions or permissions.get('can_update', True):
            action_buttons.append(f'<a href="{edit_url}" class="{framework_class.button_classes["warning"]} btn-sm">Edit</a>')
        
        if not permissions or permissions.get('can_delete', True):
            action_buttons.append(f'<a href="{delete_url}" class="{framework_class.button_classes["danger"]} btn-sm">Delete</a>')
        
        actions_html = f'''
        <div class="btn-group btn-group-sm" role="group">
            {"".join(action_buttons)}
        </div>
        ''' if action_buttons else '<span class="text-muted">No actions available</span>'
        row.append(actions_html)
        rows.append(row)
    
    # Generate table HTML
    table_html = framework_class.get_table_html(headers, rows)
    
    # Wrap table in responsive container
    responsive_table = f'''
    <div class="{framework_class.table_classes["table_responsive"]}">
        {table_html}
    </div>
    '''
    
    # Generate pagination HTML
    pagination_html = generate_pagination_html(page_obj, framework_class)
    
    # Generate search form HTML
    search_html = generate_search_html(search_fields, search_query, framework_class)
    
    # Generate complete list view HTML
    if base_url:
        create_url = f"{base_url}create/"
    else:
        create_url = "?action=create"
    
    # Add New button based on permissions
    add_button = ''
    if not permissions or permissions.get('can_create', True):
        add_button = f'<a href="{create_url}" class="{framework_class.button_classes["primary"]}">Add New</a>'
        
    complete_html = f'''
    <div class="crud-list-view">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>{model_class._meta.verbose_name_plural.title()}</h2>
            {add_button}
        </div>
        
        {search_html}
        
        <div class="mb-3">
            <small class="text-muted">
                Showing {page_obj.start_index()}-{page_obj.end_index()} of {paginator.count} items
            </small>
        </div>
        
        {responsive_table}
        
        {pagination_html}
    </div>
    '''
    
    return {
        'html': complete_html,
        'page_obj': page_obj,
        'paginator': paginator,
        'total_count': paginator.count,
    }


def generate_pagination_html(page_obj, framework_class):
    """Generate pagination HTML"""
    if not page_obj.has_other_pages():
        return ''
    
    pagination_html = '''
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
    '''
    
    # Previous page
    if page_obj.has_previous():
        pagination_html += f'''
            <li class="page-item">
                <a class="page-link" href="?page={page_obj.previous_page_number()}">Previous</a>
            </li>
        '''
    else:
        pagination_html += '<li class="page-item disabled"><span class="page-link">Previous</span></li>'
    
    # Page numbers
    for num in page_obj.paginator.page_range:
        if num == page_obj.number:
            pagination_html += f'<li class="page-item active"><span class="page-link">{num}</span></li>'
        else:
            pagination_html += f'<li class="page-item"><a class="page-link" href="?page={num}">{num}</a></li>'
    
    # Next page
    if page_obj.has_next():
        pagination_html += f'''
            <li class="page-item">
                <a class="page-link" href="?page={page_obj.next_page_number()}">Next</a>
            </li>
        '''
    else:
        pagination_html += '<li class="page-item disabled"><span class="page-link">Next</span></li>'
    
    pagination_html += '''
        </ul>
    </nav>
    '''
    
    return pagination_html


def generate_search_html(search_fields, search_query, framework_class):
    """Generate search form HTML"""
    if not search_fields:
        return ''
    
    # Create user-friendly placeholder text
    if len(search_fields) == 1:
        placeholder = f"Search {search_fields[0]}..."
    elif len(search_fields) <= 3:
        placeholder = f"Search {', '.join(search_fields)}..."
    else:
        placeholder = f"Search {', '.join(search_fields[:2])}, and {len(search_fields)-2} more..."
    
    return f'''
    <div class="row mb-3">
        <div class="col-md-6">
            <form method="get" class="d-flex">
                <input type="text" name="search" class="{framework_class.form_classes["input"]} me-2" 
                       placeholder="{placeholder}" value="{search_query or ''}">
                <button type="submit" class="{framework_class.button_classes["primary"]}">Search</button>
            </form>
        </div>
    </div>
    '''