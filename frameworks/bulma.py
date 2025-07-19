"""
Bulma CSS framework implementation
"""

from .base import BaseFramework


class BulmaFramework(BaseFramework):
    """Bulma CSS framework implementation"""
    
    name = "bulma"
    
    form_classes = {
        'form': '',
        'field': 'field',
        'label': 'label',
        'input': 'input',
        'textarea': 'textarea',
        'select': 'select',
        'checkbox': 'checkbox',
        'radio': 'radio',
        'submit': 'button is-primary',
        'error': 'help is-danger',
        'help_text': 'help',
    }
    
    table_classes = {
        'table': 'table is-striped is-hoverable is-fullwidth',
        'table_responsive': '',
        'thead': '',
        'tbody': '',
        'tr': '',
        'th': '',
        'td': '',
        'actions': 'has-text-right',
    }
    
    button_classes = {
        'primary': 'button is-primary',
        'secondary': 'button',
        'success': 'button is-success',
        'danger': 'button is-danger',
        'warning': 'button is-warning',
        'info': 'button is-info',
        'light': 'button is-light',
        'dark': 'button is-dark',
    }
    
    def get_form_field_html(self, field, field_type='text', errors=None, help_text=None):
        """Generate Bulma form field HTML"""
        field_name = getattr(field, 'name', field)
        field_label = getattr(field, 'label', field_name.replace('_', ' ').title())
        field_value = getattr(field, 'value', '') or ''
        required = getattr(field, 'required', False)
        
        # Handle different field types
        if field_type == 'textarea':
            input_html = f'<textarea class="{self.form_classes["textarea"]}" name="{field_name}" id="id_{field_name}" {"required" if required else ""}>{field_value}</textarea>'
        elif field_type == 'select':
            input_html = f'''
            <div class="select is-fullwidth">
                <select name="{field_name}" id="id_{field_name}" {"required" if required else ""}>
                </select>
            </div>
            '''
        elif field_type == 'checkbox':
            input_html = f'''
            <label class="checkbox">
                <input type="checkbox" name="{field_name}" id="id_{field_name}" {"checked" if field_value else ""}>
                {field_label}
            </label>
            '''
        else:
            input_html = f'<input type="{field_type}" class="{self.form_classes["input"]}" name="{field_name}" id="id_{field_name}" value="{field_value}" {"required" if required else ""}>'
        
        # Build complete field HTML for non-checkbox fields
        if field_type != 'checkbox':
            field_html = f'''
            <div class="{self.form_classes["field"]}">
                <label class="{self.form_classes["label"]}" for="id_{field_name}">{field_label}</label>
                <div class="control">
                    {input_html}
                </div>
                {f'<p class="{self.form_classes["help_text"]}">{help_text}</p>' if help_text else ''}
                {f'<p class="{self.form_classes["error"]}">{errors}</p>' if errors else ''}
            </div>
            '''
        else:
            field_html = f'''
            <div class="{self.form_classes["field"]}">
                <div class="control">
                    {input_html}
                </div>
                {f'<p class="{self.form_classes["help_text"]}">{help_text}</p>' if help_text else ''}
                {f'<p class="{self.form_classes["error"]}">{errors}</p>' if errors else ''}
            </div>
            '''
        
        return field_html