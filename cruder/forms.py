"""
Form generation and rendering for Django models
"""

from django import forms
from django.db import models
from django.template import Template, Context
from .frameworks import get_framework


class CRUDForm(forms.ModelForm):
    """Dynamic form class for any Django model"""
    
    def __init__(self, *args, **kwargs):
        self.framework_name = kwargs.pop('framework', 'bootstrap')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = None
        fields = '__all__'


def create_model_form(model_class, framework='bootstrap', exclude_fields=None):
    """Create a dynamic form class for a given model"""
    exclude_fields = exclude_fields or ['id', 'created_at', 'updated_at']
    
    class DynamicCRUDForm(CRUDForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.framework_name = framework
            
            # Handle boolean fields with choices (like active_client)
            for field_name, field in self.fields.items():
                if field_name == 'active_client':
                    field.widget = forms.Select(choices=[
                        ('', 'Choose...'),
                        (True, 'Yes'),
                        (False, 'No'),
                    ])
            
        class Meta:
            model = model_class
            fields = '__all__'
            exclude = exclude_fields
    
    return DynamicCRUDForm


def render_form(model_class, instance=None, framework='bootstrap', exclude_fields=None, action='', method='POST'):
    """
    Render a complete form for a Django model
    
    Args:
        model_class: Django model class
        instance: Model instance for editing (None for create)
        framework: CSS framework to use ('bootstrap', etc.)
        exclude_fields: List of fields to exclude
        action: Form action URL
        method: HTTP method ('POST', 'GET')
    
    Returns:
        HTML string of the complete form
    """
    framework_class = get_framework(framework)()
    form_class = create_model_form(model_class, framework, exclude_fields)
    form = form_class(instance=instance)
    
    # Generate form fields HTML
    fields_html = []
    for field_name, field in form.fields.items():
        try:
            model_field = model_class._meta.get_field(field_name)
            field_type = get_field_type(model_field)
            
            # Get field value if instance exists
            field_value = ''
            if instance:
                try:
                    field_value = getattr(instance, field_name, '')
                    if field_value is None:
                        field_value = ''
                except:
                    field_value = ''
            
            # Create a field object with proper attributes
            field_obj = type('Field', (), {
                'name': field_name,
                'label': field.label or field_name.replace('_', ' ').title(),
                'value': field_value,
                'required': field.required,
                'help_text': getattr(model_field, 'help_text', None)
            })()
            
            field_html = framework_class.get_form_field_html(
                field_obj, 
                field_type=field_type,
                help_text=getattr(model_field, 'help_text', None)
            )
            fields_html.append(field_html)
        except Exception as e:
            # Skip problematic fields
            continue
    
    # Generate complete form HTML
    form_html = f'''
    <form action="{action}" method="{method}" class="{framework_class.form_classes["form"]}" novalidate>
        {"{% csrf_token %}" if method.upper() == 'POST' else ''}
        {"".join(fields_html)}
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="submit" class="{framework_class.button_classes["primary"]}">
                {"Update" if instance else "Create"}
            </button>
            <a href="#" class="{framework_class.button_classes["secondary"]}">Cancel</a>
        </div>
    </form>
    '''
    
    return form_html


def get_field_type(model_field):
    """Convert Django model field to HTML input type"""
    # Check for boolean field with choices (should be dropdown)
    if isinstance(model_field, models.BooleanField) and hasattr(model_field, 'choices') and model_field.choices:
        return 'select'
    
    field_mapping = {
        models.CharField: 'text',
        models.TextField: 'textarea',
        models.EmailField: 'email',
        models.URLField: 'url',
        models.IntegerField: 'number',
        models.PositiveIntegerField: 'number',
        models.FloatField: 'number',
        models.DecimalField: 'number',
        models.BooleanField: 'checkbox',
        models.DateField: 'date',
        models.DateTimeField: 'datetime-local',
        models.TimeField: 'time',
        models.FileField: 'file',
        models.ImageField: 'file',
        models.ForeignKey: 'select',
        models.ManyToManyField: 'select',
    }
    
    for field_class, input_type in field_mapping.items():
        if isinstance(model_field, field_class):
            return input_type
    
    return 'text'  # Default fallback