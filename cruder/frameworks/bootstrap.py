"""
Bootstrap 5 framework implementation
"""

from .base import BaseFramework


class BootstrapFramework(BaseFramework):
    """Bootstrap 5 CSS framework implementation"""
    
    name = "bootstrap5"
    
    form_classes = {
        'form': 'needs-validation',
        'field': 'mb-3',
        'label': 'form-label',
        'input': 'form-control',
        'textarea': 'form-control',
        'select': 'form-select',
        'checkbox': 'form-check-input',
        'radio': 'form-check-input',
        'submit': 'btn btn-primary',
        'error': 'invalid-feedback',
        'help_text': 'form-text text-muted',
    }
    
    table_classes = {
        'table': 'table table-dark table-striped table-hover',
        'table_responsive': 'table-responsive',
        'thead': '',
        'tbody': '',
        'tr': '',
        'th': '',
        'td': '',
        'actions': 'text-end',
    }
    
    button_classes = {
        'primary': 'btn btn-primary',
        'secondary': 'btn btn-secondary',
        'success': 'btn btn-success',
        'danger': 'btn btn-danger',
        'warning': 'btn btn-warning',
        'info': 'btn btn-info',
        'light': 'btn btn-light',
        'dark': 'btn btn-dark',
    }
    
    def get_form_field_html(self, field, field_type='text', errors=None, help_text=None):
        """Generate Bootstrap form field HTML"""
        field_name = getattr(field, 'name', field)
        field_label = getattr(field, 'label', field_name.replace('_', ' ').title())
        field_value = getattr(field, 'value', '') or ''
        required = getattr(field, 'required', False)
        
        # Handle different field types
        if field_type == 'textarea':
            input_html = f'<textarea class="{self.form_classes["textarea"]}" name="{field_name}" id="id_{field_name}" {"required" if required else ""}>{field_value}</textarea>'
        elif field_type == 'select':
            # Handle boolean fields with choices (like active_client)
            if field_name == 'active_client':
                options_html = f'''
                <option value="">Choose...</option>
                <option value="True" {"selected" if str(field_value) == "True" else ""}>Yes</option>
                <option value="False" {"selected" if str(field_value) == "False" else ""}>No</option>
                '''
            else:
                options_html = '<option value="">Choose...</option>'
            
            input_html = f'''<select class="{self.form_classes["select"]}" name="{field_name}" id="id_{field_name}" {"required" if required else ""}>
                {options_html}
            </select>'''
        elif field_type == 'checkbox':
            input_html = f'''
            <div class="form-check">
                <input class="{self.form_classes["checkbox"]}" type="checkbox" name="{field_name}" id="id_{field_name}" {"checked" if field_value else ""}>
                <label class="form-check-label" for="id_{field_name}">{field_label}</label>
            </div>
            '''
        else:
            input_html = f'<input type="{field_type}" class="{self.form_classes["input"]}" name="{field_name}" id="id_{field_name}" value="{field_value}" {"required" if required else ""}>'
        
        # Build complete field HTML for non-checkbox fields
        if field_type != 'checkbox':
            field_html = f'''
            <div class="{self.form_classes["field"]}">
                <label for="id_{field_name}" class="{self.form_classes["label"]}">{field_label}</label>
                {input_html}
                {f'<div class="{self.form_classes["help_text"]}">{help_text}</div>' if help_text else ''}
                {f'<div class="{self.form_classes["error"]}">{errors}</div>' if errors else ''}
            </div>
            '''
        else:
            field_html = f'''
            <div class="{self.form_classes["field"]}">
                {input_html}
                {f'<div class="{self.form_classes["help_text"]}">{help_text}</div>' if help_text else ''}
                {f'<div class="{self.form_classes["error"]}">{errors}</div>' if errors else ''}
            </div>
            '''
        
        return field_html