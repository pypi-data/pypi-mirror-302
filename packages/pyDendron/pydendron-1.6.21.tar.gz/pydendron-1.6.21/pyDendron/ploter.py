"""
File Name: ploter.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: plotter panel
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import numpy as np
import pandas as pd

import param
import panel as pn
from panel.viewable import Viewer

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FixedTicker, Label, Range1d, BoxAnnotation
from bokeh.palettes import Category20, Category10
from bokeh.core.enums import LegendLocation

from pyDendron.dataname import *
from pyDendron.app_logger import logger, perror

class Ploter(Viewer):
    ANATOMY = 'Anatomy'
    ANATOMY_COLOR = {HEARTWOOD: 'black', 
                     PITH: 'blue', 
                     SAPWOOD:'red', 
                     CAMBIUM:'red',
                     BARK: 'red'}


    width = param.Integer(default=1000, bounds=(50, 4000), step=10)
    height = param.Integer(default=1000, bounds=(50, 4000), step=10)
    figure_title = param.String(' ')
    figure_title_font_size = param.Integer(default=14, bounds=(1, 40), step=1)

    data_type = param.Selector(default='Raw', label='Data type *', objects=['Raw', 'Log', 'Detrend'], doc='where is the data')
    color = param.Selector(default=ANATOMY, objects=['None', KEYCODE, ANATOMY], 
            doc=f'None: all black, {KEYCODE}: one color per {KEYCODE}, {ANATOMY}: color pith, sapwood... ')
    draw_type = param.Selector(default='Line', label='Draw type *', objects=['Line', 'Step', 'Spaghetti'], doc='Line draw type.') 
    group_by = param.Selector(default=None, label='Group by *', objects=[None, TAG, CATEGORY, KEYCODE, DATE_END], doc='group by')
    #draw_selection = param.Boolean(False, label='Draw selection', doc='Draw only selected series in package')
    
    x_offset_mode = param.Selector(default=DATE_BEGIN, label='X offset mode *', objects=['None', DATE_BEGIN, OFFSET], doc='Delay of the rings')
    y_offset_mode = param.Selector(default='Stack', label='Y offset mode *', objects=['Zero', 'Stack'], doc='y curve position')
    y_height = param.Selector(default='[0, max]', label='Y Height *', objects=['[0, max]', '[min, max]'], doc='height of a serie')
    y_delta = param.Number(default=0, label='Y Delta *', doc='marge between two series')
    x_range_step = param.Integer(default=25, bounds=(5, 200), step=5)
    axis_marge = param.Integer(default=35, bounds=(0, 500), step=5)
    axis_font_size = param.Integer(default=10, bounds=(1, 20), step=1)

    cambium_estimation = param.Boolean(True, label= 'Cambium estimation *', doc='Draw cambium estimation')
    show_dates = param.Boolean(True, doc='Add dates at the start and end of the serie')
    show_estimated_dates = param.Boolean(True, doc='Add estimated dates at the end of the serie')
    show_cambium_season = param.Boolean(True, doc='Add cambium season at the end of the serie')

    curve_axe = param.Selector(default='1 mm', label='Curve axe *', objects=['None', '1 mm', '0 mm', 'Mean'], doc=f'position of {KEYCODE} axe')
    anatomy = param.Selector(default='Axe', label='Anatomy *', objects=['Curve', 'Axe'], doc='color of the curve')
    
    line_width_tree = param.Number(default=0.5, bounds=(0.25, 4.0), step=0.25)
    line_width_chronology = param.Number(default=1, bounds=(0.25, 4.0), step=0.25)
    circle_radius = param.Number(default=0.5, bounds=(0.1, 5), step=0.1)

    legend = param.Selector(default=KEYCODE, label='Legend *', objects=[KEYCODE, 'Number', 'Number+' + KEYCODE, 'None'], doc=f'legend type')
    legend_location = param.Selector(default='Curve begin', label='Legend location *', objects=['None', 'Axe Y', 'Curve begin', 'Curve end']+[loc for loc in LegendLocation], doc='Legend location')
    legend_font_size = param.Integer(default=10, bounds=(1, 20), step=1)
    #grid_line_visible = param.Boolean(False, doc='Show grid line')

    border = param.Boolean(False, doc='Log transform')
    
    def __init__(self, ploter_name='ploter', **params):
        super(Ploter, self).__init__(**params)   
        self.ploter_name = ploter_name
        self.draw_data = None
        self.draw_group = None 
        self.data = None
        self.x_range, self.y_range = None, None
        self.figure_pane = pn.pane.Bokeh(height=self.height, width=self.width)
        self._layout = self.figure_pane
 
    def __panel__(self):
        return self._layout
                
    @param.depends("width", watch=True)
    def _update_width(self):
        self.figure_pane.width = self.width

    @param.depends("height", watch=True)
    def _update_height(self):
        self.figure_pane.height = self.height
    
    def get_pith_optimun(self, data_len):
        return int(data_len*0.1)
 
    def prepare_data(self, data):
        #print('prepare_data')

        self.data = data

        def init_ColumnDataSource():
            return ColumnDataSource()

        def get_x_offset(row):
            if self.x_offset_mode == 'None':
                return 0
            elif self.x_offset_mode == DATE_BEGIN:
                return row[DATE_BEGIN]
            return row[OFFSET]

        def get_y_offset(row, cum_y_offset):
            data = row[DATA_VALUES]
            v = self.y_delta
            if self.draw_type == 'Spaghetti':
                v += 50
            else:
                v += np.nanmax(data) if self.y_offset_mode == 'Stack' else 0
            cum_y_offset += v
            return v, cum_y_offset
        
        def get_values(row, info):
            values = row[DATA_VALUES]

            sapwood_offset = row[SAPWOOD]
            info[SAPWOOD] = init_ColumnDataSource()
            info[HEARTWOOD] = init_ColumnDataSource()

            
            if pd.isna(sapwood_offset) or sapwood_offset < 0:
                sapwood_offset = len(values) - 1
                info['sapwood_offset'] = sapwood_offset 
            info[HEARTWOOD].data['x'] = np.arange(0, sapwood_offset + 1) + info['x_offset']
            info[HEARTWOOD].data['w'] = values[:sapwood_offset + 1]
            info[HEARTWOOD].data['y'] = info[HEARTWOOD].data['w'] + info['y_offset'] 
            
            info['is_sapwood'] = not(pd.isna(sapwood_offset) or sapwood_offset < 0)
            info[SAPWOOD].data['x'] = np.arange(sapwood_offset, len(values)) + info['x_offset']
            info[SAPWOOD].data['w'] = values[sapwood_offset:]
            info[SAPWOOD].data['y'] = info[SAPWOOD].data['w'] + info['y_offset']
            
        def get_missing_ring(row, info):
            values = row[DATA_VALUES]
            begin = np.where(~np.isnan(values))[0][0]
            end = np.where(~np.isnan(values))[0][-1]
            
            if begin > 0:
                info[MISSING_RING_BEGIN] = init_ColumnDataSource()
                info[MISSING_RING_BEGIN].data['x'] = np.arange(0, begin) + info['x_offset']
                info[MISSING_RING_BEGIN].data['w'] = [values[begin]] * begin
                info[MISSING_RING_BEGIN].data['y'] = [values[begin] + info['y_offset']] * begin 
            if end < len(values):
                info[MISSING_RING_END] = init_ColumnDataSource()
                info[MISSING_RING_END].data['x'] = np.arange(end, len(values)) + info['x_offset']
                info[MISSING_RING_END].data['w'] = [values[end]] * (len(values) - end)
                info[MISSING_RING_END].data['y'] = [values[end] + info['y_offset']] * (len(values) - end) 
            
        def get_pith(row, info):
            values = row[DATA_VALUES] 
            x_min = info['x_offset']
            i = np.where(~np.isnan(values))[0][0]
            w = values[i]
            info[PITH] = init_ColumnDataSource()
            if pd.notna(row[PITH]) and row[PITH]:
                info[PITH].data['x'] = [info['x_offset']]
                info[PITH].data['w'] = [w]
                info[PITH].data['y'] = [get_y(info, w)]
            return x_min
                
        def get_cambium(row, info):
            info['is_cambium_estimated'] = False
            values = row[DATA_VALUES]
            x = len(values) - 1
            x_max = x + info['x_offset']

            w = values[np.where(~np.isnan(values))[0][-1]]
            info[CAMBIUM] = init_ColumnDataSource()
            info[CAMBIUM_ESTIMATED] = init_ColumnDataSource()
            info[CAMBIUM_BOUNDARIES] = init_ColumnDataSource()
            if pd.notna(row[CAMBIUM]) and row[CAMBIUM]:
                info[CAMBIUM].data['x'] = [x + info['x_offset']]
                info[CAMBIUM].data['w'] = ['NA']
                info[CAMBIUM].data['y'] = [get_y(info, w)]
            else:
                if (CAMBIUM_ESTIMATED in row) and row[[CAMBIUM_ESTIMATED, CAMBIUM_LOWER, CAMBIUM_UPPER]].notna().all():
                    info['is_cambium_estimated'] = True

                    lower, estimated, upper = row[CAMBIUM_LOWER], row[CAMBIUM_ESTIMATED], row[CAMBIUM_UPPER]
                    wo = get_y(info, w)
                    xe = estimated + info['x_offset']
                    xl = lower + info['x_offset']
                    xu = upper + info['x_offset']
                    
                    diff_h = (np.nanmax(values) - min(np.nanmin(values), 0)) / 5
                    h = 25 if diff_h > 25 else diff_h
                    h = 0.5 if h < 0.5 else h
                    #perror(f'---> {row[KEYCODE]} {diff_h} {h} {np.nanmax(values)} {np.nanmin(values)}')
                    #h = d if d < 25 else 25
                    info[CAMBIUM_BOUNDARIES].data['x'] = np.arange(xl, xu+1) 
                    info[CAMBIUM_BOUNDARIES].data['w'] = np.array(['NA']*(xu-xl+1))
                    info[CAMBIUM_BOUNDARIES].data['y'] =  np.array([get_y(info, w)]*(xu-xl+1))
                    
                    info[CAMBIUM_ESTIMATED].data['x0'] = [xu, xe, xl]
                    info[CAMBIUM_ESTIMATED].data['x1'] = [xu, xe, xl]
                    info[CAMBIUM_ESTIMATED].data['w'] = ['NA'] * 3
                    info[CAMBIUM_ESTIMATED].data['y0'] = [wo - h] * 3
                    info[CAMBIUM_ESTIMATED].data['y1'] = [wo + h] * 3
                    x_max = xu if xu > x_max else x_max
                elif (CAMBIUM_ESTIMATED in row) and row[[CAMBIUM_ESTIMATED, CAMBIUM_LOWER, CAMBIUM_UPPER]].notna().any():
                    logger.warning(f'Incomplet cambium estimation for {row[KEYCODE]}')
                    
            return x_max

        def get_bark(row, info):
            values = row[DATA_VALUES]
            x = len(values)
            w = values[np.where(~np.isnan(values))[-1]]
            info[BARK] = init_ColumnDataSource()
            if pd.notna(row[BARK]) and row[BARK]:
                info[BARK].data['x'] = [x + info['x_offset']]
                info[BARK].data['w'] = [w]
                info[BARK].data['y'] = [get_y(info, w)]
                
        def get_border(row, info):
            info['border'] = init_ColumnDataSource()
            info['border'].data['top'] = [info['y_max']]
            info['border'].data['bottom'] = [info['y_min']]
            info['border'].data['left'] = [info['x_min']]
            info['border'].data['right'] = [info['x_max']]
            
        def get_min_max(row, info):
            info['x_min'] = get_pith(row, info)
            info['x_max'] = get_cambium(row, info)
            info['w_min'] = np.nanmin(row[DATA_VALUES])
            info['w_max'] = np.nanmax(row[DATA_VALUES])
            info['w_mean'] = np.nanmean(row[DATA_VALUES])
            info['y_min'] = info['y_offset'] #info['w_min'] + info['y_offset']
            info['y_max'] = next_cum_y_offset
            info['y_mean'] = info['w_mean'] + info['y_offset']
            info['y_label'] = round(info['y_mean'], 3)    
        
        def get_text(row, i, info):
            def add_text(value, text):
                if (value is None) or pd.isna(value):
                    return text
                if text != '':
                    text += ' \u2014 '
                return text + f'{value}'
            
            info['text_begin'] = init_ColumnDataSource()
            info['text_begin'].data['x'] = [info['x_min']]
            info['text_begin'].data['y'] = [info['y_mean']]
            info['text_end'] = init_ColumnDataSource()
            info['text_end'].data['x'] = [info['x_max']]
            info['text_end'].data['y'] = [info['y_mean']]
            text_begin = ''
            text_end = ''
            
            keycode = self.get_legend(i, info[KEYCODE])
            if self.legend_location == 'Curve begin':
                text_begin = add_text(keycode, text_begin)
            elif self.legend_location == 'Curve end':
                text_end = add_text(keycode, text_end)
            if self.show_dates :
                text_begin = add_text(row[DATE_BEGIN], text_begin)
                text_end = add_text(row[DATE_END], text_end)
            if self.show_estimated_dates and info['is_cambium_estimated']:
                b = row[DATE_BEGIN]
                lower, estimated, upper = b + row[CAMBIUM_LOWER], b + row[CAMBIUM_ESTIMATED], b + row[CAMBIUM_UPPER]
                text_end += f' [{lower}, {estimated}, {upper}]'
            if self.show_cambium_season and (pd.notna(row[CAMBIUM_SEASON]) and (row[CAMBIUM_SEASON] != '')):
                text_end = add_text(f'\U0001FA93 {row[CAMBIUM_SEASON]}', text_end)
            
            info['text_begin'].data['text'] = [text_begin]
            info['text_end'].data['text'] = [text_end]
        
        def get_curve_axe(row, info):
            info['axe'] = self.curve_axe != 'None'
            if self.curve_axe == '1 mm':
                if self.data_type == 'Raw':
                    y = info['y_offset'] + 100 - info['norm_min']
                elif self.data_type == 'Log':
                    y = info['y_offset'] + np.log(100) - info['norm_min']
                else:
                    logger.warning('Curve axe 1 mm not available in Detrend mode, set to 0 mm')
                    y = info['y_offset'] - info['norm_min']
            elif self.curve_axe == '0 mm':
                y = info['y_offset'] - info['norm_min']
            elif self.curve_axe == 'Mean':
                y = info['y_offset'] + np.nanmean(row[DATA_VALUES])
            if info['axe']:
                info[f'axe_{HEARTWOOD}'] = init_ColumnDataSource()
                info[f'axe_{HEARTWOOD}'].data['y'] = [y]
                info[f'axe_{SAPWOOD}'] = init_ColumnDataSource()
                info[f'axe_{SAPWOOD}'].data['y'] = [y]
        
        def get_curve_axe_value(row, info):
            if info['axe']:
                info[f'axe_{HEARTWOOD}'].data['x0'] = [info[HEARTWOOD].data['x'][0]]
                info[f'axe_{HEARTWOOD}'].data['x1'] = [info[HEARTWOOD].data['x'][-1]]
                info[f'axe_{SAPWOOD}'].data['x0'] = [info[SAPWOOD].data['x'][0]]
                info[f'axe_{SAPWOOD}'].data['x1'] = [info[SAPWOOD].data['x'][-1]]
            
        def get_y(info, dy):
            if self.anatomy == 'Axe' and info['axe']:
                return info[f'axe_{HEARTWOOD}'].data['y'][0]
            return dy + info['y_offset']
        
        draw = {}
        dgroup = {}
        data = data.loc[data[CATEGORY].isin([CHRONOLOGY, TREE]),:]
        if self.x_offset_mode != 'None':
            if data[self.x_offset_mode].isna().any():
                logger.error(f"NA value(s) in {self.x_offset_mode} column, can't draw")
                self.draw_data = None
                return
                    
        cum_y_offset = 0
        group_by = self.group_by if self.group_by is not None else [0]*len(data)
        for group, df in data.groupby(group_by):
            grp = {}
            grp['name'] = group
            grp['y0'] = cum_y_offset
            for i, (_, row) in enumerate(reversed(list(df.iterrows()))):  
                #perror(f'\t row : {row[KEYCODE]}') 
                info = {}
                info['data'] = 'wood'
                info[CATEGORY] = row[CATEGORY]
                row[RAW] = row[DATA_VALUES]

                info['norm_min'] = 0
                if self.y_height == '[min, max]':
                    info['norm_min'] = np.nanmin(row[DATA_VALUES])
                    row[DATA_VALUES] -= info['norm_min']                 
                if self.draw_type == 'Spaghetti':
                    row[DATA_VALUES] = np.array([100] * row[DATA_LENGTH])
                info['i'] = i
                info[KEYCODE] = row[KEYCODE]
                info['x_offset'] = get_x_offset(row)
                info[DATA_LENGTH] = row[DATA_LENGTH]
                h, next_cum_y_offset = get_y_offset(row, cum_y_offset)
                #print(i, row[KEYCODE], cum_y_offset, h, next_cum_y_offset)
                info['y_offset'] = cum_y_offset
                get_curve_axe(row, info)
                get_values(row, info)
                get_bark(row, info)
                get_missing_ring(row, info)
                get_min_max(row, info)
                get_border(row, info)
                get_text(row, i, info)
                get_curve_axe_value(row, info)
                
                info['legend_group'] = group
                
                draw[info[KEYCODE]] = info
                cum_y_offset = next_cum_y_offset
            grp['y1'] = cum_y_offset
            dgroup[group] = grp

        self.draw_data = draw
        self.draw_group = dgroup 
        #print('prepare_data end')


    def clear(self):
        self.figure_pane.object = None

    @param.depends('y_delta', 'y_height', 'x_offset_mode', 'anatomy', 
                   'y_offset_mode', 'draw_type', 'cambium_estimation', 'group_by', 
                   'legend', 'legend_location', 'show_dates', 'show_estimated_dates', 
                   'show_cambium_season', 'curve_axe', watch=True)
    def prepare_and_plot_inner(self):
        self.prepare_and_plot(data=self.data)
    
    def prepare_and_plot(self, data=None):
        try:
            self._layout.loading = True
            if (data is None) or (len(data) == 0):
                self.clear()
                self._layout.loading = False
                return
            self.prepare_data(data) 
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
        self.plot()
        #print('end plot')
    
    def on_x_range_step(self):
        if (self.figure_pane.object is not None) and pd.notna(self.figure_pane.object.x_range.start):
            x_min = self.figure_pane.object.x_range.start + self.axis_marge 
            x_max = self.figure_pane.object.x_range.end - self.axis_marge + self.x_range_step
            self.figure_pane.object.xaxis[0].ticker = FixedTicker(ticks= np.arange(int(x_min), int(x_max), self.x_range_step))
            label = self.x_offset_mode if self.x_offset_mode != 'None' else f'{OFFSET}'
            self.figure_pane.object.xaxis[0].axis_label = label
        
    @param.depends('figure_title', 'figure_title_font_size', watch=True)
    def on_figure_title(self):
        if self.figure_pane.object is not None:
            self.figure_pane.object.title.text = self.figure_title
            self.figure_pane.object.title.text_font_size = str(self.figure_title_font_size) + 'px'
    
    @param.depends('axis_font_size', watch=True)
    def on_axis_font_size(self):
        if self.figure_pane.object is not None:
            self.figure_pane.object.yaxis.major_label_text_font_size = f'{self.axis_font_size}px'
            self.figure_pane.object.xaxis.major_label_text_font_size = f'{self.axis_font_size}px'
    
    @param.depends('legend_font_size', watch=True)
    def on_legend_font_size(self):
        if self.figure_pane.object is not None:
            self.figure_pane.object.legend.label_text_font_size = f'{self.legend_font_size}px'
            #print(self.figure_pane.object.legend.label_text_font_size)

    def on_legend_location(self):
        if self.figure_pane.object is not None:
            if self.legend_location not in ['None', 'Axe Y', 'Curve begin', 'Curve end']:
                #print(self.legend_location, str(self.legend_location))
                self.figure_pane.object.legend.location = self.legend_location
                
    #@param.depends('grid_line_visible', watch=True)
    #def on_grid_line_color(self):
    #    if self.figure_pane.object is not None:
    #        self.figure_pane.object.ygrid.grid_line_color = self.figure_pane.object.xgrid.grid_line_color if self.grid_line_visible else None

    def get_legend(self, i, keycode):
        if self.legend == 'Number+' + KEYCODE: 
            return f'[{i}] {keycode}'
        elif self.legend == 'Number':
            return str(i)
        elif self.legend == KEYCODE:
            return keycode
        return ''

    def on_group(self):
        if self.group_by is None:
            return
        
        x0 = self.figure_pane.object.x_range.start
        x1 = self.figure_pane.object.x_range.end
        fs = str(self.legend_font_size)+'px'
        if len(self.draw_group) <= 10:
            colors = Category10[max(len(self.draw_group), 3)]
        else:
            colors = Category20[len(self.draw_group)] if len(self.draw_group) <= 20 else Category20[20]
        boxes = []
        for idx, (grp, info) in enumerate(self.draw_group.items()):
            color = colors[idx % len(colors)]
            boxes.append(BoxAnnotation(top=info['y1'], bottom=info['y0'], left=x0, right=x1,  fill_alpha=0.1, fill_color=color, 
                                       border_radius = 5, line_width=1, line_color=color, editable = True, resizable='all', movable='both'))
            
            label = Label(x=x0, y=info['y1'], anchor="top_left", text=str(grp), editable = True, 
                  text_color='black', text_font_size=fs, text_font_style='bold italic', x_offset=10, y_offset=0)
            self.figure_pane.object.add_layout(label)
            
        self.figure_pane.object.renderers.extend(boxes)
        
    def on_legend(self):
        if self.figure_pane.object is not None:            
            y_labels = {}
            for i, (keycode, info) in enumerate(self.draw_data.items()):                 
                y_labels[info['y_label']] = self.get_legend(i, keycode)
            #print(y_labels)
            #print('-'*10)
            #print(self.legend_location)
            if self.legend_location == 'None':
                self.figure_pane.object.legend.visible = False
                self.figure_pane.object.yaxis.visible = False
            elif self.legend_location == 'Axe Y':
                self.figure_pane.object.legend.visible = False
                self.figure_pane.object.yaxis.visible = True
                self.figure_pane.object.yaxis.ticker = list(y_labels.keys())
                self.figure_pane.object.yaxis.major_label_overrides = y_labels
                #print(self.figure_pane.object.yaxis.major_label_overrides)
            elif self.legend_location.startswith('Curve'):
                self.figure_pane.object.legend.visible = False
                self.figure_pane.object.yaxis.visible = False
                self.figure_pane.object.ygrid.grid_line_color = None
            else:
                self.figure_pane.object.legend.visible = True
                self.figure_pane.object.yaxis.visible = True
                self.figure_pane.object.yaxis.ticker = list(y_labels.keys())
                self.figure_pane.object.yaxis.major_label_overrides = y_labels
                #print(self.figure_pane.object.yaxis.major_label_overrides)
                self.figure_pane.object.legend.location = self.legend_location #"top_left"
                self.figure_pane.object.legend.click_policy="mute"
                self.figure_pane.object.ygrid.grid_line_color = None
       
    def get_color(self, kind, rank):
        if self.color == self.ANATOMY:
            return self.ANATOMY_COLOR[kind]
        elif self.color == KEYCODE:
            if len(self.draw_data)  <= 10:
                return Category10[10][rank]
            else:
                return Category20[20][rank % 20]
        return 'black'
    
    def get_label_legend(self, i, info):
        return f'{i} - {info[KEYCODE]}'
    
    @param.depends( 'border', 'x_range_step', 
                   'line_width_tree', 'line_width_chronology', 'circle_radius', 'color', 'axis_marge', 'legend_font_size',
                   watch=True)
    def plot(self, x_range = None, y_range = None):   
        #logger.debug('plot')
        try:
            self._layout.loading = True
            # save x_range and y_range values for next plot (usefull for ligt ploter)
            if x_range is not None:
                self.x_range = x_range
            if y_range is not None:
                self.y_range = y_range
                
            #('ploter')
            if self.draw_data is None:
                return
            fig = figure(margin=(5), title=self.figure_title, toolbar_location="left", height=self.height, width=self.width,
                tools="pan,wheel_zoom,box_zoom,reset,hover,save,crosshair,tap,box_edit,freehand_draw", tooltips=[('(date/offset,value)', '(@x, @w)')],
                )
            
            fig.output_backend = "svg"
            radius = self.circle_radius
            line_dash = [6, 3]
            
            x = []
            for i, (keycode, info) in enumerate(self.draw_data.items()):
                line_width = self.line_width_tree if info[CATEGORY] == TREE else self.line_width_chronology
                x.append(info['x_min'])
                x.append(info['x_max'])
                fct = fig.line
                if self.draw_type == 'Step':
                    fct = fig.step
                info['ids'] = []
                fct(x='x', y='y', source=info[HEARTWOOD], line_width=line_width,  color=self.get_color(HEARTWOOD, i), legend_label=self.get_label_legend(i, info))
                fct(x='x', y='y', source=info[SAPWOOD], line_width=line_width,  color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                if info['is_cambium_estimated'] and self.cambium_estimation:
                    fig.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=info[CAMBIUM_ESTIMATED], line_width=line_width, color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                    fct(x='x', y='y', source=info[CAMBIUM_BOUNDARIES], line_dash=line_dash, line_width=line_width, color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                if self.border:
                    fig.quad(top='top', bottom='bottom', left='left', right='right', source=info['border'], line_color='red', alpha=0.05, line_width=1, color='red')
                if MISSING_RING_BEGIN in info:
                    fct(x='x', y='y', source=info[MISSING_RING_BEGIN], line_dash=line_dash, line_width=line_width, color=self.get_color(HEARTWOOD, i), legend_label=self.get_label_legend(i, info))
                if MISSING_RING_END in info:
                    c = self.get_color(SAPWOOD, i) if info['is_sapwood'] else self.get_color(HEARTWOOD, i)
                    fct(x='x', y='y', source=info[MISSING_RING_END], line_dash=line_dash, line_width=line_width, color=c, legend_label=self.get_label_legend(i, info)) 
                    
                fig.circle(x='x', y='y', source=info[PITH], radius=radius, color=self.get_color(PITH, i), legend_label=self.get_label_legend(i, info))
                fig.circle(x='x', y='y', source=info[CAMBIUM], radius=radius, color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                fig.circle(x='x', y='y', source=info[BARK], radius=radius, color=self.get_color(BARK, i), legend_label=self.get_label_legend(i, info))
                
                if info['axe']:
                    fig.segment(x0='x0', y0='y', x1='x1', y1='y', source=info[f'axe_{HEARTWOOD}'], line_width=1, color=self.ANATOMY_COLOR[HEARTWOOD])
                    fig.segment(x0='x0', y0='y', x1='x1', y1='y', source=info[f'axe_{SAPWOOD}'], line_width=1, color=self.ANATOMY_COLOR[SAPWOOD])
                
                fs = str(self.legend_font_size)+'px'
                fig.text(x='x', y='y', text='text', source=info['text_begin'], x_offset=-5 , y_offset=0, anchor="center_right", text_font_size=fs)
                obj = fig.text(x='x', y='y', text='text', source=info['text_end'], x_offset=5 , y_offset=0, anchor="center_left", text_font_size=fs)
                   
            (x_min, x_max) = (np.min(x), np.max(x)) if self.x_range is None else self.x_range
            fig.x_range = Range1d(start=x_min - self.axis_marge, end=x_max + self.axis_marge)
            if self.y_range is not None:
                fig.y_range = Range1d(self.y_range[0], self.y_range[1])

            fig.legend.visible = False
            self.figure_pane.object = fig
            self.on_x_range_step()
            self.on_legend()
            self.on_group()
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False

