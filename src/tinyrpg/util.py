#!/usr/bin/env python3

import datetime
import logging
from colorama import init, Fore, Back, Style
from pprint import pprint
import pdb


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Floating Point
EPSILON = 1e-6

# Date
def date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Color
init(autoreset=True)
