"""
CSS Framework support for Django Cruder
"""

from .base import BaseFramework
from .bootstrap import BootstrapFramework
from .bulma import BulmaFramework

FRAMEWORKS = {
    'bootstrap': BootstrapFramework,
    'bootstrap5': BootstrapFramework,
    'bulma': BulmaFramework,
}

def get_framework(name='bootstrap'):
    """Get framework class by name"""
    return FRAMEWORKS.get(name, BootstrapFramework)