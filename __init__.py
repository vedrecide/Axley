__license__ = 'MIT'
__version__ = '0.0.1'

# Main bot file
from .bot import Axley
from .cogs.help import AxleyHelpCommand

# Cogs
from .cogs.moderation import Moderation
from .cogs.admin import Admin
from .cogs.general import General
from .cogs.help import Help
from .cogs.prefix import Prefix

from .cogs.error_handler import ErrorHandler
