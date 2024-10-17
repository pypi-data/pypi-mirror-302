
import numpy as np
import pandas as pd
from pathlib import Path
import logging

import param
import panel as pn

from pyDendron.app_logger import logger, catch_bokeh_log, perror 
from pyDendron.dataset import Dataset
from pyDendron.gui_panel.sidebar import ParamColumns, ParamDetrend, ParamChronology, ParamPackage, ParamColumnStats
from pyDendron.gui_panel.dataset_selector import DatasetSelector
from pyDendron.gui_panel.dataset_treeview import DatasetTreeview
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.dataset_package_builder import DatasetPackageBuilder
from pyDendron.gui_panel.dataset_package_editor import DatasetPackageEditor
from pyDendron.gui_panel.tools_panel import ToolsPanel
from pyDendron.gui_panel.tabulator import tabulator
from pyDendron.gui_panel.ploter_panel import PloterPanel
from pyDendron.gui_panel.debug_panel import DebugPanel
from pyDendron.gui_panel.crossdating_panel import CrossDatingPanel
from pyDendron.crossdating import CrossDating
from pyDendron.chronology import data2col, chronology
from pyDendron.ploter import Ploter
from pyDendron.tools.alignment import Alignment
from pyDendron.alien.io_besancon import IOBesancon
from pyDendron.alien.io_heidelberg import IOHeidelberg
from pyDendron.alien.io_rwl import IORWL
from pyDendron.alien.io_sylphe import IOSylphe
from pyDendron.alien.io_dendronIV import IODendronIV
from pyDendron.alien.io_tridas import IOTridas
#from pyDendron.alien.sylpheII import SylpheII
#from pyDendron.alien.rwl import RWL
from pyDendron.estimation import cambium_estimation
from pyDendron.detrend import detrend, slope

def get_git_version():
    import subprocess
    
    try:
        import importlib.metadata

        version = importlib.metadata.version('pyDendron')
        #perror(f"Version metadata: {version}")
        return version
    except ImportError:
        # Get the directory of the __init__.py file
        current_directory = Path(__file__).resolve().parent
        file_path = current_directory / 'version.txt'
        # Exécute la commande git pour obtenir la version (tag) la plus récente
        version = subprocess.check_output(['git', 'describe', '--tags']).strip().decode('utf-8')

        #perror(f"Version git: {version}")
        return version
    except subprocess.CalledProcessError:
            return "Number unable."
    
__version__ = get_git_version()
