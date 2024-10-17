"""
Package 
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import pandas as pd
import param
import numpy as np
import panel as pn
import copy
from panel.viewable import Viewer
from bokeh.models.widgets.tables import NumberEditor

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, array2html,
                                           _cell_formatters, _hidden_columns, _get_selection, _cell_transform)

class DatasetPackage(Viewer): 
    notify_package_change = param.Event()
          
    def __init__(self, dataset, param_column, param_package, param_detrend=None, param_chronology=None, editable=False, orderable=False, **params):
        super(DatasetPackage, self).__init__(**params)   
        self._dt_data = pd.DataFrame(columns=list(dtype_package.keys()))
        self._data = pd.DataFrame(columns=list(dtype_package.keys()))
        self.dt_param = {}
        self.editable = editable
        self.accept_notification = True
        self.orderable = orderable
        self.bt_size = 100
        
        self.param_package = param_package
        #self.param_package.param.watch(self.sync_show_data,  ['show_data'], onlychanged=True)

        self.param_detrend = param_detrend
        if self.param_detrend is not None:
            self.param_detrend.param.watch(self._sync_dt_data,  ['detrend', 'window_size', 'log'], onlychanged=True )
        
        self.param_chronology = param_chronology
        if self.param_chronology is not None:
            self.param_chronology.param.watch(self._sync_dt_data,  ['biweight_mean', 'date_as_offset'], onlychanged=True)

        self.param_package.param.watch(self.sync_data, ['cambium_estimation_method', 'lambert_parameters', 'slope_resolution'], onlychanged=True)

        self.param_column = param_column
        self.wcolumns = self.param_column.columns
        self.wcolumns.param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.dataset = dataset
        self.dataset.param.watch(self.sync_dataset,  ['notify_reload', 'notify_synchronize', 'notify_packages'], onlychanged=True)

        self.wselection = pn.widgets.Select(name='Name: '+self.name, options=[], description='Select a package.')
        self.wselection.param.watch(self.sync_data,  ['value'], onlychanged=True)

        
        edit = _cell_editors(dtype_package, False)
        if self.editable:
            edit[TAG] = {'type': 'list', 'valuesLookup': True, 'autocomplete':True, 'freetext':True, 'allowEmpty':True, }
        
        order = pn.Row()
        if self.orderable:
            #self.bt_top = pn.widgets.Button(name='Top', icon='arrows-up', button_type='primary', width=self.bt_size, description='Move the selected rows to the top')
            self.bt_up = pn.widgets.Button(name='Up', icon='arrow-up', button_type='primary', width=self.bt_size, description='Move the selected rows up')
            self.bt_down = pn.widgets.Button(name='Down', icon='arrow-down', button_type='primary', width=self.bt_size, description='Move the selected rows down')
            #self.bt_bottom = pn.widgets.Button(name='Bottom', icon='arrows-down', button_type='primary', width=self.bt_size, description='Move the selected rows to the bottom')
            order = pn.Row(self.bt_up, self.bt_down,)
            self.bt_up.on_click(self.on_move_up)
            self.bt_down.on_click(self.on_move_down)
    
        
        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=list(dtype_package.keys())),
                                    hidden_columns=_hidden_columns(dtype_view=dtype_package), 
                                    text_align=_cell_text_align(dtype_package),
                                    editors=edit, 
                                    on_edit=self.on_edit,
                                    header_filters=_header_filters(dtype_package), 
                                    formatters=_cell_formatters(dtype_package),
                                    frozen_columns=[ICON, KEYCODE], 
                                    show_index=True,
                                    pagination= 'local',
                                    page_size=100, #100000,
                                    selectable='checkbox', 
                                    sizing_mode='stretch_width',
                                    max_height=400,
                                    min_height=300,
                                    height_policy='max',
                                    row_content = self.get_row_content,
                                    #configuration  = {'movableRows':True},
                                    #description='Display package containing series, down arrow to see the data values',
                                    ) 

        self.panel_tabulator = pn.Card(self.wtabulator, margin=(5, 0), collapsed=True, 
                                       sizing_mode='stretch_width',  
                                       title='Data '+self.name, collapsible=True,
                                       )
        
        stylesheet = 'p {padding: 0px; margin: 0px;}'
        self.dt_info = pn.pane.Alert('Detrend data is empty set', margin=(0, 0, 5, 5), align=('start', 'end'), stylesheets=[stylesheet])
        
        self._layout = pn.Column(pn.Row(self.wselection, self.dt_info), self.panel_tabulator)

    #def clone(self, name=''):
    #    return DatasetPackage(self.dataset, param_column=self.param_column, param_package=self.param_package, 
    #                          param_detrend=self.param_detrend, param_chronology=self.param_chronology, name=name) 

    def on_move_up(self, event):
        """
        Handle the event when the move up button is clicked.

        Args:
            event: The event object representing the move up event.
        """
        self._layout.loading = True
        try:
            if len(self.wtabulator.filters) > 0:
                logger.warning('Move up is not allowed with filters.')
            d = _get_selection(self.wtabulator)
            #perror(f'on_move_up: get_selection {d.index}')
            #perror(f'on_move_up: selection {self.wtabulator.selection}')
            #perror(f'on_move_up: _index_mapping {self.wtabulator._index_mapping}')
            #perror(f'on_move_up: value {self.wtabulator.value.index}')
            #perror(f'on_move_up: selected_dataframe {self.wtabulator.selected_dataframe.index}')
            #perror(f'on_move_up: current_view {self.wtabulator.current_view.index}')
            #perror(f'on_move_up: _processed {self.wtabulator._processed.index}')
            _processed, _d = self.wtabulator._get_data()
            #perror(f'on_move_up: local _processed {_processed.index}')
        except Exception as inst:
            logger.error(f'on_move_up: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    def on_move_down(self, event):
        pass

    def get_package_name(self):
        """
        Returns the name of the package selected in the GUI panel.
        
        Returns:
            str: The name of the selected package.
        """
        return self.wselection.value

    def get_row_content(self, series):
        """
        Returns a view of a datavalue.

        Parameters:
        - series: The series containing the data values.

        Returns:
        - pn.Tabs: A panel containing the data values in a tabular format.

        Raises:
        - Exception: If there is an error retrieving the data values.
        """        
        try:
            #perror(f'get_row_content: {series}')
            if isinstance(series[DATA_VALUES], np.ndarray):
                lst = []
                lst.append((RAW, array2html(series[DATA_VALUES])))
                if SLOPE in series:
                    lst.append((SLOPE, array2html(series[SLOPE])))
                if self._dt_data is not None:
                #if isinstance(self._dt_data, np.ndarray):
                    dt_type = self._dt_data.at[series.name, DATA_TYPE]
                    if dt_type != RAW:
                        lst.append((dt_type, array2html(self._dt_data.at[series.name, DATA_VALUES])))
                        #if SLOPE in self._dt_data.columns:
                        #    lst.append((SLOPE+' '+dt_type, array2html(self._dt_data.at[series.name, SLOPE])))
                return pn.Tabs(*lst)
        except Exception as inst:
            return pn.pane.Markdown('Data error.')
        return pn.pane.Markdown('Data is missing.')

    def __panel__(self):
        return self._layout

    def sync_columns(self, event):
        """
        Set the hidden columns in the tabulator widget.

        Parameters:
        - event: The event object triggered by the column selector.

        Returns:
        None
        """
        #perror(f'sync_columns')
        self.wtabulator.hidden_columns = _hidden_columns(self.wcolumns.value, dtype_view=dtype_package)

    def sync_dataset(self, event):
        """
        Synchronizes the dataset with the GUI panel.

        This method updates the package selection options.

        Parameters:
            event (object): The event object triggered by the sync action.

        Returns:
            None
        """
        #perror(f'sync_dataset')
        if not self.accept_notification:
            #perror(f'sync_dataset: not accept notification')
            return
        lst = self.dataset.package_keys()
        self._data = pd.DataFrame(columns=list(dtype_package.keys()))
        self.wtabulator.value = pd.DataFrame(columns=list(dtype_package.keys()))
        self._dt_data = pd.DataFrame(columns=list(dtype_package.keys()))
        self.dt_param = {}
        self.wselection.options = ['None'] + lst
        if self.wselection.value not in self.wselection.options:
            self.wselection.value = 'None' 
        else:
            self.sync_data(event)
    
    def sync_data(self, event):
        """
        Synchronizes the data in the GUI panel with the dataset package.

        Args:
            event: The event object triggered by the synchronization action.

        Returns:
            None
        """
        if not self.accept_notification:
            return
        try:
            self._layout.loading = True
            self._data = pd.DataFrame(columns=list(dtype_package.keys()))
            package_name = self.get_package_name()
            if package_name != 'None':
                self._data = self.dataset.get_package_components(package_name, self.param_package.slope_resolution, self.param_package).reset_index()
                self._data.insert(len(self._data.columns)-1, OFFSET, self._data.pop(OFFSET))
                self._data.insert(0, ICON, self._data.apply(lambda x: category_html(x), axis=1))
                self._data.reset_index(inplace=True)
                self._data = self._data.sort_values(by=KEYCODE)
        except Exception as inst:
            self._data = pd.DataFrame(columns=list(dtype_package.keys()))
            self.wtabulator.value = _cell_transform(self._data)
        finally:
            self.wtabulator.hidden_columns = _hidden_columns(self.wcolumns.value, dtype_view=dtype_package)
            self.wtabulator.value = _cell_transform(self._data)
            self._sync_dt_data(event)
            self._layout.loading = False

    def _sync_dt_data(self, event):
        """
        Synchronizes the detrended data with the current dataset.

        This method performs the detrending operation on the dataset based on the specified parameters.
        It updates the detrended data and the detrend information accordingly.

        Args:
            event: The event triggering the synchronization.

        Returns:
            None
        """
        def get_dt_param():
            dt_param = {}
            if self.param_detrend is not None:
                dt_param[DETREND] = self.param_detrend.detrend
                dt_param[DETREND_WSIZE] = self.param_detrend.window_size
                dt_param[DETREND_LOG] = self.param_detrend.log
                dt_param[CHRONOLOGY_DATE_AS_OFFSET] = self.param_chronology.date_as_offset
                dt_param[CHRONOLOGY_BIWEIGHT_MEAN] = self.param_chronology.biweight_mean
            return dt_param
        
        try:
            #perror(f'_sync_dt_data')
            self._layout.loading = True
            tmp_data = self.get_data()
            
            tmp_dt_data = tmp_data
            idxs = tmp_data[IDX_CHILD].unique().tolist()
            if len(idxs) <= 0:
                tmp_dt_data = None
                tmp_data = None
                self.dt_info.object = 'Detrend data is empty set'
                self.dt_info.alert_type = 'warning'
            elif (self.param_detrend is  None) or (self.param_detrend.detrend == RAW):
                self.dt_info.object = 'Detrend data is raw data. '
                self.dt_info.alert_type = 'primary'
            else:
                if len(idxs) != len(tmp_data[IDX_CHILD]):
                    logger.warning(f'Duplicate series in package {self.name}')
                tmp_dt_data = tmp_data[[IDX_CHILD, IDX_PARENT, OFFSET, CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER, SLOPE]]
                res = self.dataset.detrend(idxs, self.param_detrend.detrend, self.param_detrend.window_size, 
                                                    self.param_detrend.log, self.param_chronology.date_as_offset, 
                                                    self.param_chronology.biweight_mean)      
                tmp_dt_data = tmp_dt_data.join(res, on=IDX_CHILD, how='left')
                self.dt_info.alert_type = 'info'
                c = f'Detrend data is {self.get_data_type()} '
                c += ', '.join([f'{index}: {valeur}' for index, valeur in tmp_dt_data[CATEGORY].value_counts().items()]) +'.'
                self.dt_info.object = c
                
                if tmp_dt_data[INCONSISTENT].any():
                    self.dt_info.object += ' one or more series is inconsistent.'
                    self.dt_info.alert_type='warning'
                else:
                    self.dt_info.alert_type='primary'
        except Exception as inst:
            self.dt_info.object = f'Detrend data is {RAW} data'
            logger.error(f'_sync_dt_data: {inst}', exc_info=True)
        finally:
            self.dt_param = get_dt_param()
            self._dt_data = tmp_dt_data
            self.accept_notification = False
            self.param.trigger('notify_package_change')
            self.accept_notification = True
            self._layout.loading = False
    
    def on_cambium_estimation(self, event):
        """
        Handle the event when cambium estimation is triggered.

        Args:
            event: The event object representing the cambium estimation event.

        Returns:
            None
        """
        #perror(f'on_cambium_estimation')
        try:
            self._layout.loading = True
            edit = self.wtabulator.editors
            if self.param_package.cambium_estimation_method == 'user values':
                edit[CAMBIUM_LOWER] = NumberEditor(step=1)
                edit[CAMBIUM_ESTIMATED] = NumberEditor(step=1)
                edit[CAMBIUM_UPPER] = NumberEditor(step=1)
            else:
                edit[CAMBIUM_LOWER] = None
                edit[CAMBIUM_ESTIMATED] = None
                edit[CAMBIUM_UPPER] = None
            self.wtabulator.editors = edit

            self.do_cambium_estimation(self._data)
            self.wtabulator.value = _cell_transform(self._data)
            self.param.trigger('notify_package_change')
        except Exception as inst:
            logger.error(f'sync_data: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    # def do_cambium_estimation(self, df):
    #     """
    #     Perform cambium estimation on the given dataset.

    #     Args:
    #         data (pandas.DataFrame): The dataset to perform cambium estimation on.

    #     Returns:
    #         None
    #     """
    #     #perror(f'do_cambium_estimation')
    #     if CAMBIUM_LOWER not in df.columns:
    #         df[[CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = [pd.NA, pd.NA, pd.NA]
    #     if (self.param_package.cambium_estimation_method != 'user values'):
    #         for idx, row in df.iterrows():
    #             df.loc[idx, [CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = cambium_estimation(self.param_package, row[CAMBIUM], row[BARK], row[SAPWOOD], row[DATA_VALUES])
                    
    def get_data(self):
        """
        Retrieves chronology and tree from the wtabulator and returns it.

        If the wtabulator is empty, an empty DataFrame is returned.

        Returns:
            pandas.DataFrame: The retrieved data.
        """
        return self._data

    @property
    def data(self):
        """
        Returns the selected data from the tabulator widget.

        If there is no selection, returns the entire dataset.

        Returns:
            pandas.DataFrame: The selected data.
        """
        if (self._data is None) or len(self._data) == 0:
            return None
        d = _get_selection(self.wtabulator)
        
        idxs = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = self._data.loc[idxs,:]     
        return df.loc[df[CATEGORY].isin([CHRONOLOGY, TREE]),:]

    def get_data_type(self):
        """
        Returns the detrend data as a string.

        Returns:
            str: The detrend data type as a string.
        """
        if (self.param_detrend is  None) or (self.param_detrend.detrend == RAW):
            return f'{RAW}'
        if self.param_detrend.log and (self.param_detrend.detrend != BP73):
            return f'log({self.param_detrend.detrend}), ws: {self.param_detrend.window_size}. '
        
        return f'{self.param_detrend.detrend}, ws: {self.param_detrend.window_size}. '
    
    @property
    def dt_data(self):
        """
        Returns a subset of the detrend dataset based on the selected indices.

        If no indices are selected, the entire dataset is returned.

        Returns:
            pandas.DataFrame: Subset of the dataset.
        """
        if (self._dt_data is None) or len(self._dt_data) == 0:
            return None
        #perror(f'dt_data')
        d = _get_selection(self.wtabulator)
        
        idxs = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = self._dt_data.loc[idxs,:]     
        return df.loc[df[CATEGORY].isin([CHRONOLOGY, TREE]),:]

    def _apply_log(self, array):
        x = np.log(array)
        x[np.isinf(x)] = np.nan
        return x

    @property
    def log_data(self):
        """
        Apply logarithm to the data values in the dataset.

        Returns:
            DataFrame: A copy of the dataset with logarithm applied to the data values.
        """
        
        #perror(f'log_data')
        if (self._data is None) or len(self._data) == 0:
            return None
        d = _get_selection(self.wtabulator)

        df = copy.deepcopy(self.data)
        df[DATA_VALUES] = df[DATA_VALUES].apply(self._apply_log)
        idxs = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = df.loc[idxs,:]     
        return df.loc[df[CATEGORY].isin([CHRONOLOGY, TREE]),:]

    def get_data_values_idx(self, idx):
        def get_data(df, idx):
            if df is None:
                return None
            return df.loc[df[IDX_CHILD] == idx, DATA_VALUES].iloc[0]
        
        data = get_data(self.data, idx)
        
        dt_data = get_data(self.dt_data, idx)
        log_data = get_data(self.log_data, idx) 
        
        return data, dt_data, log_data

    def on_edit(self, event):
        """
        Handle the event when a cell is edited.

        Args:
            event: The event object representing the edit event.
        """
        try:
            #perror(f'on_edit')
            self.accept_notification = False
            #perror(f'on_edit: before notification {self.accept_notification}')
            self._layout.loading = True
            col = event.column
            row = self.wtabulator.value.iloc[event.row]
            new = event.value
            idx_parent, idx_child = row[IDX_PARENT], row[IDX_CHILD]
            self._data.at[row.name, col] = new
            self._dt_data.at[row.name, col] = new
            if col == TAG:
                current_package = self.get_package_name()
                self.dataset.edit_sequence(idx_child, col, new, notify=True)
            else:
                self.param_package.cambium_estimation_method = 'user values'
        except Exception as inst:
            self.wtabulator.patch({event.column: [(event.row, event.old)]})
            logger.error(f'on_edit: {inst}', exc_info=True)
        finally:            
            self._layout.loading = False    
            self.param.trigger('notify_package_change')
            self.accept_notification = True
            #perror(f'on_edit: after notification {self.accept_notification}')
    
    def save(self):
        """
        Saves the package using the current tabulator value.

        Note: This method does not trigger the 'notify_package_change' event.

        Returns:
            None
        """
        save_package(self._data, self.get_package_name(), self.dataset)


def save_package(dataframe, package_name, dataset):
    
    def get_missing_keycodes(df, key):
        mask = df[key].isna()
        return df.loc[mask, KEYCODE].to_list(), mask

    def get_missing_values(df):
        mask = (df[CATEGORY] != SET) & df[DATA_VALUES].isna()
        return df.loc[mask, KEYCODE].to_list(), mask
    
    #perror(f'Save package {package_name}')
    if package_name == '':
        logger.warning(f'Selection name is empty')
    else:
        df = dataframe.set_index([IDX_PARENT, IDX_CHILD], verify_integrity=True)
        paires = df.index.tolist()            
        missing_date_begin, mask = get_missing_keycodes(df, DATE_BEGIN)
        if len(missing_date_begin) > 0:       
            logger.warning(f'{DATE_BEGIN} is missing for {missing_date_begin}')
        missing_offset, mask = get_missing_keycodes(df, OFFSET)
        if len(missing_offset) > 0:       
            logger.warning(f'{OFFSET} is missing for {missing_offset}')
        missing_ring_values, mask = get_missing_values(df)
        if len(missing_ring_values) > 0:       
            logger.warning(f'{DATA_VALUES} id missing for {missing_ring_values}, remove them')
            df = df.loc[~mask]
        if len(df) != 0:      
            dataset.set_package(package_name, paires)
            #dataset.dump()
            logger.info(f'Save selection')
        else:
            logger.warning(f'Selection is empty, delete package.')
            dataset.delete_package(package_name)


                
            

        



