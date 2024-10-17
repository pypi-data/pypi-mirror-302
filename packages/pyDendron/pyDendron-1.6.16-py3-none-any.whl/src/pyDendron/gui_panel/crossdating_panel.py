"""
Crossdating tools
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import logging
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import panel as pn
import json
import param
import time
import numpy as np
import warnings

from panel.viewable import Viewer
from bokeh.io import export_svgs, export_svg
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
from pathlib import Path
from io import BytesIO

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.crossdating import CrossDating, COLS, MapValueError, r
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.run import RunThread

from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters_lookup,
                                           _cell_formatters, _hidden_columns, _get_selection,
                                             get_download_folder, unique_filename)

class CrossDatingPanel(Viewer):
    """A panel for cross-dating analysis.

    This panel provides functionality for cross-dating analysis, including filtering, visualization, and exporting of results.

    Parameters:
    - dataset (Dataset): The dataset for cross-dating analysis.
    - parameters (Parameters): The parameters for cross-dating analysis.
    - cfg_path (str): The path to the configuration file.

    Attributes:
    - inner (bool): Flag indicating whether inner cross-dating is enabled.
    - param_array (ParamArray): Parameters related to the array crossdating.
    - param_filter (ParamFilter): Parameters related to filtering of results.
    - cfg_file (str): The path to the configuration file.
    - results (None or DataFrame): The computed results of cross-dating analysis.
    - pmatrix (None or Matplotlib Figure): The matrix plot of cross-dating analysis.
    - pstem (None or Bokeh Figure): The stem plot of cross-dating analysis.
    - gplot (None or Bokeh Figure): The graph plot of cross-dating analysis.
    - dataset_package (DatasetPackage): The dataset package for cross-dating analysis.
    - master_dataset_package (DatasetPackage): The master dataset package for cross-dating analysis.
    - cross_dating (CrossDating): The cross-dating object.
    - wtabulator (Tabulator): The tabulator widget for displaying results.
    - plot (None or Plot): The plot widget for displaying the selected result.
    - wrun (Row): The row widget containing the run buttons.
    - warray (Column): The column widget containing the array-related widgets.
    - wheat_matrix (Matplotlib): The Matplotlib widget for displaying the matrix plot.
    - wstem (Bokeh): The Bokeh widget for displaying the stem plot.
    - wzstem (Bokeh): The Bokeh widget for displaying the zoomed stem plot.
    - whist (Column): The column widget for displaying the histogram plot.
    - wmap (Bokeh): The Bokeh widget for displaying the map plot.
    - wgraph (Bokeh): The Bokeh widget for displaying the graph plot.
    - tabs (Tabs): The tabs widget for switching between different views.

    Methods:
    - get_tabulator(): Returns the Tabulator widget for displaying results.
    - _sync_data(event): Synchronizes the data when the dataset package changes.
    - get_plot(row): Returns the plot widget for the selected result.

    """

    inner =  param.Boolean(True, doc='Inner crossdation')

    class ParamArray(param.Parameterized):
        table_height = param.Integer(400, bounds=(100, 1000), step=10, doc='Maximum height of the Treeview tabulator.')
        max_results = param.Integer(default=500000, allow_None=True, bounds=(100000, 5000000), step=100000, doc='Maximum number of results displayed.')
        group_by = param.Selector(default=None, objects=[None, DATE_END_ESTIMATED, SYNC, T_RANK, Z_RANK, D_RANK], doc='Group scores by column.')
        columns = param.ListSelector(default=list(set(list(CrossDating.COLS.keys()))- set([IDX, IDX_MASTER])), 
                                objects=list(CrossDating.COLS.keys()),
                                doc='Displayed crossdating columns.')
    param_array = ParamArray(name='Array')
    
    class ParamFilter(param.Parameterized):
        score = param.Selector(default=CORRELATION, objects=[CORRELATION, GLK, DIST], doc='Score applyed with threshold.')
        filter_threshold = param.Boolean(False, doc='Apply filter using score threshold.')
        threshold = param.Number(default=0, allow_None=True, bounds=(None, None), step=0.5, doc='Keep results upper the threshold.')
        filter_max_rank = param.Boolean(True, doc='Apply filter using rank value.')
        max_rank = param.Integer(default=10, allow_None=True, bounds=(1, None), step=1, doc='Keep top ranking results based on score field.')
        filter_sync = param.Boolean(False, doc=f'Apply filter on {SYNC}.')
        sync = param.Boolean(True, doc='Apply filter using rank value.')
        remove_incorrect_date = param.Boolean(False, doc="Apply a filter on dates greater than today's date for start and end dates.")
    param_filter = ParamFilter()


    def __init__(self, dataset, parameters, cfg_path, **params):
        super(CrossDatingPanel, self).__init__(**params)   
        self.cfg_file = cfg_path / Path(f'{self.__class__.__name__}.cfg.json')

        bt_size = 100
        self.results = None
        self.pmatrix = None
        self.pstem = None
        self.gplot = None
        self.row_results = None
        self.dataset_package = DatasetPackage(dataset, parameters.column, parameters.package, 
                                                      parameters.detrend, parameters.chronology, name='hyp')
        self.master_dataset_package = DatasetPackage(dataset, parameters.column, parameters.package, 
                                                      parameters.detrend, parameters.chronology, name='master')
        self.master_dataset_package._layout.visible = False

        self.dataset_package.param.watch(self._sync_data, ['notify_package_change'], onlychanged=True)
        self.master_dataset_package.param.watch(self._sync_data, ['notify_package_change'], onlychanged=True)

        self.cross_dating = self.load_cfg()

        row_dataset_view = pn.Row(self.dataset_package, pn.pane.HTML('<span> </span>'), self.master_dataset_package,
                margin=(5, 0), sizing_mode='stretch_width')

        self.bt_compute = pn.widgets.Button(name='Compute', icon='sum', button_type='primary', align=('start', 'center'), width=bt_size, description='Compute the crossdating.')
        self.bt_compute.on_click(self.on_compute)
        self.bt_stop = pn.widgets.Button(name='Stop', icon='stop', button_type='primary', align=('start', 'center'), width=bt_size, description='Stop the computation.')
        self.bt_stop.on_click(self.on_stop)
        #self.bt_compute.disabled = False
        #self.bt_stop.disabled = True

        self.progress = pn.indicators.Progress(name='Run', value=0, width=400, disabled=True, bar_color='primary')
        self.progress_info = pn.pane.HTML()
        self.cross_dating.progress.param.watch(self.on_progress, ['count'], onlychanged=True)

        self.bt_sync = pn.widgets.Button(name='Sync / Unsync', icon='swicth', button_type='primary', align=('start', 'center'), width=2*bt_size, description='Switch sync/unsync the seleted rows.')
        self.bt_sync.on_click(self.on_sync)
        
        self.bt_export = pn.widgets.FileDownload(callback=self.on_export, filename='crossdating.xlsx', embed=False, 
                                                label='Download Excel', icon='file-export', button_type='primary', 
                                                width=2*bt_size, align=('start', 'end'), description='Download the table as an Excel file.')


        self.param_array.param.watch(self.on_group_by, ['group_by'], onlychanged=True)
        self.param_array.param.watch(self.on_columns, ['columns'], onlychanged=True)
        self.param_array.param.watch(self.on_table_height, ['table_height'], onlychanged=True)

        self.param_filter.param.watch(self.on_tabs, ['score', 'filter_threshold', 'threshold', 'filter_max_rank', 'max_rank', 'filter_sync', 'sync', 'remove_incorrect_date'], onlychanged=True)
        
        self.cross_dating.param_matrix.param.watch(self.on_tabs, ['size_scale', 'font_scale',  'method', 'metric', 'sorted'], onlychanged=True)
        self.cross_dating.param_stem.param.watch(self.on_tabs, ['keycode_nrows', 'height', 'window_size'], onlychanged=True)
        self.cross_dating.param_density.param.watch(self.on_tabs, ['bullet_size', 'font_size', 'keycode_nrows'], onlychanged=True)
        self.cross_dating.param_density.param.watch(self.on_density_width, ['width'], onlychanged=True)
        self.cross_dating.param_density.param.watch(self.on_density_height, ['height'], onlychanged=True)
        self.cross_dating.param_graph.param.watch(self.on_tabs, [ 'height', 'width', 'font_size', 'line_ratio', 'bullet_ratio'], onlychanged=True)

        self.cross_dating.param_map.param.watch(self.on_tabs, ['width', 'map_provider', 'label_distance', 'alpha', 'map_type', 'map_radius', 'map_center','line_ratio', 'height', 'font_size', 'bullet_ratio'], onlychanged=True)

        self.col = self.columns()

        self.wtabulator = self.get_tabulator()
        self.run_thread = None
        #self.plot = None
        self.wrun = pn.Row(
                        self.bt_compute,
                        pn.Column(
                            self.progress_info,
                            self.progress,
                            ),
                        self.bt_stop
                    )

        self.warray = pn.Column(pn.Row(self.bt_sync, self.bt_export), 
                                self.wtabulator)
        self.wheat_matrix = pn.pane.Matplotlib()
        self.wstem = pn.pane.Bokeh()
        self.wzstem = pn.pane.Bokeh()
        self.wdensity = pn.Column()
        self.wmap = pn.pane.Bokeh()
        self.wgraph = pn.pane.Bokeh()
        
        #self.bt_svg = pn.widgets.Button(name='Save plot', icon='svg', button_type='primary', align=('start', 'end'), width=2*bt_size)
        #self.bt_svg.on_click(self.on_save_svg)

        self.tabs = pn.Tabs(('Array', self.warray),
                           ('Matrix', pn.Column('Computed only on sync *scores*. Threshold filter allowed.', self.wheat_matrix)), 
                           ('Timeline', pn.Column('Computed on all *scores*. Threshold and rank filters allowed.', self.wstem, self.wzstem, sizing_mode='stretch_width')), 
                           ('Density', pn.Column('Computed on all *scores*. Threshold and rank are disallowed.', self.wdensity)),
                           ('Map', pn.Column('Computed only on sync *scores*. Threshold filter allowed.', self.wmap)),
                           ('Graph', pn.Column('Computed only on sync *scores*. Threshold filter allowed.', self.wgraph)),
                           dynamic=False)
        self.tabs.param.watch(self.on_tabs,  ['active'], onlychanged=True)

        self._layout = pn.Column(
                row_dataset_view, 
                self.wrun,
                self.tabs,
                name=self.name,
                margin=(5, 0), sizing_mode='stretch_width')

    def on_table_height(self, event):
        self.wtabulator.max_height = event.new
        self.wtabulator.min_height = event.new

    def get_tabulator(self):
        """
        Returns a Tabulator widget populated with data.

        Returns:
            pn.widgets.Tabulator: A Tabulator widget.
        """
        dtype_columns = self.dtype_columns()

        return pn.widgets.Tabulator(pd.DataFrame(columns=self.col),
                                    hidden_columns=['index', IDX_MASTER, IDX], #_hidden_columns(dtype_view=col), 
                                    text_align=_cell_text_align(dtype_columns),
                                    editors=_cell_editors(dtype_columns, False),
                                    header_filters=_header_filters_lookup(dtype_columns),
                                    formatters=_cell_formatters(dtype_columns),
                                    pagination='remote',
                                    page_size=10000,
                                    frozen_columns=[KEYCODE, KEYCODE_MASTER],
                                    selectable='checkbox', 
                                    sizing_mode='stretch_width',
                                    layout='fit_data_fill',
                                    height_policy='max',
                                    max_height=self.param_array.table_height,
                                    min_height=self.param_array.table_height,
                                    show_index = False,
                                    row_content = self.get_plot,
                                    )
    
    def _sync_data(self, event):
        self.clean()

    def get_plot(self, row):
        """
        Generates a plot based on the given row data.

        Parameters:
            row (pandas.Series): The row data containing information for generating the plot.

        Returns:
            pn.pane.Bokeh: The generated plot as a Bokeh pane.

        Raises:
            None

        """
        def callback(event):
            nonlocal data, data_dt, data_log, data_dt_master   
            if data is not None:
                x = int(round(event.x)) 
                pos = np.searchsorted(ds.data['x'], x)
                if event.modifiers['shift']:
                    if ds.data['y'][pos] is np.nan:
                        perror('callback shift nan', event.x, event.y, event.modifiers)   
                        ds.data['x'] = np.delete(ds.data['x'], -1)
                        ds.data['y'] = np.delete(ds.data['y'], pos)
                        data = np.delete(data, pos)
                        data_dt = np.delete(data_dt, pos)
                        data_log = np.delete(data_log, pos)     
                    else:
                        perror('callback shift not nan', event.x, event.y, event.modifiers)
                else:                
                    #perror('callback', event.x, event.y, event.modifiers)      
                    if data is not None:
                        #x = int(round(event.x)) 
                        #pos = np.searchsorted(ds.data['x'], x)
                        ds.data['x'] = np.append(ds.data['x'], ds.data['x'][-1] + 1) 
                        ds.data['y'] = np.insert(ds.data['y'], pos, np.nan) 
                        data = np.insert(data, pos, np.nan) 
                        data_dt = np.insert(data_dt, pos, np.nan) 
                        data_log = np.insert(data_log, pos, np.nan) 
                        
                start_data = max(0, -offset)
                start_data_master = max(0, offset)
                l = min(len(data_dt) - start_data, len(data_dt_master) - start_data_master)
                segment = data_dt[start_data:start_data+l]
                master_segment = data_dt_master[start_data_master:start_data_master+l]
                valid_data_points = (~np.isnan(segment)) & (~np.isnan(master_segment))
                n = np.sum(valid_data_points)
                nnan =  valid_data_points.size - n
                nr, nt, ___ = r(n, segment[valid_data_points], master_segment[valid_data_points])
                wr.value = round(nr, 3)
                wt.value = round(nt, 3)
                #perror('callback', nr,nt, event.x, event.y, event.modifiers)
        
        def get_data(data_type, data, data_dt, data_log):
            if data_type == 'Raw':
                return data
            elif data_type == 'Log':
                return data_log
            else:
                return data_dt
        
        def on_data_type(event):
            if ds.data is not None:
                ds.data['y'] = get_data(event.new, data, data_dt, data_log)
                ds_master.data['y'] = get_data(event.new, data_master, data_dt_master, data_log_master)
            
        plot = None   
        ds = ColumnDataSource()
        ds_master = ColumnDataSource()
        try:
            from bokeh.events import DoubleTap
            wdata_type = pn.widgets.RadioBoxGroup(name='Data Type', value='Raw', options=['Raw', 'Log', 'Detrend'], inline=True)
            wdata_type.param.watch(on_data_type, ['value'],  onlychanged=True)
            wr = pn.widgets.StaticText(name='r', value=round(row[CORR], 3))
            wt = pn.widgets.StaticText(name='t-score', value=round(row[T_SCORE],3))
            data, data_dt, data_log = self.dataset_package.get_data_values_idx(row[IDX])
            
            dp = self.dataset_package if self.inner else self.master_dataset_package
            data_master, data_dt_master, data_log_master = dp.get_data_values_idx(row[IDX_MASTER])

            offset = row[OFFSET]

            ds.data['x'] =  np.arange(len(data)) + offset
            ds.data['y'] =  get_data(wdata_type.value, data, data_dt, data_log)

            ds_master.data['x'] = np.arange(len(data_master))
            ds_master.data['y'] = get_data(wdata_type.value, data_master, data_dt_master, data_log_master)
            
            fig = figure(margin=(5), toolbar_location="below", height=200, width=1000,
                    tools="pan,wheel_zoom,box_zoom,reset,hover,crosshair,tap,save", 
                    tooltips=[('(date/offset,value)', '(@x, @y)')],
                    sizing_mode='stretch_width')
            fig.line('x', 'y', source=ds, line_width=1, line_color=Category10[10][0], legend_label='serie')
            fig.line('x', 'y', source=ds_master, line_width=1, line_color=Category10[10][1], legend_label='master')
            fig.on_event(DoubleTap, callback)
            plot = pn.pane.Bokeh(fig, sizing_mode='stretch_width')
        except Exception:
            plot = None
        finally:
            return pn.Column(pn.Row(wdata_type, wr, wt), plot)
            
        
    def update_col(self):
        col = self.columns()
        dtype_columns = self.dtype_columns()
        self.param_array.param.columns.objects = col
        self.param_array.columns = list(set(col)- set([IDX, IDX_MASTER]))
        self.wtabulator.hidden_columns=_hidden_columns(column_list=col, dtype_view=dtype_columns) 
        self.wtabulator.text_align=_cell_text_align(dtype_columns)
        self.wtabulator.editors=_cell_editors(dtype_columns, False)
        self.wtabulator.header_filters=_header_filters_lookup(dtype_columns)
        self.wtabulator.formatters=_cell_formatters(dtype_columns)

    def on_export(self):
        try:
            if (self.wtabulator.value is None) or (len(self.wtabulator.value) <=0 ):
                logger.warning('No data')
                return     
            output = BytesIO()
            chunk_size = 1000000
            with pd.ExcelWriter(output) as writer:
                data = self.row_results if self.row_results is not None else self.wtabulator.value
                total_rows = len(data)
                num_chunks = (total_rows // chunk_size) + 1
                
                for i in range(num_chunks):
                    start_row = i * chunk_size
                    end_row = min((i + 1) * chunk_size, total_rows)
                    chunk = data.iloc[start_row:end_row]
                    sheet_name = f'crossdating_part_{i + 1}'
                    chunk.to_excel(writer, sheet_name=sheet_name, merge_cells=False, float_format="%.6f")
            
                #writer.save()
                ##data = self.wtabulator.value                
                #data.to_excel(writer, sheet_name='crossdating', merge_cells=False, float_format="%.6f")
            output.seek(0)
            return output

        except Exception as inst:
            logger.error(f'on_excel: {inst}', exc_info=True)

    def on_columns(self, event):
        #perror('on_columns', event)
        self.wtabulator.hidden_columns=_hidden_columns(column_list=self.param_array.columns, 
                                                       dtype_view=self.dtype_columns()) 

    def on_group_by(self, event):
        if self.param_array.group_by is None:
            self.wtabulator.groupby = []
        else:
            self.wtabulator.groupby = [self.param_array.group_by]

    def on_density_height(self, event):
        try:
            self._layout.loading = True
            for p in self.wdensity.objects:
                p.height = self.cross_dating.param_density.height
        except Exception as inst:
            logger.error(f'CrossDating: {inst}', exc_info=True)
            self.wdensity.objects = None
        finally:
            self._layout.loading = False

    def on_density_width(self, event):
        try:
            self._layout.loading = True
            for p in self.wdensity.objects:
                p.width = self.cross_dating.param_density.width
        except Exception as inst:
            logger.error(f'CrossDating: {inst}', exc_info=True)
            self.wdensity.objects = None
        finally:
            self._layout.loading = False

    def get_score_key(self):
        if self.param_filter.score not in self.cross_dating.method:
            logger.warning(f'score key {self.param_filter.score} not in method ({self.cross_dating.method}), score set to {self.cross_dating.method[0]}')
            self.param_filter.score = self.cross_dating.method[0]
        method = self.param_filter.score 
        if method == DIST:
            return DIST
        elif method == GLK:
            return Z_SCORE
        elif method == CORRELATION:
            return T_SCORE
        return None


    def on_tabs(self, event):
        def get_filter(threshold, rank, sync, unk_date):
            param = {}
            param['score'] = self.get_score_key()

            if self.param_filter.filter_threshold and threshold:
                param['threshold'] = self.param_filter.threshold
            if self.param_filter.filter_max_rank and rank:
                param['max_rank'] = self.param_filter.max_rank
            if self.param_filter.filter_sync and sync:
                param['sync'] = self.param_filter.sync
            if self.param_filter.remove_incorrect_date and unk_date:
                param['incorrect_date'] = self.param_filter.remove_incorrect_date
                
            return param
        
        def concat_data():
            dt_data = self.dataset_package.data
            dt_data_master = self.master_dataset_package.data 
            #perror(f'concat_data: {self.cross_dating.param_map.map_type}')
            if self.inner is None:
                return dt_data
            else:
                if (dt_data is None) and (dt_data_master is None):
                    return None
                elif self.cross_dating.param_map.map_type == 0:
                    #perror(f'concat_data: {self.cross_dating.param_map.map_type}')
                    return dt_data_master
                else:
                    with warnings.catch_warnings():
                        # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                        warnings.filterwarnings("ignore", category=FutureWarning)
                        return pd.concat([dt_data, dt_data_master ], ignore_index=True)

        try:
            self._layout.loading = True
            #perror('--> on_tabs')
            if self.tabs.active == 0: #Array
                self.wtabulator.value = pd.DataFrame(columns=self.col)
                self.row_results = self.cross_dating.concat_results(**get_filter(True, True, True, True))
                if self.row_results is None:
                    self.wtabulator.value = pd.DataFrame(columns=self.col)
                elif len(self.row_results) < self.param_array.max_results:
                    self.wtabulator.value = self.row_results
                else:
                    logging.warning(f'Too many results, the displayed array will be limited to {self.param_array.max_results/1000000}M of values.')
                    self.wtabulator.value = self.row_results.sort_values(by=self.get_score_key()).iloc[ :self.param_array.max_results]
            elif self.tabs.active == 1: #Matrix
                self.wheat_matrix.object = self.cross_dating.heat_matrix(**get_filter(True, False, False, False), 
                                            metric=self.cross_dating.param_matrix.metric, method=self.cross_dating.param_matrix.method)
            elif self.tabs.active == 2: #Time line
                self.wstem.object, self.wzstem.object = self.cross_dating.stem(**get_filter(True, True, False, False))
            elif self.tabs.active == 3: 
                rows, _ = self.cross_dating.density(score=self.get_score_key())
                self.wdensity.objects = rows
            elif self.tabs.active == 4:
                try:
                    self.wmap.object = self.cross_dating.map( **get_filter(True, True, False, False), data_dt=concat_data())
                except MapValueError as inst:
                    logger.warning(f'CrossDating: {repr(inst)}')
            elif self.tabs.active == 5: 
                self.wgraph.object = self.cross_dating.graph( **get_filter(True, True, False, False))
        except Exception as inst:
            logger.error(f'CrossDating: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=self.col)
            self.wheat_matrix.object = None
            self.wstem.object = None
            self.wdensity.objects = None
        finally:
            self._layout.loading = False

    @param.depends("inner", watch=True)
    def _update_inner(self):
        if self.inner == True :
            self.master_dataset_package._layout.visible = False
        else:
            self.master_dataset_package._layout.visible = True

    def get_sidebar(self, visible=True):
        self.p_panel = pn.Param(self.param, show_name=False)
        self.p_filter = pn.Param(self.param_filter, show_name=True)
        self.p_cross = pn.Param(self.cross_dating, show_name=False)
        self.parray = pn.Param(self.param_array, show_name=False)
        self.pmatrix = pn.Param(self.cross_dating.param_matrix, show_name=False)
        self.pstem = pn.Param(self.cross_dating.param_stem, show_name=False)
        self.phist = pn.Param(self.cross_dating.param_density, show_name=False)
        self.pmap = pn.Param(self.cross_dating.param_map, show_name=False)
        self.pgraph = pn.Param(self.cross_dating.param_graph, show_name=False)
        
        return pn.Card(self.p_panel, self.p_cross, self.p_filter, 
                       pn.Accordion(self.parray, self.pmatrix, self.pstem, self.phist, self.pmap, self.pgraph, toggle=True),
                title='Crossdating', sizing_mode='stretch_width', margin=(5, 0), collapsed=True, visible=visible)  

    def dump_cfg(self):
        with open(self.cfg_file, 'w') as fd:
            data = {
                'param' : self.param.serialize_parameters(),
                'param_filter' : self.param_filter.param.serialize_parameters(),
                'param_array' : self.param_array.param.serialize_parameters(),
                'cross_dating' : self.cross_dating.param.serialize_parameters(),
                'cross_dating.param_matrix' : self.cross_dating.param_matrix.param.serialize_parameters(),
                'cross_dating.param_stem' : self.cross_dating.param_stem.param.serialize_parameters(),
                'cross_dating.param_density' : self.cross_dating.param_density.param.serialize_parameters(),
                'cross_dating.param_map' : self.cross_dating.param_map.param.serialize_parameters(),
                'cross_dating.param_graph' : self.cross_dating.param_graph.param.serialize_parameters(),
            }
            json.dump(data, fd)

    def load_cfg(self):
        cross_dating = CrossDating()
        try:
            if Path(self.cfg_file).is_file():
                with open(self.cfg_file, 'r') as fd:
                    data = json.load(fd)
                    self.param_filter = self.ParamFilter(**self.ParamFilter.param.deserialize_parameters(data['param_filter']))
                    self.param_array = self.ParamArray(**self.ParamArray.param.deserialize_parameters(data['param_array']))
                    cross_dating = CrossDating(**CrossDating.param.deserialize_parameters(data['cross_dating']))
                    cross_dating.param_matrix = CrossDating.ParamMatrix(** CrossDating.ParamMatrix.param.deserialize_parameters(data['cross_dating.param_matrix']))
                    cross_dating.param_stem =  CrossDating.ParamStem(** CrossDating.ParamStem.param.deserialize_parameters(data['cross_dating.param_stem']))
                    cross_dating.param_density =  CrossDating.ParamDensity(** CrossDating.ParamDensity.param.deserialize_parameters(data['cross_dating.param_density']))
                    cross_dating.param_map =  CrossDating.ParamMap(** CrossDating.ParamMap.param.deserialize_parameters(data['cross_dating.param_map']))
                    cross_dating.param_graph =  CrossDating.ParamGraph(** CrossDating.ParamGraph.param.deserialize_parameters(data['cross_dating.param_graph']))
                    (json.loads(data['param']))
                    for key, value in json.loads(data['param']).items():
                        if key in self.param.params().keys():
                            if key != 'name':
                                #print(f'crossdating load_cfg: set {key} = {value}')
                                self.param.set_param(key, value)
        except Exception as inst:
            logger.warning(f'ignore cfg crossdating panel, version change.')
            logger.error(f'crossdating load_cfg: {inst}')
        finally:
            #print(cross_dating)
            return cross_dating

    def columns(self):
        return list(CrossDating.COLS.keys())

    def dtype_columns(self):
        return CrossDating.COLS
        
    def __panel__(self):
        return self._layout

    def get_selection(self) -> pd.DataFrame:
        """
        Returns the view of selectionned series. 
        """
        return _get_selection(self.wtabulator)
    
    def on_link(self, event):
        if not self.inner:
            raise ValueError('Only available for self crossdating (inner parameter must be True)')
        selections = self.get_selection()
        logger.warning('link selection is not implemented yet')
        
    def on_sync(self, event):
        selections = self.get_selection()
        df = self.wtabulator.value.copy()        
        sync = selections.loc[selections[SYNC] == 'true']
        if len(sync) > 0:
            logger.warning('Sync pairs are ignored.')
        unsync = selections.loc[selections[SYNC] == 'false']
        for (idx, idx_master), grp in unsync.groupby([IDX, IDX_MASTER]):
            if len(grp) > 1:
                logger.warning('Multipled unsync pairs are ignored.')
            else:        
                mask = (df[IDX] == idx) & (df[IDX_MASTER] == idx_master)
                df.loc[mask, SYNC] = 'false'
                df.loc[grp.index[0] , SYNC] = 'true'
                date_begin = df.loc[grp.index[0] , DATE_BEGIN_ESTIMATED]
                self.dataset_package.dataset.set_dates(idx, date_begin, warning=False)
                ascendants = self.dataset_package.dataset.get_ascendants(idx)
                if len(ascendants) > 0:
                    logger.warning('Seleted date is inconsistent with ascendants.')
                    self.dataset_package.dataset.edit_sequence(ascendants, INCONSISTENT, True)
                
                d = df.loc[grp.index[0] ].to_dict()
                #d.update(self.dt_param)
                self.dataset_package.dataset.log_crossdating(d)
                self.dataset_package.sync_data(event)
        
        self.dataset_package.dataset.notify_changes('save')
        self.wtabulator.value = df

    def on_stop(self, event):
        #perror('stoping thread', self.run_thread)
        if self.run_thread is not None:
            #perror('stop thread')
            self.run_thread.stop()
        #logger.info('on_stop')

    def clean(self):
        self.plot = None
        self.results = None
        self.wtabulator = self.get_tabulator()
        self.warray[-1] = self.wtabulator
        self.wheat_matrix.object = None
        self.wstem.object = None
        self.wzstem.object = None
        self.wdensity.object = None
        self.wmap.object = None
        self.wgraph.object = None

    def on_compute(self, event):
        if self.dataset_package.dt_data is None:
            logger.warning('No data to process.')
            return
        try:
            dt_data = self.dataset_package.dt_data
            dt_data_master = self.master_dataset_package.dt_data if not self.inner else None
            if (not self.inner) and (self.dataset_package.dt_param != self.master_dataset_package.dt_param):
                raise ValueError('master and dataset parameters are not equal')
            
            self.progress_info.object = f'<span>start running...</span>'
            self.run_thread = RunThread(run_action=self.cross_dating.run, end_action=self.on_end, args=(self.dataset_package.get_data_type(), dt_data, dt_data_master))
            self.run_thread.start()
            
        except Exception as inst:
            logger.error(f'on_compute: {inst}', exc_info=True)
            self.clean()

    def on_end(self):
        #perror('--> on_end', len(self.cross_dating.results))
        
        name = 'crossdating_' + self.dataset_package.get_package_name() 
        if not self.inner:
            name += '_' + self.master_dataset_package.get_package_name()
        self.bt_export.filename = name + '.xlsx'

        self.progress.disabled = True
        rate, info = self.cross_dating.progress.info() 
        self.progress.value = rate
        self.progress_info.object = f'<span>{info}</span>'
        self.run_thread = None
        self.on_tabs(None)        

    def on_progress(self, event):
        if self.cross_dating.progress.count == self.cross_dating.progress.max_count:
            self.progress.disabled = True
            return
        self.progress.disabled = False
        rate, info = self.cross_dating.progress.info() 
        self.progress.value = rate
        self.progress_info.object = f'<span>{info}</span>'
        