"""
Parametre classes for the sidebar
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import os
import param
import panel as pn
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *

class ParamColumnStats:
    def __init__(self, column_list=[DATA_NAN, STAT_MEAN, STAT_MIN, STAT_MAX], title='Statistic Columns'):
        self.columns = pn.widgets.MultiChoice(name='Statistic Columns', value=column_list, options=list(stat_dtype_dict.keys()), 
                                     sizing_mode='stretch_width', search_option_limit=25, description='Select statistics to display in table.')
        self.title = title
    
    def get_columns(self):
        return  self.columns.value
    
    def get_widgets(self):
        return self.columns
    
    def get_sidebar(self):    
        return pn.Card(self.columns, title=self.title, sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  

class ParamColumns:
    def __init__(self, column_list=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], title='Columns'):
        self.columns = pn.widgets.MultiChoice(name='Columns', value=column_list, options=list(dtype_view.keys()), 
                                     sizing_mode='stretch_width', search_option_limit=25, description='Select columns to display in table.')
        self.title = title

    def get_columns(self):
        return  self.columns.value
        
    def get_sidebar(self):    
        return pn.Card(self.columns, title=self.title, sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  
    
class ParamChronology(param.Parameterized):
    num_threads = param.Integer(default=1, bounds=(1, os.cpu_count()), step=1, doc='Number of threads.')
    biweight_mean =  param.Boolean(False, doc='Biweight mean method for computing the chronology.')
    date_as_offset =  param.Boolean(True, doc='Dates are used as offsets for computing the chronology.')
    
    def get_sidebar(self):    
        return pn.Card(pn.Param(self, show_name=False), title='Chronology', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  

class ParamDetrend(param.Parameterized):
    num_threads = param.Integer(default=1, bounds=(1, 10), step=1, doc='Number of threads.')
    detrend = param.Selector(objects=ring_types, doc='Detrend method apply to the series.')
    window_size = param.Integer(default=5, bounds=(3, 15), step=2, doc='Size of the sliding window for detrending.')
    log = param.Boolean(True, doc='Perform a logarithm transformation at the end of detrending.')
            
    def __init__(self, **params):
        super(ParamDetrend,self).__init__(**params)
    
    def get_sidebar(self):
        return pn.Card(pn.Param(self, show_name=False), title='Detrend', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  

class ParamPackage(param.Parameterized):
    #show_data = param.Boolean(False, doc='Show data in selection view')
    cambium_estimation_method = param.Selector(default='Lambert', objects=['Lambert', 'log-log', 'user values'], doc='Method for cambium estimation.')
    lambert_parameters = param.Range(default=(12,23), bounds=(0, 60), step=1, doc='Lambert estimator range.')
    #pith_estimation = param.Boolean(False, doc='Draw pith estimation')
    slope_resolution = param.Integer(default=0, bounds=(0, 10), step=1, doc='Minimal GLK resolution')
            
    def __init__(self, **params):
        super(ParamPackage,self).__init__(**params)
    
    def get_sidebar(self):
        return pn.Card(pn.Param(self, show_name=False), title='Package', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  
