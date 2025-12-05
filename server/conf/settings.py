r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *
from evennia.contrib.base_systems import color_markups

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "dune"

# Force 80-character width for help files and formatted output
CLIENT_DEFAULT_WIDTH = 80

# Text formatting settings
# Enable special character substitutions (%r for newlines, %t for tabs)
ENABLE_SPECIAL_CHAR_SUBSTITUTIONS = True

# Define custom substitutions (can be extended by admins)
SPECIAL_CHAR_SUBSTITUTIONS = {
    '%r%r': '\n\n',  # Paragraph break (must be processed first)
    '%r': '\n',      # Newline/carriage return
    '%t': '     ',   # Tab (5 spaces)
}
######################################################################
# Color Markup Configuration
######################################################################

"""
BASE ANSI MARKUP CONFIGURATION
See below for more specific color markup configurations.

Note that this is not the only place to set %r/%t replacements, as that needs to also be done
within each file that uses the MUX carriage return or tab style.
"""
# Enable both default pipe-based (|r, |n, |b) AND MUX (%cr, %cn, %cb) color systems
COLOR_NO_DEFAULT = False

COLOR_ANSI_EXTRA_MAP = color_markups.MUX_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = color_markups.MUX_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = color_markups.MUX_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = color_markups.MUX_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = color_markups.MUX_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = color_markups.MUX_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP

######################################################################
# Account Creation Settings (for testing)
######################################################################

# Disable account creation throttling for testing purposes
# Set to None to disable, or increase the limit for more accounts
CREATION_THROTTLE_LIMIT = None  # Disable limit (default: 2)
# CREATION_THROTTLE_TIMEOUT = 10 * 60  # 10 minutes (default)

######################################################################
# Client Display Settings
######################################################################

# Set default client dimensions for clients that don't report screen size
# These are used by evmore for pagination when the client doesn't support NAWS
CLIENT_DEFAULT_WIDTH = 78
CLIENT_DEFAULT_HEIGHT = 55  # Default to 45 lines (allows ~40 lines per page after footer)

######################################################################
# Help system settings
######################################################################

# Disable help pagination if clients report incorrect screen heights
# This will show all help text at once without pagination
# Set to True to re-enable pagination (useful for very long help files)
HELP_MORE_ENABLED = False
MAX_NR_CHARACTERS = 100
CREATION_THROTTLE_LIMIT = None  # Disable limit (default: 2)

# Note: If you re-enable HELP_MORE_ENABLED, pagination is controlled by Evennia's evmore utility
# which uses CLIENT_DEFAULT_HEIGHT when clients don't report screen size.
# If clients report incorrect screen heights (like 1-2 lines), evmore will paginate excessively.
# We've set CLIENT_DEFAULT_HEIGHT to 45 to ensure reasonable pagination when enabled.
# We've also made command docstrings more compact to reduce excessive pagination.

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
