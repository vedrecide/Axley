__license__ = 'MIT'
__version__ = '0.0.1'

# Main bot file
from .bot import Axley

# Cogs
from .cogs.moderation import Moderation
from .cogs.admin import Admin

from .cogs.error_handler import ErrorHandler