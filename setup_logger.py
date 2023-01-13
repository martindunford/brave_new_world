import coloredlogs, logging
from termcolor import *
import arrow

tick  = '\N{White Heavy Check Mark}'
arrowSymbol = '\N{Heavy Concave-Pointed Black Rightwards Arrow}'+' '
testtube = '\N{Test Tube}'
sun = '\N{Sun With Face}'
pencil = '\N{Lower Right Pencil}' + ' '
resting = '\N{Crescent Moon}' + ' '
clock = '\N{Mantelpiece Clock}' + ' '
cross_mark = '\N{Cross Mark}' + ' '
calculator = pencil
bstep = '\N{Black Right-Pointing Triangle}' + ' '

solidCircle = u'\u2b24 '
fail_flag = '\N{Triangular Flag On Post}'

target = '\N{Bullseye}'
warning_sign = '\N{Warning Sign}'
globe = '\N{Globe with Meridians}'
fox = '\N{Fox Face}'
toolbox = '\N{Toolbox}'

restore = '\N{Clockwise Open Circle Arrow}'
eurosign = '\N{Euro Sign}'
construction_sign = '\N{Construction Sign}'
cloud = '\N{cloud}'
coffee = '\N{Hot Beverage}'
lightning = '\N{High Voltage Sign}'
green_book = '\N{Green Book}'
cactus = '\N{Cactus}'

from rich.logging import RichHandler
from rich.table import Table as Rich_Table  #Avoid conflict with SqlAlchemy Table!
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.theme import Theme

# See: https://github.com/Textualize/rich/discussions/1799
def log_table(rtable):
    """Generate an ascii formatted presentation of a Rich table
    Eliminates any column styling
    """
    console = Console(width=150)
    with console.capture() as capture:
        console.print(rtable)
    return Text.from_ansi(capture.get())

# See
# /usr/local/lib/python3.7/site-packages/rich/default_styles.py
# also:
# https://github.com/Textualize/rich/issues/1161
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "logging.level.info": "cyan",
    "logging.level.debug1": "magenta",
    "logging.level.debug1": "white",
    "log.level":"green",
    "log.time":"white",
    "log.message":"yellow",
    "log.path":"",

})

console1 = Console(theme=custom_theme)
handler1 = RichHandler(rich_tracebacks=True,
                       show_time=True,
                       show_level=True,
                       console=console1)
handler1.setLevel(logging.INFO)
# __________________________
# Add a Custom DEBUG1 level
logging.DEBUG1 = 15  # between WARNING and INFO
logging.addLevelName(logging.DEBUG1, 'DEBUG1')

# ___________________________________
# Log to a file as well as to console
# tstamp = arrow.utcnow().format('HH_mm')
# fh = logging.FileHandler(os.path.expanduser(f'~/CoreHR_Projects/Azure/roster/Roster_Test_Suite/features/logs/testrun_{tstamp}.log'))
# fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)

logging.basicConfig(
    level="INFO",
    format='%(message)s',
    datefmt ='%H:%M:%S',
    handlers=[handler1]
)
logger = logging.getLogger("rich")
setattr(logger, 'debug1', lambda message, *args: logger._log(logging.DEBUG1, message, args))
