"""
Tabulator tools
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import numpy as np
import pandas as pd
import panel as pn
import os
from pathlib import Path

from bokeh.models.widgets.tables import (NumberFormatter, DateFormatter, 
                                         SelectEditor, NumberEditor)

from pyDendron.dataname import *
from pyDendron.app_logger import logger, perror

def unique_filename(filename):
    filename = Path(filename)  
    directory = filename.parent  
    base, extension = filename.stem, filename.suffix  
    unique_fn = filename
    n = 1

    while unique_fn.exists():
        unique_fn = directory / f"{base}({n}){extension}"
        n += 1

    return unique_fn

def get_download_folder():
    # Pour Windows
    if os.name == 'nt':
        download_folder = Path(os.getenv('USERPROFILE')) / 'Downloads'
    # Pour macOS et Linux
    else:
        download_folder = Path.home() / 'Downloads'
    
    return download_folder

def _cell_transform(data):
    if data is None:
        return data
    data_out = pd.DataFrame()
    for col, dtype in data.dtypes.to_dict().items():
        if col not in [ICON, ICON2, IDX, IDX_CHILD, IDX_PARENT]:                    
            if str(dtype).lower().startswith('int'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('float'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('bool'):
                data_out[col] = data[col].astype('string').fillna('unk').str.lower()
            elif str(dtype).lower().startswith('string'):
                data_out[col] = data[col].fillna('')
            else:            
                data_out[col] = data[col]
        else:            
            data_out[col] = data[col]
    return data_out
            
def _cell_text_align(dtype_dict):
    aligns = {} 
    for key, dtype in dtype_dict.items():
        aligns[key] = 'left' if (dtype == 'string') or (dtype == 'object') else 'center' 
    if (ICON in aligns) or (ICON2 in aligns):
        aligns[ICON] = 'center'
    return aligns

def _cell_formatters(dtype_dict):
    formatters = {} 
    for key, dtype in dtype_dict.items():
        if dtype == 'int': formatters[key] = NumberFormatter(format='0')
        if dtype == 'Int32': formatters[key] = NumberFormatter(format='0')
        if dtype == 'float32': formatters[key] = NumberFormatter(format='0.000')
        #if dtype == 'boolean': formatters[key] = StringFormatter(nan_format = '-') #BooleanFormatter() #{'type': 'tickCross', 'allowEmpty': True, 'tickElement': "<i class='fa fa-check'></i>",'crossElement':"<i class='fa fa-times'></i>"} #BooleanFormatter(icon='check-square')
        if dtype == 'datetime64[ns]': formatters[key] = DateFormatter()
    if (ICON in dtype_dict) or (ICON2 in dtype_dict):
        formatters[ICON] = {'type': 'html'}
    return formatters

def _header_filters(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if key not in [ICON, ICON2]:                
            if dtype == 'string': filters[key] =  {'type': 'input', 'func': 'like', 'placeholder': 'Like..'}
            if dtype == 'boolean': filters[key] = {'type': 'list', 'valuesLookup': True}
            if dtype == 'Int32': filters[key] = {'type': 'number', 'func': '=='}
            if dtype == 'float32': filters[key] = {'type': 'number', 'func': '=='}
    return filters

def _header_filters_lookup(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if dtype == 'string': filters[key] =  {'type': 'list', 'func': 'in', 'valuesLookup': True, 'sort': 'asc', 'multiselect': True}
        if dtype == 'boolean': filters[key] = {'type': 'list', 'valuesLookup': True}
        if dtype == 'Int32': filters[key] = {'type': 'number', 'func': '=='}
        if dtype == 'float32': filters[key] = {'type': 'number', 'func': '>='}
    return filters

def _cell_editors(dtype_dict, edit=False):
    if edit == False:
        editors = {x:None for x in dtype_dict.keys()}
    else:
        editors = {}
        for key, dtype in dtype_dict.items():
            editors[key] = None
            if dtype == 'string': editors[key] =  {'type': 'list', 'valuesLookup': True, 'autocomplete':True, 'freetext':True, 'allowEmpty':True, }
            if dtype == 'Int32': editors[key] = NumberEditor(step=1) 
            if dtype == 'Float32': editors[key] = NumberEditor() 
            if dtype == 'boolean': editors[key] = SelectEditor(options=['true', 'false', 'unk'])
            if dtype == 'datetime64[ns]': editors[key] = 'date'
        if CATEGORY in dtype_dict:
            editors[CATEGORY] = SelectEditor(options=[SET, CHRONOLOGY, TREE])
        for col in [ICON, ICON2, IDX, IDX_CHILD, IDX_MASTER]:
            if col in dtype_dict:
                editors[col] = None            

    return editors

def tabulator(data):    
    return pn.widgets.Tabulator(data.reset_index(),
        pagination='local',
        header_filters=True, 
        sizing_mode='stretch_width',
        ) 

def _hidden_columns(column_list=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], dtype_view=dtype_view):
    return list(set(dtype_view.keys()) - set(column_list)) 

def _get_selection(wtabulator) -> pd.DataFrame:
    """
    Returns the view of selectionned rows. 
    """
    if wtabulator.pagination == 'remote':
        selection = wtabulator.value.iloc[wtabulator.selection]
    else: # 'local'
        idxs = [x for k, x in wtabulator._index_mapping.items() if k in wtabulator.selection]
        selection = wtabulator._processed.loc[idxs,:]
    #perror('-'*20)
    #perror(f'Selection: sorters {wtabulator.sorters}, filters {wtabulator.filters},  pagination {wtabulator.pagination}')
    #perror(f'Selection: {selection.index}')
    #perror('-'*20)

    return selection
    
    # is_sortered = len(wtabulator.sorters) > 0
    # d = wtabulator._index_mapping
    # is_filtered = sum([ k == v for k, v in d.items()]) != len(d)
    # is_filtered2 = len(wtabulator.filters) > 0
    
    # perror('-'*20)
    # perror(f'Selection: sorters {wtabulator.sorters}')
    # perror(f'Selection: filters {wtabulator.filters}')
    # perror(f'Selection: is_sortered: {is_sortered}, is_filtered: {is_filtered}, is_filtered2: {is_filtered2} pagination {wtabulator.pagination}')
    # idxs = [x for k, x in wtabulator._index_mapping.items() if k in wtabulator.selection]
    # selection = wtabulator._processed.loc[idxs,:]
    # perror(f'Selection: sorted / filtered{selection.index} local')
    # selection = wtabulator.value.iloc[wtabulator.selection]        
    # perror(f'Selection: sorted / not filtered{selection.index} remote')
    # selection = wtabulator.selected_dataframe
    # perror(f'Selection: not sorted / ? filtered{selection.index}')
    # perror('-'*20)


    # selection = None
    # if is_sortered:
    #     if is_filtered: # sorted and filtered
    #         perror('Selection: sorted and filtered')
    #         idxs = [x for k, x in wtabulator._index_mapping.items() if k in wtabulator.selection]
    #         selection = wtabulator._processed.loc[idxs,:]
    #     else: # sorted
    #         perror('Selection: sorted and not filtered')
    #         selection = wtabulator.value.iloc[wtabulator.selection]        
    # else: # not sorted and (filtered or not filtered)
    #     perror('Selection: not sorted and ? filtered')
    #     selection = wtabulator.selected_dataframe
    #     #if is_filtered:
    #     #    logger.warning('Selection not sorted, check restults. if results are OK, remove this warning.')

    #return selection

VALUES_PER_LINE = 20

def array2html(v):
    l = len(v)
    nl = (l + 1) // VALUES_PER_LINE + 2
    tmp = np.array([0.0] * nl * VALUES_PER_LINE, dtype=object)
    tmp[0:l] = v
    tmp[tmp == 0] = pd.NA
    tmp[len(v)] = ';'
    c = list(range(0, nl * VALUES_PER_LINE, VALUES_PER_LINE))
    return pd.DataFrame(tmp.reshape(-1, VALUES_PER_LINE).T, columns=c).T.style.format(precision=2)

