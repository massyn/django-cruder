"""
Base framework class for CSS framework support
"""

class BaseFramework:
    """Base class for CSS framework implementations"""
    
    name = "base"
    
    # CSS classes for different elements
    form_classes = {
        'form': '',
        'field': '',
        'label': '',
        'input': '',
        'textarea': '',
        'select': '',
        'checkbox': '',
        'radio': '',
        'submit': '',
        'error': '',
        'help_text': '',
    }
    
    table_classes = {
        'table': '',
        'table_responsive': '',
        'thead': '',
        'tbody': '',
        'tr': '',
        'th': '',
        'td': '',
        'actions': '',
    }
    
    button_classes = {
        'primary': '',
        'secondary': '',
        'success': '',
        'danger': '',
        'warning': '',
        'info': '',
        'light': '',
        'dark': '',
    }
    
    def get_form_field_html(self, field, field_type='text'):
        """Generate HTML for a form field"""
        return f'<input type="{field_type}" name="{field.name}" class="{self.form_classes["input"]}">'
    
    def get_table_html(self, headers, rows):
        """Generate HTML for a data table"""
        header_html = "".join(f'<th class="{self.table_classes["th"]}">{h}</th>' for h in headers)
        
        # Build rows HTML without nested f-strings
        rows_html = []
        for row in rows:
            cells_html = []
            for cell in row:
                cells_html.append(f'<td class="{self.table_classes["td"]}">{cell}</td>')
            row_html = f'<tr class="{self.table_classes["tr"]}">{"".join(cells_html)}</tr>'
            rows_html.append(row_html)
        
        return f'''
        <table class="{self.table_classes["table"]}">
            <thead class="{self.table_classes["thead"]}">
                <tr class="{self.table_classes["tr"]}">
                    {header_html}
                </tr>
            </thead>
            <tbody class="{self.table_classes["tbody"]}">
                {"".join(rows_html)}
            </tbody>
        </table>
        '''
    
    def get_button_html(self, text, button_type='primary', href=None):
        """Generate HTML for a button"""
        tag = 'a' if href else 'button'
        href_attr = f'href="{href}"' if href else ''
        return f'<{tag} class="{self.button_classes[button_type]}" {href_attr}>{text}</{tag}>'