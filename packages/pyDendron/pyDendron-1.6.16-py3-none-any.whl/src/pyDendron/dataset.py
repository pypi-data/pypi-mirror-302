"""
Dataset class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

from typing import List, Tuple, Union
import warnings
import os
import copy
import pickle
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import numpy as np
import panel as pn
import param

from collections import Counter
from scipy.stats import  kurtosis, skew, entropy

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.componentsTree import ComponentsNode, ComponentsTree
from pyDendron.chronology import chronology, chronologies
from pyDendron.crossdating import CrossDating
from pyDendron.detrend import detrend, slope
from pyDendron.estimation import cambium_estimation

class Dataset(param.Parameterized):
    """
    Data storage of sequences and components. Includes also selections of pairs.
    """
    VERSION = 1
    
    notify_message = param.String(default='', doc='log change in the dataset') 
    notify_reload = param.Event()
    notify_synchronize = param.Event()
    notify_packages = param.Event()
    notification_source = param.ClassSelector(default=None, class_=object)
    #counter = param.Integer(3, doc='Node added in tree')
    save_auto =  param.Boolean(False, doc='show all components / sequences')
            
    version_control = True
    
    def __init__(self, sequences=None, components=None, username='None', cfg_tmp='./', **params):
        super(Dataset, self).__init__(**params)   
        self.username = username        
        self.filename = None
        self.cfg_tmp = cfg_tmp
        
        if (components is not None) and (sequences is not None):
            self.sequences = pd.DataFrame(sequences)
            self.components = pd.DataFrame(components)
            self.update()
        else:
            self.clean()   
        self._packages = {}
        self._freeze_components = None
        self._freeze_sequences = None
        self._log = []
        self._crossdating = pd.DataFrame()
    
    def get_log(self):
            """
            Returns the log data as a pandas DataFrame.

            Returns:
                pandas.DataFrame: The log data.
            """
            return pd.DataFrame(self._log, columns=log_dtype_dict.keys())
    
    def get_sequences_copy(self, idxs):
        """
        Returns a copy of the sequences at the specified indices.

        Parameters:
            idxs (list): A list of indices specifying the sequences to be copied.

        Returns:
            pandas.DataFrame: A copy of the sequences at the specified indices.
        """
        data = self.sequences.loc[idxs,:].copy()
        return data

    def get_components_copy(self, idx_pairs):
        """
        Returns a copy of the components DataFrame based on the given index pairs.

        Parameters:
            idx_pairs (list): A list of index pairs specifying the rows to be copied.

        Returns:
            pandas.DataFrame: A copy of the components DataFrame containing the specified rows.
        """
        data = self.components.loc[idx_pairs,:].copy()
        return data
        
    def freeze_sequences(self, idxs):
        """
        Freezes the sequences at the specified indices.

        Args:
            idxs (list): A list of indices indicating the sequences to freeze.

        Returns:
            None
        """
        #perror('freeze_sequences', idxs)
        self._freeze_sequences = self.get_sequences_copy(idxs)

    def freeze_components(self, idx_pairs):
        """
        Freezes the components specified by the given index pairs.

        Args:
            idx_pairs (list): A list of index pairs specifying the components to freeze.

        Returns:
            None
        """
        self._freeze_components = self.get_components_copy(idx_pairs)

    def log_components(self, idx_pairs, comments=''):
        """
        Compare the components specified by the given index pairs.

        Args:
            idx_pairs (list): A list of index pairs specifying the components to compare.

        Returns:
            None

        Raises:
            None
        """
        new_df = self.get_components_copy(idx_pairs)
        old_df = self._freeze_components
        log = []
        
        merge = old_df.join(new_df, lsuffix='_old', rsuffix='_new')
        for idxs, row in merge.iterrows():
            (idx_child, idx_parent) = idxs
            old, new = row[OFFSET+'_old'], row[OFFSET+'_new']
            if pd.isna(old) or pd.isna(new) or (old != new):
                log.append([datetime.now(), idx_child, idx_parent ,OFFSET, old, new, self.username, comments])
        
        self._freeze_components = None
        if len(log) > 0:
            self._log += log
            #self.notify_changes(comments)
            return True
        #print('no change in components')
        return False
        
    def log_sequences(self, idxs, comments=''):
        """
        Compare sequences between the old and new dataframes.

        Args:
            idxs (list): List of indices to compare.
            comments (str, optional): Additional comments for the comparison. Defaults to ''.

        Returns:
            dict: A dictionary containing the history of changes made in the sequences.
                The dictionary keys are tuples of (index, column, date), and the values are lists
                containing the old value, new value, user, and comments.

        Raises:
            KeyError: If the two dataframes are not aligned.

        """
        def compare(idx, old_row, new_row):
            log = []
            d = new_row[DATE_SAMPLING]
            for col in new_row.index:
                cmp = False 
                old, new = old_row[col], new_row[col]
                if col in [DATA_INFO, DATA_VALUES, DATA_WEIGHTS]:
                    cmp = not np.array_equal(np.nan_to_num(old), np.nan_to_num(new))
                elif pd.isna(old) or pd.isna(new) or (col == DATE_SAMPLING):
                    cmp = False
                else:
                    cmp = old != new
                if cmp:
                    log.append([d, idx, pd.NA ,col, old, new, self.username, comments])
            return log
        
        old_df = self._freeze_sequences
        new_df = self.get_sequences_copy(idxs)
        log = []
        if isinstance(new_df, pd.Series):
            log = compare(idxs, old_df, new_df)
        else:
            for (idx1, row1), (idx2, row2) in zip(old_df.iterrows(), new_df.iterrows()):
                if idx1 == idx2:
                    log = compare(idx1, row1, row2)
                else:
                    raise KeyError('The 2 dataframes are not aligned.')
        self._freeze_sequences = None
        #print('Log', log)
        if len(log) > 0:
            self._log += log
            #self.notify_changes(comments)
            return True
        return False
    
    def get_crossdating_log(self):
        """
        Returns the crossdating log associated with the dataset.

        Returns:
            The crossdating log.
        """
        return self._crossdating
    
    def log_crossdating(self, crossdating):
        """
        Logs the crossdating information for a dataset.

        Parameters:
        crossdating (dict): A dictionary containing the crossdating information.

        Returns:
        None
        """
        crossdating[CROSSDATING_DATE] = datetime.now()
        if len(self._crossdating) > 0:
            self._crossdating.loc[self._crossdating.index.max()+1] = crossdating
        else:
            self._crossdating = pd.DataFrame([crossdating])
        
    
    def is_empty(self):
        """
        Returns True if dataset is empty.
        """
        return len(self.sequences) == 0
        
    def notify_changes(self, message, source=None):
        """
        Set `msg` into `self.change`.
        """
        self.notify_message = message
        if self.save_auto:
            #print('*** Save auto ***')
            self.dump()
            
        self.notification_source = source if source is not None else self
        if message in ['load', 'reindex']:
            self.param.trigger('notify_reload')
        else:
            self.param.trigger('notify_synchronize')
        
    def update(self, update_tree=False):
        """
        Update index and dtype of `self.sequences` and `self.component`.
        """
        self.sequences.reset_index(inplace=True)
        self.sequences = pd.DataFrame(self.sequences, columns=sequences_index+sequences_cols)
        self.sequences.set_index(sequences_index, inplace=True, verify_integrity=True)  
        self.sequences = self.sequences.astype(sequences_dtype_dict, copy=True, errors='ignore')
        self.components.reset_index(inplace=True)
        self.components = pd.DataFrame(self.components, columns=components_index+components_cols)
        self.components.set_index(components_index, inplace=True, verify_integrity=True)  
    
    def clone(self):
        """
        Copy the dataset and returns it.
        """
        tmp = Dataset()
        tmp.sequences = self.sequences.copy()
        tmp.components = self.components.copy()
        tmp._packages = copy.deepcopy(self._packages)
        
        return tmp
    
    def _get_filename(self, filename: str = None) -> str:
        if filename is None:
            if self.filename is None:
                raise ValueError('DataSet._get_filename: empty filename')
            else:
                filename = self.filename
        else:
            self.filename = filename
        return filename

    def backup(self, filename: str):
        """
        Dump/save a dataset into `filename`.
        """
        filename = Path(filename)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{filename.stem}_{current_datetime}{filename.suffix}"
        #print('backup', filename)
        # Construct the new full file path
        directory = filename.parent 
        new_file_path = directory / 'backup' / new_filename
        os.makedirs(directory / 'backup', exist_ok=True)

        self.dump(new_file_path, save_name=False)
 
    def dump(self, filename: str = None, save_name=True):
        """
        Dump/save a dataset into `filename`.
        """
        filename = self._get_filename(filename) if save_name else filename
        #print('save', filename, self.filename)
        suffix = Path(filename).suffix
        if suffix == '.json':
            self._dump_json(filename)
        elif suffix == '.p':
            self._dump_pickle(filename)
        elif suffix == '.xlsx':
            self._dump_excel(filename)
        else:
            raise TypeError(f'DataSet.dump: unknown suffix {suffix} from {filename}')

    def _dump_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('wb') as fic:
            pickle.dump((self.VERSION, self.sequences, self.components, self._packages, self._log, self._crossdating), fic)

    def _dump_json(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('w') as fic:
            dfs_json = {
                VERSION: self.VERSION,
                SEQUENCES: json.loads(self.sequences.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                COMPONENTS: json.loads(self.components.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                SELECTIONS: self._packages,
                LOG: self._log,
                CROSSDATING: json.loads(self._crossdating.to_json(orient='table', index=True, force_ascii=False, indent=2))
            }
            json.dump(dfs_json, fic, indent=2)            

    def _dump_excel(self, filename: str):
        filename = Path(filename) 
        with pd.ExcelWriter(filename) as writer:
            self.sequences.to_excel(writer, sheet_name=SEQUENCES, merge_cells=False, float_format="%.6f")
            self.components.to_excel(writer, sheet_name=COMPONENTS, merge_cells=False, float_format="%.6f")

    def _dump_csv(self, path: str):
        base_path = Path(path)
        self.sequences.to_csv(base_path / 'sequences.csv', sep='\t', float_format="%.6f")
        self.components.to_csv(base_path / 'components.csv', sep='\t', float_format="%.6f")

    def update_version(self, version):
        """
        Update the dataset to a specific version.

        Parameters:
        - version (int): The version number to update the dataset to.

        Returns:
        - None

        Raises:
        - None
        """
        self._log = []
            
        if version == self.VERSION:
            return
        if version <= 1:
            self.sequences[COMPONENT_COUNT] = pd.NA

        logger.info(f'update dataset version {version} to {self.VERSION}')

    def load(self, filename: str=None):
        """
        Load a dataset from `filename`.
        """
        filename = self._get_filename(filename)
        ('load', filename)
        suffix = Path(filename).suffix
        version = self.VERSION
        if suffix == '.json':
            version = self._load_json(filename)
        elif suffix == '.p':
            version = self._load_pickle(filename)
        elif suffix == '.xlsx':
            self._load_excel(filename)
        else:
            raise TypeError(f'DataSet.load: unknown suffix {suffix} from {filename}')
        self.update_version(version)
        self.notify_changes('load')
        #perror('roots', self.get_roots())

    def _load_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('rb') as fic:
            data = pickle.load(fic)
            version, self.sequences, self.components, self._packages, self._log, self._crossdating = data
        return version

    def _load_json(self, filename):
        dataset_path = Path(filename) 
        with dataset_path.open('r') as fic:
            dfs_json = json.load(fic)
        version = dfs_json[VERSION]
        self.sequences = pd.DataFrame(dfs_json[SEQUENCES])
        self.components = pd.DataFrame(dfs_json[COMPONENTS])    
        self._packages = dfs_json[SELECTIONS]
        self._log = dfs_json[LOG]
        self._crossdating = pd.DataFrame(dfs_json[CROSSDATING])
        self.update()
        return version
    
    def _load_excel(self, filename: str):
        filename = Path(filename) 
        seqs = pd.read_excel(filename, sheet_name=SEQUENCES)
        comps = pd.read_excel(filename, sheet_name=COMPONENTS)
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()

    def _load_csv(self, path: str):
        base_path = Path(path)
        seqs = pd.read_csv(base_path / 'sequences.csv', sep='\t')
        comps = pd.read_csv(base_path / 'components.csv', sep='\t')
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()
        
    def new_dataset(cls):
        """
        Create a new dataset.

        Returns:
            dataset (cls.Dataset): The newly created dataset.
        """
        dataset = cls.Dataset()
        dataset.new_root()
        dataset.new_trash()
        dataset.new_workshop()
        return dataset
    
    def new_root_idx(self):
        """
        Create a new root node in the dataset.

        Returns:
            int: The index of the new root node.
        """
        return self.sequences.index.min() - 10
    
    def new_root(self, keycode: str = 'Dataset', idx = ROOT, append=True):
        """
        Create a new root node in the dataset.

        Args:
            keycode (str, optional): The keycode for the new root node. Defaults to 'Dataset'.
            idx (int, optional): The index of the new root node. Defaults to ROOT.

        Returns:
            int: The index of the new root node.

        """
        self.new(keycode, SET, idx_parent=None, idx=idx)
        if append:
            data = []
            for idx_child in set(self.get_roots()):
                if idx != idx_child:
                    data.append({IDX_PARENT: idx, IDX_CHILD: idx_child, OFFSET: pd.NA})
            df = pd.DataFrame(data).set_index(components_index, verify_integrity=True)
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                self.components = pd.concat([self.components, df])
        return idx
            
    def new_trash(self, keycode: str = 'Trash'):
        """
        Create a new trash item in the dataset.

        Parameters:
            keycode (str): The keycode for the trash item. Defaults to 'Trash'.

        Returns:
            The newly created trash item.
        """
        return self.new(idx=TRASH, idx_parent=None, keycode=keycode, category=SET)

    def new_workshop(self, keycode: str = 'Workshop' ):
        """
        Create a new workshop in the dataset.

        Parameters:
            keycode (str): The keycode for the workshop. Defaults to 'Workshop'.

        Returns:
            The newly created workshop.
        """
        return self.new(idx=WORKSHOP, idx_parent=None, keycode=keycode, category=SET)

    def new_clipboard(self, keycode: str = 'Clipboard' ):
        """
        Create a new clipboard entry in the dataset.

        Parameters:
            keycode (str): The keycode for the clipboard entry. Defaults to 'Clipboard'.

        Returns:
            The newly created clipboard entry.
        """
        return self.new(idx=CLIPBOARD, idx_parent=None, keycode=keycode, category=SET)

    def new(self, keycode: str, category: str, idx_parent: int | None, 
            idx: int | None = None, others = {}, offset : int = pd.NA) -> int:
        """
        Creat a new Sequence and component if idx_parent is not None.
        
        Arguments
        ---------
        keycode: KEYCODE of the new Sequence.
        category: CATEGORY of the new Sequence.
        idx_parent: IDX_PARENT of the new Conponent.
        idx: IDX of the Sequence.
        others: dictionary of field, value pairs to set in new Sequence.
        offset: offset to set in new Component.
        make_root : !!!! error !!! make_root and idx_parent
        
        
        Returns
        -------
        The IDX of the new Sequence.
        """
        idx = self.sequences.index.max() + 1 if idx is None else idx
        others.update({KEYCODE: keycode, CATEGORY: category})
        if CREATION_DATE not in others:
            others[CREATION_DATE] = datetime.now()
        self.sequences.loc[idx, list(others.keys())] = others
        if idx_parent is not None:
            self.components.loc[(idx_parent, idx), OFFSET] = offset
        #self.notify_changes(f'new')
        return idx                

    def _idx_list(self, idxs):
        """
        Returns a list of int created form a List[int] of from int.
        """
        if not isinstance(idxs, list):
            idxs = [idxs]
        return idxs
 
    def copy(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int], notify=True) -> str:
        """
        Copy `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(IDX_PARENT, IDX_CHILD): OFFSET}
        """
        # detect circular referencies
        couples_ = [(p, c) for p, c, o in triplets if dest_path[-1] != p]
        if len(couples_) != len(triplets):
            logger.warning('Destination and source are equal. Copy aborded.')
            return None

        couples_ = [(p, c) for p, c, o in triplets if c not in dest_path] 
        if len(couples_) != len(triplets):
            logger.warning('circular reference. Copy aborded.')
            return None

        dest_map = {(dest_path[-1], c) : o for p, c, o in triplets}
        msg = ''
        for keys, offset in dest_map.items():
            if keys in self.components.index:
                msg= str(keys[1])+', '
            else :
                self.components.loc[keys, OFFSET] = offset
        if msg != '':
            msg = 'Duplicates not copied: ' + msg 
            logger.warning(msg)

        if notify:
            self.notify_changes('copy')
                            
        return dest_map
    
    def move(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int], notify=True) -> str:
        """
        Cut `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(IDX_PARENT, IDX_CHILD): OFFSET}
        """
        dest_map = self.copy(triplets, dest_path)
        if dest_map is not None:
            keys = [(p, c) for p, c, o in triplets if p != -1]
            #logger.info(f'dataset cut keys: {keys}')
            self.components.drop(index=keys, inplace=True)
            if notify:
                self.notify_changes('cut')
        return dest_map
        
    def drop(self, triplets: List[Tuple[int, int, int]], notify=True)-> str:
        """
        drop `triplets`.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        
        Returns
        -------
        List of sequences droped
        """
        def drop_children(node, cpt_drops, drop_comp, drop_seq, deep=0):
            if cpt_drops[node.idx] >= 0:
                #perror('cpt_drops[node.idx]', cpt_drops[node.idx])
                drop_comp.append((node.parent.idx, node.idx))
                drop_seq.append(node.idx)
                for child in node.children:
                    drop_children(child, cpt_drops, drop_comp, drop_seq, deep+1)
            else:
                if deep == 0:
                    drop_comp.append((node.parent.idx, node.idx))
                logger.warning(f'Child {node.idx} / {node.keycode} has {cpt_drops[node.idx]} is dupplicated.')
        
        idx_roots = self.get_roots()
        tree_roots = self.get_descendants(idx_roots)
        cpt_roots = tree_roots.count_descendants()
        #perror('cpt_roots', cpt_roots)
        
        idx_drops = list(set([c for p, c, o in triplets]))
        tree_drops = self.get_descendants(idx_drops)
        cpt_drops = tree_drops.count_descendants()
        
        #perror('cpt_drops', cpt_drops)
        
        for key in cpt_drops.keys():
            if key in cpt_roots.keys():
                #perror('cpt_drops[key]', key, cpt_drops[key])
                #perror('cpt_roots[key]', key, cpt_roots[key])
                cpt_drops[key] = cpt_drops[key] - cpt_roots[key]

        #perror('cpt_drops', cpt_drops)
        
        drop_seq = []
        drop_comp = []
        
        for child in tree_drops.children:
            drop_children(child, cpt_drops, drop_comp, drop_seq)

    def soft_drop(self, pairs: List[Tuple[int, int]]) -> str:
        """
        soft drop of `triplets` in trash set.
        
        Arguments
        ---------
        pairs: list of tuples (IDX_PARENT, IDX_CHILD)

        Returns
        -------
        A string with duplicate sequences erased in trash.
        """
        return self.move(pairs, dest_path=[TRASH])
        
    def clean(self):
        """
        Remove data in `self.sequences` and `self.components` 
        """
        self.sequences = pd.DataFrame()
        self.components = pd.DataFrame()
        #self.notify_changes(f'clean')

    def append(self, dataset, verify_integrity=True, notify=True, merge_root=False):
        """
        Append a dataset to `self`. Warning use pd.concat with NA values.
        deprecated: use `merge` instead.
        """
        if len(self.sequences) > 0:
            tmp = dataset.clone()
            tmp.sequences.drop(index=WORKSHOP, inplace=True)
            tmp.sequences.drop(index=CLIPBOARD, inplace=True)
            tmp.sequences.drop(index=TRASH, inplace=True)
            roots = tmp.get_roots()
            #perror('get roots before drop', roots)
            if (tmp.components.index.get_level_values(IDX_PARENT) == WORKSHOP).sum() > 0:
                tmp.components.drop(index=WORKSHOP, inplace=True)
            if (tmp.components.index.get_level_values(IDX_PARENT) == CLIPBOARD).sum() > 0:
                tmp.components.drop(index=CLIPBOARD, inplace=True)
            if (tmp.components.index.get_level_values(IDX_PARENT) == TRASH).sum() > 0:
                tmp.components.drop(index=TRASH, inplace=True)
            min_idx = self.sequences.index.min() - 10
            roots = tmp.get_roots()
            #perror('get roots after drop', roots)
            index_mapping = dict(zip(roots, [i*-10+min_idx for i in range(len(roots))]))
            #print(index_mapping)
            tmp.components.rename(index=index_mapping, level=IDX_PARENT, inplace=True)
            tmp.sequences.rename(index=index_mapping, level=IDX, inplace=True)
            
            tmp.reindex(start=self.sequences.index.max() + 1)
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                #print(keep)
                self.sequences = pd.concat([self.sequences, tmp.sequences], verify_integrity=verify_integrity)
                self.components = pd.concat([self.components, tmp.components], verify_integrity=verify_integrity)
        else:
            self.sequences = dataset.sequences.copy()
            self.components = dataset.components.copy()
        if notify:
            self.notify_changes('append')
              
    def reindex(self, start=0, notify=True) -> int:
        """
        Reindex sequences from `start` to `start` + number of sequences. 
        Modifies IDX_CHILD and IXD_PARENT values in components.

        deprecated: never use.
        
        Returns
        -------
        the last IDX        
        """
        # Reindexing with contiguous index
        last = start + len(self.sequences.loc[self.sequences.index >= 0])
        new_index = list(range(start, last))
        # Create a mapping dictionary between old and new index
        index_mapping = dict(zip(self.sequences.index[self.sequences.index >= 0], new_index))
        # Use the dictionary to reindex
        tmp = self.components.rename(index=index_mapping, level=IDX_PARENT)
        self.components = tmp.rename(index=index_mapping, level=IDX_CHILD)
        self.sequences = self.sequences.rename(index=index_mapping, level=IDX)
        if notify:
            self.notify_changes('reindex')
        return last

    def drop_orphans_components(self, paires, level=IDX_PARENT):
        self.components = self.components.drop(paires)

    def get_orphans_sequences(self):
        # get sequences that are not TRASH, WORKSHOP, CLIPBOARD, ...
        # root nodes should be < 0
        seqs = set(self.sequences.index[self.sequences.index > 0].tolist())
        parent_idxs = set(self.components.index.get_level_values(IDX_PARENT).tolist())
        child_idxs = set(self.components.index.get_level_values(IDX_CHILD).tolist())
        
        orphans = seqs - (parent_idxs | child_idxs)
        
        return orphans
        
    def get_orphans_components(self, level=IDX_PARENT):
        """
        Get orphan IDX 

        Returns
        -------
        List of IDX        
        """
        idxs = set(self.components.index.get_level_values(level).unique().tolist())
        seqs = set(self.sequences.index.unique().tolist())
        filters = self.components.index.get_level_values(level).isin(list(idxs - seqs))
        return self.components.index[filters].tolist()
        
    def get_roots(self):
        """
        Get IDX_CHILD roots of components and orphan IDX sequences

        Returns
        -------
        List of IDX        
        """
        root = ~self.sequences.index.isin(self.components.index.get_level_values(IDX_CHILD))
        idxs = self.sequences.index[root].unique().tolist() 
        return idxs

    def get_leafs(self) -> List[int]:
        """
        Get IDX_CHILD leafs of components 

        Returns
        -------
        List of IDX_CHILD        
        """
        leaf = ~self.components.index.get_level_values(IDX_CHILD).isin(self.components.index.get_level_values(IDX_PARENT))
        return self.components[leaf].index.get_level_values(IDX_CHILD).unique().tolist()

    def get_sequences(self, idxs: int | List[int]) -> pd.DataFrame:
        """
        Get sequences of `idxs`

        Returns
        -------
        A pandas DataFrame.        
        """
        return self.sequences.loc[self._idx_list(idxs), :]
    
    def get_components(self, pairs : Tuple[int, int] | List[Tuple[int, int]] = None) -> pd.DataFrame:
        """
        Get the  joint view of components and sequences of `pairs` (IDX_PARENT, IDX_CHILD)
        
        Returns
        -------
        A pandas DataFrame.        
        """
        comps = self.components.loc[pairs, :] if pairs is not None else self.components
        comps = comps.join(self.sequences, on=IDX_CHILD, how='left')   
        comps = comps.join(self.sequences[KEYCODE], on=IDX_PARENT, how='left', rsuffix='Parent')
        return comps

    def package_keys(self):
        return list(self._packages.keys())
    
    def set_package(self, key: str, value: List[Tuple[int, int]]):
        self._packages[key] = value
        self.param.trigger('notify_packages')

    def get_package(self, key: str) -> List[Tuple[int, int]]:
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        return self._packages[key]

    def delete_all_packages(self):
        self._packages = {}
        self.param.trigger('notify_packages')

    def delete_package(self, key: str):
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        del self._packages[key]
        self.param.trigger('notify_packages')
    
    
    def get_package_components(self, key: str, slope_resolution=None, param_cambium_estimation=None) -> pd.DataFrame:
        """
        Return the selection (a joint view of components and sequences) stored in dictonary `self.selection`.        
        
        Arguments
        ---------
        key: name of the selection.
        
        Returns
        -------
        A pandas DataFrame.
        """        
        def do_cambium_estimation(df, param):
            if CAMBIUM_LOWER not in df.columns:
                df[[CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = [pd.NA, pd.NA, pd.NA]
            if (param.cambium_estimation_method != 'user values'):
                for idx, row in df.iterrows():
                    df.loc[idx, [CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = cambium_estimation(param, row[CAMBIUM], row[BARK], row[SAPWOOD], row[DATA_VALUES])

        df = self.get_components(self.get_package(key))
        if slope_resolution is not None:
            df[SLOPE] = df[DATA_VALUES].apply(lambda x: slope(x, slope_resolution))
            
        if param_cambium_estimation is not None:
            do_cambium_estimation(df, param_cambium_estimation)
        
        return df
 
    def get_data(self, idxs: Union[int, List[int], None] = None, category: Union[str, None] = None, 
                idx_roots=None, max_depth: Union[int, None] = None) -> pd.DataFrame:
        """
        Create a joint view of components and sequences of `idxs` descendants.        
        
        Arguments
        ---------
        idxs: an `idx` or a list of `idx`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.
        
        Returns
        -------
        A pandas DataFrame.
        """
        d = []
        if idxs is None:
            idxs = self.get_roots()
        idxs = self._idx_list(idxs)
        if idx_roots is None:
            include_parent = False
            idx_roots = [-1] * len(idxs)
        else:
            idx_roots = self._idx_list(idx_roots)
            include_parent = True
        dict_idx_roots = {idx: idx_root for idx, idx_root in zip(idxs, idx_roots)}
        
        pairs = set()
        tree = self.get_descendants(idxs, max_depth=max_depth)        
        for node, offset in tree.filter(categories=category, max_depth=max_depth).items():
            idx_parent = node.parent.idx if node.idx not in idxs else dict_idx_roots[node.idx]
            if (node.idx not in idxs) or include_parent:
                if (node.idx, idx_parent) not in pairs:
                    d.append({IDX_CHILD: node.idx, IDX_PARENT: idx_parent, OFFSET: offset})
                    pairs.add((node.idx, idx_parent))
            
        components = pd.DataFrame(d, columns=components_index+components_cols)
        components.set_index(components_index, inplace=True, verify_integrity=True)  
        return components.join(self.sequences, on=IDX_CHILD, how='left')

    def get_path_to_root(self, idx: int) -> List[int]:
        if idx is None:
            return []
        lst = [idx]
        if idx < 0:
            return lst
        idx_parents = self.components.xs(idx, level=IDX_CHILD)
        if len(idx_parents) > 0:
            if len(idx_parents) > 1:
                logger.warning(f'multiple parents for {idx} in {idx_parents.index[0]}')
            lst = self.get_path_to_root(idx_parents.index[0]) + lst
        #print('get_path_to_root:', lst)
        return lst
        
    def get_ascendants(self, idx: int, recursive=False, categories=[CHRONOLOGY, SET]):
        idx_parents = self.components.xs(idx, level=IDX_CHILD).index.to_list()
        #perror('get_ascendants', idx)
        #perror('get_ascendants', idx_parents)
        l = self.sequences.loc[idx_parents, CATEGORY].isin(categories).index.tolist() if len(idx_parents) > 0 else []

        if recursive:
            for i in l:
                l += self.get_ascendants(i, recursive, categories)
        return l

    
    def get_descendants(self, idxs: int | List[int], max_depth=None) -> ComponentsTree():
        """
        Get descendants of `idxs`.
        
        Arguments
        ---------
        idxs: an `idx` or a list of `idx`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.

        Returns
        -------
            A tree.
        """
        categories_keycodes = self.sequences.loc[:, [CATEGORY, KEYCODE]]
        data = self.components.join(categories_keycodes, on=IDX_CHILD, how='left')
        group_parents = data.groupby(IDX_PARENT)
        idx_depth = []
        #errors = []

        def iterate(parent, idx, keycode, category, offset, depth, max_depth):
            if idx in idx_depth:
                #errors.append([idx_depth[-1], idx])
                #if raise_error:
                #raise KeyError(f'DataSet.get_descendants: circular reference: {idx} in {idx_depth}')
                keycode_idx = self.sequences.at[idx, KEYCODE]
                keycode_idx_depth = [self.sequences.at[i, KEYCODE] for i in idx_depth]
                
                logger.warning(f'DataSet.get_descendants: circular reference: {idx} in {idx_depth}. Recursive loop aborded.\n {keycode_idx} in {keycode_idx_depth}')
                
                return None
            idx_depth.append(idx)
            node = ComponentsNode(parent, idx, keycode, category, offset, depth=depth)
            if (idx in group_parents.groups) and (category != TREE) and ((max_depth is None) or (depth+1 <= max_depth)):
                for (_, idx_child), row in group_parents.get_group(idx).iterrows():
                    child = iterate(node, idx_child, row[KEYCODE], row[CATEGORY], row[OFFSET], depth+1, max_depth)
                    if child is not None:
                        node.append(child)
            idx_depth.pop()
            return node
            #return node, errors
        
        tree = ComponentsTree()
        for idx in self._idx_list(idxs):
            child = iterate(tree, idx, categories_keycodes.at[idx, KEYCODE], categories_keycodes.at[idx, CATEGORY], 0, 0, max_depth)
            if child is not None:
                tree.append(child)
        return tree

    def edit_component(self, idx_parent, idx_child, value, notify=True, source=None):
        idxs = [(idx_parent, idx_child)]
        self.freeze_components(idxs)
        self.components.at[(idx_parent, idx_child), OFFSET] = np.round(value)

        self.log_components(idxs, 'edit_component')
        if notify:
            self.notify_changes('notify_synchronize', source=source)
        if self.save_auto:
            self.dump()

    def edit_sequence(self, idxs, column, value, notify=True, source=None):
        if dtype_view[column].lower().startswith('int'):
            value = np.round(value) if pd.notna(value) else pd.NA
        elif dtype_view[column].lower().startswith('float'):
            if pd.isna(value):
                value = pd.NA   
        elif dtype_view[column].lower().startswith('boolean'):
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    value = pd.NA
        
        idxs = self._idx_list(idxs)     
        if column == KEYCODE:
            if len(idxs) > 1:
                raise ValueError(f'Edit: multiple editions for {column} are not allowed')
            elif value in self.sequences[KEYCODE].values:
                raise ValueError(f'Edit: duplicate {KEYCODE} for value: {value}')
        self.freeze_sequences(idxs)
        self.sequences.loc[idxs, column] = value        
        self.log_sequences(idxs, 'edit_sequence')
        if notify:
            self.notify_changes('notify_synchronize', source=source)
        if self.save_auto:
            self.dump()

    def shift_offsets(self, parent_idx, child_idxs=None, notify=True):
        """
        Get children of `parent_idx` and shift the children offsets to 0.
        """
        data = self.get_data(parent_idx, max_depth=1)
        if child_idxs is not None:
            data = data[data.index.get_level_values(IDX_CHILD).isin(child_idxs)]
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.shift_offsets: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {OFFSET} field.')
        idxs = data.index.to_list()
        
        self.freeze_components(idxs)
        self.components.loc[idxs, OFFSET] -= data[OFFSET].min()
        self.log_components(idxs, 'shift_offsets')
        if notify:
            self.notify_changes('notify_synchronize')

    def copy_dates_to_offsets(self, parent_idx, child_idxs=None, notify=True):
        """
        Get children of `parent_idx`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_idx, max_depth=1)
        if child_idxs is not None:
            data = data[data.index.get_level_values(IDX_CHILD).isin(child_idxs)]
        if data[DATE_BEGIN].isna().any():
            logger.warning(f'one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATE_BEGIN} field.')
        idxs = data.index.to_list()
        self.freeze_components(idxs)
        self.components.loc[idxs, OFFSET] = data.loc[idxs, DATE_BEGIN]
        self.log_components(idxs, 'copy_dates_to_offsets')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_offsets_to_dates(self, parent_idx, child_idxs=None, notify=True):
        """
        Get children of `parent_idx`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_idx, max_depth=1)
        if child_idxs is not None:
            data = data[data.index.get_level_values(IDX_CHILD).isin(child_idxs)]
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.set_offsets_to_dates: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {OFFSET} field.')
        min_offset = data[OFFSET].min()
        min_date = data.at[(data[OFFSET] == min_offset).idxmax(), DATE_BEGIN]
        if pd.isna(min_date):
            raise ValueError(f'DataSet.set_offsets_to_dates: {DATE_BEGIN} corresponding to min {OFFSET} contains NA value.')
        data[OFFSET] -= min_offset
        idxs = data.index.get_level_values(IDX_CHILD).to_list()
        self.freeze_sequences(idxs)
        self.sequences.loc[idxs, DATE_BEGIN] =  data.reset_index().set_index(IDX_CHILD)[OFFSET] + min_date
        self.sequences.loc[idxs, DATE_END] = self.sequences.loc[idxs, DATE_BEGIN] + self.sequences.loc[idxs, DATA_LENGTH] - 1        
        self.log_sequences(idxs, 'set_offsets_to_dates')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_date_begin(self, parent_idx, child_idxs=None, notify=True):
        data = self.get_data(parent_idx, max_depth=1)
        if child_idxs is not None:
            data = data[data.index.get_level_values(IDX_CHILD).isin(child_idxs)]
        if data[DATE_END].isna().any():
            raise ValueError(f'DataSet.set_date_begin: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATE_END} field.')
        if data[DATA_LENGTH].isna().any():
            raise ValueError(f'DataSet.set_date_begin: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATA_LENGTH} field.')
        idxs = data.index.get_level_values(IDX_CHILD).to_list()
        self.freeze_sequences(idxs)
        self.sequences.loc[idxs, DATE_BEGIN] =  self.sequences.loc[idxs, DATE_END] - self.sequences.loc[idxs, DATA_LENGTH] + 1
        self.log_sequences(idxs, 'set_date_begin')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_date_end(self, parent_idx, child_idxs=None, notify=True):
        data = self.get_data(parent_idx, max_depth=1)
        if child_idxs is not None:
            data = data[data.index.get_level_values(IDX_CHILD).isin(child_idxs)]
        if data[DATE_BEGIN].isna().any():
            raise ValueError(f'DataSet.set_date_end: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATE_BEGIN} field.')
        if data[DATA_LENGTH].isna().any():
            raise ValueError(f'DataSet.set_date_end: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATA_LENGTH} field.')
        idxs = data.index.get_level_values(IDX_CHILD).to_list()
        self.freeze_sequences(idxs)
        self.sequences.loc[idxs, DATE_END] =  self.sequences.loc[idxs, DATE_BEGIN] + self.sequences.loc[idxs, DATA_LENGTH] - 1
        self.log_sequences(idxs, 'set_date_end')
        if notify:
            self.notify_changes('notify_synchronize')


    def check_ring_count(self, parent_idx):
        """
        Check the ring count of the given parent index.

        Args:
            parent_idx (int): The index of the parent.

        Raises:
            ValueError: If the ring count does not match the length of the values.

        Returns:
            None
        """
        def length_(values):
            l = len(values) if values is not None else 0
            #logger.debug(f'{l}, {values}')
            return l
        data = self.get_data(parent_idx, max_depth=1)
        ring_count = data[DATA_VALUES].apply(lambda x: length_(x))
        if ring_count != data[DATA_LENGTH]:
            raise ValueError(f'{DATA_LENGTH} does not match the length of {DATA_VALUES}.')

    def check_date_ring_count(self, parent_idx):
        """
        Checks the date and ring count consistency for a given parent index.

        Args:
            parent_idx (int): The index of the parent node.

        Raises:
            ValueError: If the date and ring count are not consistent.

        Returns:
            None
        """
        self.check_ring_count(parent_idx)
        data = self.get_data(parent_idx, max_depth=1)
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date        
        data[DATE_END] -= min_date
        if (data[DATE_END] - data[DATE_BEGIN] +1) != data[DATA_LENGTH]:
            raise ValueError(f'DataSet.check_date_ring_count: {DATE_BEGIN} - {DATE_BEGIN} and {DATA_LENGTH} are not consistent.')
    
    def check_offset_begin_date(self, parent_idx):
        """
        Check the consistency between the 'OFFSET' and 'DATE_BEGIN' columns in the dataset.

        Args:
            parent_idx (int): The index of the parent dataset.

        Raises:
            ValueError: If the 'OFFSET' and 'DATE_BEGIN' columns are not consistent.

        Returns:
            None
        """
        data = self.get_data(parent_idx, max_depth=1)
        data[OFFSET] -= data[OFFSET].min()
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date
        if data[OFFSET] != data[DATE_BEGIN]:
            raise ValueError(f'DataSet.check_offset_begin_date: {DATE_BEGIN} and {OFFSET} are not consistent.')
        
    def check_date_offset_count(self, parent_idx):
        """
        Checks the date offset count for a given parent index.

        Parameters:
        - parent_idx (int): The index of the parent.

        Returns:
        None
        """
        self.check_date_ring_count(parent_idx)
        self.check_offset_begin_date(parent_idx)

    def set_dates(self, idx, date_begin, data_length=None, sequences=None, warning=True):
        """
        Set DATE_END and DATE_BEGIN (if not NA) of `idx` series given a `date_begin` 
        and a `ring_count`.

        Parameters:
        - idx (int): The index of the series.
        - date_begin (datetime): The beginning date for the series.
        - data_length (int, optional): The length of the data. If not provided, it will be retrieved from the sequences.
        - sequences (pandas.DataFrame, optional): The sequences dataframe. If not provided, it will use the self.sequences.
        - warning (bool, optional): Whether to show a warning if there is a potential inconsistent chronology. Default is True.
        """
        if sequences is None:
            sequences = self.sequences
        if pd.notna(date_begin):
            keycode = sequences.at[idx, KEYCODE]
            date_first = sequences.at[idx, DATE_BEGIN]
            if pd.notna(date_first) and (date_begin != date_first) and (warning):
                logger.warning(f'potential inconsistent chronology, {keycode} {DATE_BEGIN} changed: {date_begin} ')
            if data_length is None:
                data_length = sequences.at[idx, DATA_LENGTH]
            else:
                sequences.at[idx, DATA_LENGTH] = data_length
            sequences.at[idx, DATE_BEGIN] = date_begin                
            sequences.at[idx, DATE_END] = date_begin + data_length - 1
    
    def set_chononology_info(self, idx, means, weights, offsets, data_type, data_samples, sequences=None):
        """
        Set the chronology information for a given index in the dataset.

        Args:
            idx (int): The index of the sequence to update.
            means (list): The mean values of the sequence.
            weights (list): The weights of the sequence.
            offsets (list): The offsets of the sequence.
            data_type (str): The type of data.
            data_samples (pandas.DataFrame): The data samples.
            sequences (pandas.DataFrame, optional): The sequences dataframe. Defaults to None.

        Returns:
            None
        """
        if sequences is None:
            sequences = self.sequences
        self.freeze_sequences(idx)
        sequences.at[idx, DATA_VALUES] = means
        sequences.at[idx, DATA_TYPE] = data_type
        sequences.at[idx, DATA_LENGTH] = len(means)
        sequences.at[idx, DATA_WEIGHTS] = weights
        sequences.at[idx, DATA_INFO] = offsets
        sequences.at[idx, DATE_SAMPLING] = datetime.now()
        sequences.at[idx, INCONSISTENT] = False
        sequences.at[idx, CAMBIUM] = False
        sequences.at[idx, PITH] = False
        sequences.at[idx, CAMBIUM_SEASON] = ''
        sequences.at[idx, SAPWOOD] = pd.NA
        
        sequences.at[idx, CATEGORY] = CHRONOLOGY
        for key in [SITE_ELEVATION, SITE_CODE, SITE_LATITUDE, SITE_LONGITUDE, SPECIES, LABORATORY_CODE, PROJECT, URI]: 
            l = data_samples[key].unique()
            if len(l) == 1:
                sequences.at[idx, key] = l[0]
        date_min = data_samples[DATE_BEGIN].min()
        self.set_dates(idx, date_min, len(means))
        sequences.at[idx, COMPONENT_COUNT] = len(data_samples)
        
        self.log_sequences(idx, 'Chronology update')
    
    def chronologies(self, idxs, date_as_offset=False, biweight=False, num_threads=1):
        """
        Compute chronologies for the given indices.

        Args:
            idxs (list): List of indices for which to compute chronologies.
            date_as_offset (bool, optional): Whether to treat dates as offsets. Defaults to False.
            biweight (bool, optional): Whether to use biweight location and scale estimators. Defaults to False.
            num_threads (int, optional): Number of threads to use for computation. Defaults to 1.

        Returns:
            None
        """
        tree = self.get_descendants(idxs)
        node_chronologies = tree.filter(categories=[CHRONOLOGY, SET], max_depth=1) 
        idx_chronologies = []
        data_dict = {}
        for node in node_chronologies:
            idx = node.idx
            if idx in idxs: # Need in the return
                if (idx not in idx_chronologies):  # Never computed 
                    idx_chronologies.append(idx)
                    samples = {node.idx: offset for node, offset in node.descendants[TREE].items()}
                    dt_data = self.get_sequences(list(samples.keys())).copy()
                    dt_data[OFFSET] = list(samples.values())
                    data_dict[idx] = dt_data
        results = chronologies(data_dict, ring_type=RAW, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
        for idx, values in results.items():
            means, weights, offsets = values
            self.set_chononology_info(idx, means, weights, offsets, RAW, data_dict[idx], sequences=None)
        
        if self.save_auto:
            self.dump()

    def detrend(self, idxs, ring_type, window_size=5, do_log=False, date_as_offset=False, biweight=False, num_threads=1):
        """
        Detrends the data for the specified indices.

        Args:
            idxs (list): List of indices to detrend.
            ring_type (str): Type of ring data.
            window_size (int, optional): Size of the moving window for detrending. Defaults to 5.
            do_log (bool, optional): Whether to apply logarithmic transformation. Defaults to False.
            date_as_offset (bool, optional): Whether to treat dates as offsets. Defaults to False.
            biweight (bool, optional): Whether to use biweight location and scale estimators. Defaults to False.
            num_threads (int, optional): Number of threads to use for parallel processing. Defaults to 1.

        Returns:
            pandas.DataFrame: Detrended data for the specified indices.
        """
        tree = self.get_descendants(idxs)

        if TREE in tree.descendants:
            idxs_samples = list(set([node.idx for node in tree.descendants[TREE].keys()]))
            data_samples = self.get_sequences(idxs_samples)
            dt_samples = detrend(data_samples, ring_type, window_size=window_size, do_log=do_log, num_threads=num_threads)
        dt_chonology = []
        if CHRONOLOGY in tree.descendants:
            node_chronologies = tree.filter(categories=[CHRONOLOGY], max_depth=1)
            idx_chronologies = []
            data_dict = {}
            for node in node_chronologies:
                idx = node.idx
                if idx in idxs: # Need in the return
                    if (idx not in idx_chronologies):  # Never computed 
                        idx_chronologies.append(idx)
                        samples = {node.idx: offset for node, offset in node.descendants[TREE].items()}
                        dt_data = dt_samples.loc[list(samples.keys()), :]
                        dt_data[OFFSET] = list(samples.values())
                        data_dict[idx] = dt_data
            results = chronologies(data_dict, ring_type=ring_type, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
            for idx, values in results.items():
                means, weights, offsets = values
                seq = self.get_sequences(idx).copy()
                self.set_chononology_info(idx, means, weights, offsets, ring_type, data_dict[idx], sequences=seq)
                dt_chonology.append(seq)
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            data_dt = pd.concat([dt_samples]+dt_chonology)
        return data_dt.loc[idxs, :]

    def check(self, idx):
        def check_children(node):
            children = node.get_children()
            idx_children = [node.idx for node in children.keys()]
            category_children = [node.category for node in children.keys()]
            offsets = pd.Series([offset for offset in children.values()], index=idx_children)
            offset_nonan = offsets.notna()
            noffset = offset_nonan.sum()
            offsets_norm = offsets - offsets.min()
            keycodes = self.sequences.loc[idx_children, KEYCODE]
            dates = self.sequences.loc[idx_children, DATE_BEGIN]
            date_nonan = dates.notna()
            dates_norm = dates - dates.min()
            ndate = date_nonan.sum()
            norm = dates_norm.max()+offsets_norm.max()
            diff =  dates_norm.fillna(norm) != offsets_norm.fillna(norm) 
            equal =  dates_norm.fillna(norm) == offsets_norm.fillna(norm) 
            ndiff = diff.sum()
            if node.category == CHRONOLOGY:
                if (ndiff == 0) and (ndate == len(dates)) and (noffset == len(offsets)): 
                    if SET not in category_children:
                        msg = '1: dates and offsets are consistent.'
                    else:
                        msg = '-1: dates and offsets are consistent. But some children are "set".'
                elif (ndate == len(dates)) and (noffset == 0):
                    # all dates, no offset
                    if SET not in category_children:
                        msg = '2: dates are available, no offsets. Offsets update required.'
                    else:
                        msg = '-2: dates are available, no offsets. Offsets update required. But some children are "set".'
                elif (noffset == len(offsets)) and (ndate == 0):
                    # all offsets, no date
                    msg = '3: offsets are available, no dates. Undated serie.'
                elif (noffset == len(offsets)) and (equal[dates != pd.NA].sum() == ndate):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '4: offsets are available, some empty dates. subset of dates and offsets are consistent. Years update required.'
                    else:
                        msg = '-4: offsets are available, some empty dates. But some children are "set".'
                elif (ndate == len(dates)) and (equal[offsets != pd.NA].sum() == noffset):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '5: Years are available, some empty offsets. subset of dates and offsets are consistent. Offsets update required.'
                    else:
                        msg = '-5: Years are available, some empty offset. But some children are "set".'
                else:
                    if SET not in category_children:
                        msg = '-6: Years and offsets are unconsistent. Undated serie. '
                    else:
                        msg = f'-7: Contain {SET}, dates and offsets are unconsistent. Undated serie.'
            else:
                msg = f'-7: Years and offsets are unconsistent. Parent is not a {CHRONOLOGY}. Correction required'
            
            info = [(node.idx, self.sequences.at[node.idx, KEYCODE], self.sequences.at[node.idx, CATEGORY],
                          self.sequences.at[node.idx, DATE_BEGIN],  pd.NA,  pd.NA , pd.NA, pd.NA)]
            info += zip(idx_children, keycodes.to_list(), category_children, dates.tolist(), offsets.tolist(), 
                        dates_norm.tolist(), offsets_norm.tolist(), equal)            
            df = pd.DataFrame(info, columns=[IDX, KEYCODE, CATEGORY, DATE_BEGIN, OFFSET, DATE_BEGIN_NORM, OFFSET_NORM, 'date ~ offset'])          
            return (msg, df)
        
        def get(node):
            out[node.idx] = check_children(node)
            for child_node in node.children:
                if child_node.category != TREE:
                    get(child_node)
        
        out = {}
        tree = self.get_descendants(idx)
        for child_node in tree.children:
            get(child_node)        
        return out

    def statistics(self, columns=[IDX, KEYCODE], stat_columns=[DATA_NAN], data=None):
        """
        Calculate statistics for the dataset.

        Args:
            columns (list, optional): List of columns to include in the statistics. Defaults to [IDX, KEYCODE].
            stat_columns (list, optional): List of additional statistics columns to include. Defaults to [DATA_NAN].
            data (pandas.DataFrame, optional): Data to calculate statistics on. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame containing the calculated statistics.

        """
        stats_lst = []
        if data is None:
            data = self.sequences
        for idx, row in data.iterrows():
            stats = row[columns].to_dict()
            if pd.notna(row[DATA_LENGTH]) and (row[DATA_LENGTH] > 0):
                values = row[DATA_VALUES]
                ring_nan = np.sum(np.isnan(values))
                values = values[~np.isnan(values)]
                stats2 = {
                    DATA_NAN: ring_nan,
                    STAT_MEAN: np.mean(values),
                    STAT_MEDIAN: np.median(values),
                    #STAT_MODE: mode(values).mode[0],
                    STAT_STD: np.std(values),
                    #STAT_VAR: np.var(values),
                    STAT_MIN: np.min(values),
                    STAT_MAX: np.max(values),
                    STAT_PERC25: np.percentile(values, 25),
                    STAT_PERC50: np.percentile(values, 50),
                    STAT_PERC75: np.percentile(values, 75),
                    STAT_SUM: np.sum(values),
                    STAT_KURTOSIS: kurtosis(values),
                    STAT_SKEWNESS: skew(values),
                    STAT_ENTROPY: entropy(values)
                }
            stats_lst.append(stats | stats2)
        return pd.DataFrame(stats_lst)[columns+stat_columns]

    def get_keycodes(self, idxs, fields=None):
            """
            Generate unique keycodes for each element stored in attributes of the Sequences DataFrame.

            Args:
                idxs (list): A list of indices corresponding to the elements for which keycodes need to be generated.
                fields (list, optional): A list of fields to include in the generated keycodes. Defaults to None.

            Returns:
                dict: A dictionary containing the keycodes as keys and their corresponding values.
            """
            cols = [KEYCODE, PROJECT]
            if fields is not None:
                cols += fields
            data = self.sequences.loc[idxs, cols]
            if fields == None:
                if len(data) == len(data[KEYCODE].unique()):
                    return {x:y for x, y in zip(data.index, data[KEYCODE])}
                if len(data) == len(data[[PROJECT, KEYCODE]].drop_duplicates()):
                    return {x:f'{x}/{y}/{z}' for x, y, z in zip(data.index, data[PROJECT], data[KEYCODE])}
                return {x:f'{x}/{y}' for x, y in zip(data.index, data[KEYCODE])}
            else:
                return {x:f'{x}/{y}' for x, y in zip(data.index, data[fields])}

    def detrend_package(self, package_key, ring_type, window_size=5, do_log=False, date_as_offset=False, biweight=False, num_threads=1,
                       slope_resolution=None, cambium_estimation=None):
        
        def info(df, idxs):
            message_type = 'primary'
            message = f'Detrend data is {ring_type} '
            message += ', '.join([f'{index}: {valeur}' for index, valeur in df[CATEGORY].value_counts().items()]) +'.'
            if len(idxs) != len(df[IDX_CHILD]):
                message += 'Duplicate series.'
            if df[INCONSISTENT].any():
                message += ' one or more series is inconsistent.'
                message_type = 'warning'

            return message_type, message

        data = self.get_package_components(package_key, slope_resolution, cambium_estimation).reset_index()
        idxs = data[IDX_CHILD].unique().tolist()
        if len(idxs) <= 0:
            return None, 'warning', 'Detrend data is empty set'
        elif (ring_type != RAW):
            dt_data = self.detrend(idxs, ring_type, window_size=window_size, do_log=do_log, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
            data_cols = [DATA_LENGTH, DATA_TYPE, DATA_VALUES, DATA_WEIGHTS, DATA_INFO, INCONSISTENT]
            other_cols = data.columns.difference(data_cols)
            data = data[other_cols].join(dt_data[data_cols], on=IDX_CHILD, how='left')

        message_type, message = info(data, idxs)
        return data, message_type, message

    def read_buffer(self, keycode_parent, buffer, mine_type=None):
        perror('read_buffer', mine_type)
        suffix = '.p'
        if mine_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            suffix = '.xlsx'
        elif mine_type == 'text/csv':
            suffix = '.csv'
        elif mine_type == 'application/json':
            suffix = '.json'
        output_file = Path(self.cfg_tmp) / Path(keycode_parent).with_suffix(suffix)
        with open(output_file, 'wb') as f:
            f.write(buffer)  # Récupère le contenu binaire du buffer
        
        
        self.load(output_file) 
        output_file.unlink()
        return self    