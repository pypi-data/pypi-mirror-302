import re
# import matplotlib.pyplot as plt
import polars as pl
import pandas as pd
import numpy as np
import boto3
from dataclasses import dataclass, field
import json
import os
from functools import reduce
from tqdm import tqdm
from math import e


# Turn off annoying pandas warnings
pd.options.mode.chained_assignment = None
pd.set_option("future.no_silent_downcasting", True)

module_dir = os.path.dirname(__file__)




@dataclass
class DataContainer:
    path: str

    # To be computed
    filetype: str = None # diann or encyclopedia
    datatype: str = None # protein or peptide
    raw_df: pd.DataFrame = None
    batches: list = None
    normalized_df: pd.DataFrame = None
    z_scores: pd.DataFrame = None
    median_z_scores: pd.DataFrame = None # only for peptide data
    melted_z_scores: pd.DataFrame = None

    def __post_init__(self):
        self._detect_filetype()
        self._detect_datatype()

    def _detect_filetype(self):
        if self.filetype is None:
            if "encyclopedia" in self.path:
                self.filetype = "encyclopedia"
            # Otherwise keep the default of "diann"
            else:
                self.filetype = "diann"
            
    def _detect_datatype(self):
        if self.datatype is None:
            if "pr_matrix" in self.path or "peptides" in self.path:
                self.datatype = "peptide"
            elif "pg_matrix" in self.path or "proteins" in self.path:
                self.datatype = "protein"
            else:
                raise ValueError("Unable to determine data type from path.")

@dataclass
class DataLoader():


    def load_data(self, path,
                  filetype=None,
                  datatype=None,
                  target=None,
                  get_batches=False,
                  merge_type='left'):
        
        if isinstance(path, list) and len(path) == 2:
            merge_data = True
        else:
            merge_data = False

        if isinstance(path, list) and len(path) > 2:
            raise ValueError("Data loading is only supported with max 2 paths.")
        
        # Instantiate DataContainer
        data_container = DataContainer(path,
                                       filetype=filetype,
                                       datatype=datatype)

        if merge_data:
            path_list = path
            path = path_list[0]

        if get_batches:
            data_container.batches = ProcessUtils.get_batches(data_container.path)
        
        lazy_df = self._load_lazy_df(path)

        # Filter for targets, if provided
        if target is not None:
            lazy_df = self._filter_targets(data_container.filetype, 
                                           lazy_df,
                                           target)

        # Collect all column names for filtering
        df = self._select_columns_of_interest(data_container, lazy_df)

        # If a second path is given, load and merge that path
        if merge_data:
            # collect the smaller df to get info on targets. Convert to 
            # diann style if encyclopedia
            data_container.raw_df = df.collect(streaming=True).to_pandas()
            if data_container.filetype == "encyclopedia":
                data_container = PeptideProcessor. \
                    _convert_encyclopedia_file(data_container)
            df = data_container.raw_df
            merge_targets = df["Genes"].unique()
            df = pl.from_pandas(df).lazy() # back to lazy dataframe

            second_lazy_df = self._load_lazy_df(path_list[1])
            second_lazy_df = self._filter_targets("diann",
                                                  second_lazy_df,
                                                  merge_targets)
            second_lazy_df = self._select_columns_of_interest(data_container, 
                                                              second_lazy_df)

            df = df.join(second_lazy_df,
                         on=DataLoader._detect_id_columns(data_container),
                         how=merge_type)

        # Collect the DataFrame
        df = df.collect(streaming=True).to_pandas()
        data_container.raw_df = df

        return data_container
    
    @staticmethod
    def extract_unique_genes(df):
        return list(set(gene for genes in df["Genes"] \
                         for gene in genes.split(";")))
    

    def _filter_targets(self, filetype, lazy_df, target):
        if type(target) not in [str, list, set]:
            raise TypeError("Target must be a string, list, or set")
        if not isinstance(target, set):
            target = set(target)
        #TODO: sort this out for diann vs encyclopedia
        if filetype == "diann" and target is not None:
            filter_expr = pl.col("Genes").str.contains("|".join(set(target)))
            lazy_df = lazy_df.filter(filter_expr)
        elif filetype == "encycolopedia" and target is not None:
            raise NotImplementedError("Target filtering for encyclopedia data" \
                                      " has yet to be implemented.")
        return lazy_df

    def _select_columns_of_interest(self, data_container, lazy_df):
        #TODO: There's probably a more elegant way of sharing datatype info...
        id_cols = DataLoader._detect_id_columns(data_container)
        file_suffix = self._detect_file_suffix(data_container)

        all_columns = lazy_df.collect_schema().names()
        selected_columns = id_cols + [col for col in all_columns \
                                      if col.endswith(file_suffix) \
                                        and col not in bad_batches]
        return lazy_df.select(selected_columns)
    
    @staticmethod
    def _detect_id_columns(data_container):
        if data_container.filetype == "diann":
            if data_container.datatype == "protein":
                return ["Protein.Ids", "Genes"]
            else:
                return ["Protein.Ids", "Genes", "Precursor.Id"]
        else: # encyclopedia
            if data_container.datatype == "protein":
                return ["Protein"]
            else:
                return ["Peptide", "Protein"]

    
    def _detect_file_suffix(self, data_container):
        return ".d" if data_container.filetype == "diann" else ".mzML"

    def _detect_file_format(self, path):
        if path.endswith(".csv"):
            return "csv"
        elif path.endswith(".tsv") or path.endswith(".txt"): # encylopedia paths end with .txt despite being tsv
            return "tsv"
        else:
            raise ValueError(f"Unsupported file format for file: {path}")

    def _load_lazy_df(self, path):
        file_format = self._detect_file_format(path)
        sep = "," if file_format == "csv" else "\t"
        lazy_df = pl.scan_csv(path,
                        separator=sep,
                        storage_options=self.get_storage_options(),
                        infer_schema_length=10000,
                        )
        
        return lazy_df

    @staticmethod
    def get_storage_options() -> dict[str, str]:
        """Get AWS credentials to enable polars scan_parquet functionality.
        """
        credentials = boto3.Session().get_credentials()
        return {
            "aws_access_key_id": credentials.access_key,
            "aws_secret_access_key": credentials.secret_key,
            "session_token": credentials.token,
            "aws_region": "us-west-2",
        }

@dataclass
class ProcessUtils:

    dropna_percent_threshold: float = 50

    label_screens: bool = True
    screen_split: dict = field(default_factory= 
                               # MSR numbers by which to split screens
                               lambda: {(0, 5863): "THP-1 1K",  
                               (5863, 1e16): "Anborn"})
    ignore_missing_ranges: bool = False
    label_tfs: bool=True
    tf_list: list=None
    gene_info_by_acc: dict=None


    def __post_init__(self):
        if self.label_screens:
            if self.screen_split is None:
                raise ValueError("Provide a dictionary to label screens.")
            if not self.ignore_missing_ranges:
                missing_ranges = self._check_missing_ranges()
                if len(missing_ranges) > 0:
                    raise ValueError(f"Missing MSR numbers in screen" \
                                     " dictionary.\nUnable to label MSR" \
                                     " numbers in range(s) {missing_ranges}.\n"
                                     "To ignore missing ranges, " \
                                     "set ignore_missing_ranges=True. Invalid "\
                                      "screen numbers will be labeled 'NaN'."
                                    ) 
        if self.dropna_percent_threshold <=1:
            raise Warning(f"dropna_percent_threshold is a percent. " \
                          "Not a portion. Passing a value of 1 or less will " \
                          "exlude columns unless they are 99%+ not NaN.")
        if self.label_tfs:
            self.tf_list = self.load_tf_list()

    def _drop_nan_cols(self, df):
        nan_percentage = df.isnull().sum() * 100 / len(df)
        df = df.drop(columns=
                     nan_percentage[nan_percentage >= 
                                    self.dropna_percent_threshold].index)
        return df
    
    def load_tf_list(self):
        tf_path = os.path.join(module_dir, "acc_by_tf_gene.json")
        with open(tf_path, 'r') as file:
            acc_by_tf_gene = json.load(file)
        self.tf_list = list(acc_by_tf_gene.keys())
        return self.tf_list

    @staticmethod
    def load_gene_info():
        gene_info_path = os.path.join(module_dir, "gene_info_by_acc.json")
        with open(gene_info_path, 'r') as file:
            gene_info_by_acc = json.load(file)
        return gene_info_by_acc

    def _is_tf(self, gene):
        gene_list = gene.split(';')
        return any(gene in self.tf_list for gene in gene_list)

    def _label_tfs(self, df):
        df["Is TF"] = df["Genes"].apply(self._is_tf)
        return df

    def _split_batch_screen(self, df):
        df[['batch', 'screen']] = df['batch'].str.split('_', expand=True)
        return df
        
    
    def _get_batch_compound_names(self, pivot_df):
        pivot_df["batch"] = pivot_df["Compound"].astype(str) \
            .str.extract(r'(SET\d+(-\d+)?REP\d+(-\d+)?)')[0] \
                .astype("category").to_list()
        if self.label_screens:
            pivot_df["batch"] = pivot_df["batch"] + "_" + \
                pivot_df["Compound"].apply(self._get_screen)
        pivot_df["Compound"] = pivot_df["Compound"] \
            .apply(self._get_compound_name)
        return pivot_df
    
    def _get_compound_name(self, s: str) -> str:
        """
        Extracts the compound name from the name of the file.
    
        Parameters
        ----------
        s: str
            An entry from the "Filename" column, a path to where 
            the file is located
        
        Returns
        -------
        str
            The name of the treatment compound
        """
        # Look for compounds with the name TAL####
        if "TAL" in s.upper():
            tal_num = re.search(r'TAL\d+(-\d+)?', s)[0]
            # Strip leading zeros if present
            num = int(re.search(r'\d+(-\d+)?', tal_num)[0])
            new_name = "TAL" + str(num)
            return new_name
        elif "DMSO" in s.upper():
            return "DMSO"
        elif "PRTC" in s.upper():
            return "PRTC"
        elif "nuclei" in s.lower():
            return "NUC"
        elif "nuc" in s.lower(): # cases where it is labeled as NUC2
            nuc_num = re.search(r'NUC\d+(-\d+)?', s)
            if nuc_num is None:
                return "NUC"
            else:
                return nuc_num[0]
        elif "dbet" in s.lower():
            return "dBET6"
        elif "FRA" in s.upper():
            return "FRA"
        elif "none" in s.lower():
            return "None"
        else:
            raise Exception(f"Unable to extract compound from filename {s}.")
    
    def _get_screen(self, msr_str):
        if msr_str.startswith("MSR"):
            try:        
                msr = re.search(r'MSR\d+(-\d+)?', msr_str)[0]
            except:
                raise ValueError(f"Unable to match MSR for filename {msr_str}.")
            
            msr = int(re.search(r'\d+(-\d+)?', msr)[0])
        
            for msr_range, screen_name in self.screen_split.items():
                if isinstance(msr_range, tuple):
                    if msr_range[0] <= msr < msr_range[1]:
                        return screen_name
            raise ValueError(f"Unable to determine screen for MSR {str(msr)}.")
        else:
            screen_name = msr_str.split("_")[0]
            try:
                screen = self.screen_split[screen_name]
            except KeyError:
                raise KeyError(f"Screen name {screen_name} not in screen_dict.")
            return screen

    
    def _check_missing_ranges(self):
        quant_keys = [key for key in self.screen_split.keys() \
                      if isinstance(key, tuple)]
        sorted_ranges = sorted(quant_keys)
        missing_ranges = []

        for i in range(len(sorted_ranges) - 1):
            current_end = sorted_ranges[i][1]
            next_start = sorted_ranges[i+1][0]

            if current_end < next_start:
                missing_ranges.append((current_end, next_start))
        return missing_ranges
    

    @staticmethod
    def get_batches(path):
        if isinstance(path, str):
            path = [path]
        batches = []
        for p in path:
            sep = ',' if p.endswith(".csv") else '\t'
            lazy_df = pl.scan_csv(p,
                            separator=sep,
                            storage_options=DataLoader.get_storage_options(),
                            infer_schema_length=10000,
                            )
            column_names = lazy_df.collect_schema().names()
            p_batches = []
            for column in column_names:
                batch = re.search(r'SET\d+(-\d+)?REP\d+(-\d+)?', column)
                if isinstance(batch, re.Match):
                    p_batches.append(batch[0])
            batches += list(set(p_batches))
        return batches
    
    @staticmethod
    def filter_screens(df, screens):
        if isinstance(screens, str):
            return df.loc[df["screen"] == screens]
        elif isinstance(screens, list(str)):
            return df.loc[df["screen"].isin(screens)]
        else:
            raise TypeError("Provides screen(s) as string or list of strings.")

@dataclass
class PeptideProcessor(ProcessUtils):

    progress_bar: bool=True

    def __post_init__(self):
        super().__post_init__()


    def process_and_normalize(self, data_container,
                              process_by_batch=False,
                              copy=True,
                              normalize_abundance=False):
        
        if data_container.datatype == "protein":
            raise ValueError("Function received protein data. \
                             Provide petide data or use ProteinProcessor.")

        if data_container.filetype == "encyclopedia":
            data_container = self._convert_encyclopedia_file(data_container)
        
        if copy:
            pep_df = data_container.raw_df.copy()
        else:
            pep_df = data_container.raw_df
            # raise Warning("Modiying raw_df. Set copy=True to avoid this.")
        
        if process_by_batch:

            id_cols = DataLoader._detect_id_columns(data_container)

            processed_batch_dfs = []

            if data_container.batches is None:
                data_container.batches = ProcessUtils \
                    .get_batches(data_container.path)
            
            for batch in tqdm(data_container.batches, 
                              desc="Processing Batches", 
                              unit="batch"):
                """Yes this will extract batches from multiple screens if there
                are SET1REP1 in several batches for example. But the 
                _get_batch_compound_name will append the screen name to the 
                batch (if label_screens=True) so the true batches will be
                preserved for median normalization."""
                chunk_cols = [col for col in pep_df.columns if batch in col]
                subdf = pep_df[id_cols+chunk_cols]
                pivot_df = self._melt_pivot_df(subdf)
                pivot_df = self._get_batch_compound_names(pivot_df)
                if normalize_abundance:
                    normalized_df = self._normalize_abundance(pivot_df)
                else:
                    normalized_df = self._median_normalize(pivot_df)
                processed_batch_dfs.append(normalized_df)

            normalized_df = pd.concat(processed_batch_dfs)
        else:
            pivot_df = self._melt_pivot_df(pep_df)
            pivot_df = self._get_batch_compound_names(pivot_df)
            if normalize_abundance:
                    normalized_df = self._normalize_abundance(pivot_df)
            else:
                normalized_df = self._median_normalize(pivot_df)

        if self.label_screens:
            normalized_df = self._split_batch_screen(normalized_df)
        normalized_df = self._drop_nan_cols(normalized_df)

        if normalized_df.empty:
            raise Exception("Dataframe is empty after dropping NaNs. \
                            Try lowering dropna_percent_threshold.")
        data_container.normalized_df = normalized_df
    

    @staticmethod
    def _convert_encyclopedia_file(data_container):
        gene_info_by_acc = ProcessUtils.load_gene_info()
        # Take an encyclopedia file and convert it to look like a diann file
        rename_dict = {"Peptide": "Precursor.Id",
                       "Protein": "Protein.Ids"}
        df = data_container.raw_df 
        df = df.rename(columns=rename_dict)
        df[["Genes", "Protein.Ids"]] = df["Protein.Ids"] \
            .apply(lambda x: PeptideProcessor \
                   ._extract_gene_info(x, gene_info_by_acc))
        data_container.raw_df = df
        data_container.filetype = "diann"
        return data_container

    @staticmethod
    def _extract_gene_info(protein_ids, gene_info_by_acc):
        protein_list = protein_ids.split(';')

        gene_ids = set() 
        clean_proteins = [] 
        
        for protein in protein_list:
            if '|' in protein:
                protein_id = protein.split('|')[1]
            else:
                protein_id = protein
                
            base_protein_id = protein_id.split('-')[0]

            base_protein_id = protein_id.split('-')[0]
            gene_info = gene_info_by_acc.get(base_protein_id, {})
            gene_name = gene_info.get('id', 'Unknown')
            if gene_name is None:
                gene_name = "None"

            gene_ids.add(gene_name)
            clean_proteins.append(protein_id)
        
        genes = ';'.join(sorted(gene_ids))
        return pd.Series([genes, ';'.join(clean_proteins)])

    def _is_tf(self, gene):
        # Overwrite
        gene_list = gene.split(';')
        is_tf = any(gene in self.tf_list for gene in gene_list)
        return f"{gene}_{str(is_tf)}"
    
    def _label_tfs(self, df):
        # Overwrites the super method
        df["Genes"] = df["Genes"].apply(self._is_tf)
        return df


    def _melt_pivot_df(self, pep_df):
        quant_cols = [col for col in pep_df.columns \
                      if (col.endswith(".d") or col.endswith(".mzML"))]

        # Log transform 
        quant_pep_df = pep_df.replace({None: np.nan,
                                       0: np.nan}).infer_objects(copy=False)
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols] \
                                          .astype(float))

        # Restructure df so columns are peptides
        id_vars=["Protein.Ids", "Genes", "Precursor.Id"]    
        melt_df = quant_pep_df.melt(id_vars=id_vars, # Melt so filename is col.
                                    var_name="Compound",
                                    value_name="Log Abundance")
        pivoted_df = melt_df.pivot(index="Compound", 
                                   columns=id_vars,
                                   values="Log Abundance")
        pivoted_df.reset_index(inplace=True) # Make compound a normal column
        return pivoted_df

    def _normalize_abundance(self, pivot_df):
        # Get the median (log) abundances for each peptide for each screen
        medians = {}
        screens = list(self.screen_split.values())
        for screen in screens:
            subdf = pivot_df.loc[pivot_df["batch"].str.contains(screen)]
            quant_cols = [col for col in subdf.columns if col not in \
                [("Compound","",""), ("batch","","")]]
            medians[screen] = subdf[quant_cols].median()

        # Median normalize as usual
        normalized = self._median_normalize(pivot_df)

        # Add back in medians column by column for every screen
        for screen in screens:
            mask = normalized["batch"].str.contains(screen)
            for idx in medians[screen].index:
                normalized.loc[mask, idx] += medians[screen][idx]
        
        # Go back to linear scale for all abundance columns
        all_quant_cols = [col for col in normalized.columns if col not in \
                [("Compound","",""), ("batch","","")]]
        normalized[all_quant_cols] = np.exp(normalized[all_quant_cols])

        return normalized

    def melt_normalized_df(self, normalized_df):
        df = normalized_df.copy()
        id_cols = ['screen__', 'batch__', 'Compound__']
        df.columns = ['_'.join([str(i) for i in col]).strip() \
                                        for col in df.columns] # Combine mulitindex columns
        df_melted = pd.melt(
                    df, 
                    id_vars=id_cols,
                    value_vars=[col for col in df.columns \
                                if col not in id_cols],
                    var_name='multiindex', 
                    value_name='Abundance'
                )
        new_cols = ['Protein.Ids', 'Genes', 'Precursor.Id']
        df_melted[new_cols] = df_melted['multiindex'] \
            .str.split('_', expand=True)
        df_melted = df_melted.drop(columns=['multiindex'])
        df_melted = df_melted.rename(columns= \
                                    {key: key.rstrip("_") for key in id_cols})
        return df_melted

        

    def _median_normalize(self, pivot_df):

        # Drop empty batches
        pivot_df = pivot_df.groupby(("batch", "", "")).filter( \
            lambda x: not x.iloc[:,2:].isna().all().all())
        if pivot_df.empty:
            return pivot_df
    
        def subtract_median(group):
            if group.empty:
                return group
            # Check if the group contains any non-NaN values
            non_nan_values = group.iloc[:, 2:]  # Skip the first two columns
            if non_nan_values.isna().all().all():
                return group  # Return group unchanged if all values are NaN
            return group - group.median().median()
            
        pivot_df.index = pivot_df["Compound"] # Temporarily make compound the index
        pivot_df.drop(columns=["Compound"], level=0, inplace=True)
        normalized_df = pivot_df.groupby(("batch", "", ""), observed=False) \
            .apply(subtract_median, include_groups=True)
        normalized_df.reset_index(inplace=True) # Remove batch from index
        return normalized_df

@dataclass
class ProteinProcessor(ProcessUtils):
    

    def __post_init__(self):
        super().__post_init__()

    def process_and_normalize(self,
                              data_container,
                              normalize_abundance=True):
        # If normalize_abundance is true, then we'll median normalize,
        # add back in the median for the screen (as proxy for cell type) and 
        # then convert back to linear scale. Otherwise we'll just median 
        # normalized everything by batch so all medians will be 0 and everything 
        # remains log scale.
        if data_container.datatype == "peptide":
            raise ValueError("Function received peptide data. \
                Supply a protein DataContainer or use PeptideProcessor.")
        
        # Melt df so that columns are ["Protein.Ids", "Genes", "Compound",
        # "Abundance", and "batch"]
        prot_df = data_container.raw_df.copy()
        melt_df = self._melt_df(prot_df)
        melt_df = self._get_batch_compound_names(melt_df)

        if self.label_tfs: # Add column "Is TF" with bools
            melt_df = self._label_tfs(melt_df)

        # Normalize
        if normalize_abundance:
            normalized = self._normalize_abundance(melt_df)
        else:
            normalized = self._median_normalize(melt_df)
            if self.label_screens:
                normalized = self._split_batch_screen(normalized)

        # Drop rows where abundance is nan and put in data_container
        data_container.normalized_df = normalized.loc \
            [normalized["Abundance"].notna()]

    def _normalize_abundance(self, melt_df):
        # Get the median (log) abundances
        medians = {}
        screens = list(self.screen_split.values())
        for screen in screens:
            subdf = melt_df.loc[melt_df['batch'].str.contains(screen)]
            medians[screen] = subdf["Abundance"].median()

        # Median normalize per usual and separate batch and screen into columns
        normalized = self._median_normalize(melt_df)
        normalized = self._split_batch_screen(normalized)

        # Add back the screen medians
        def add_back_median(row, median_dict):
            return row["Abundance"] + median_dict[row['screen']]
        normalized["Abundance"] = normalized \
            .apply(lambda x: add_back_median(x, medians), axis=1)
    
        # Go back to linear scale
        normalized["Abundance"] = np.exp(normalized["Abundance"])

        return normalized

        



    def _melt_df(self, prot_df):

        quant_cols = [col for col in prot_df.columns \
                      if (col.endswith(".d") or col.endswith(".mzML"))]

        # Log transform 
        quant_pep_df = prot_df.replace({None: np.nan,
                                        0: np.nan}).infer_objects(copy=False)
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols] \
                                          .astype(float))

        df = quant_pep_df[["Protein.Ids", "Genes"] + quant_cols]
        df = self._drop_nan_cols(df)
        if df.empty:
            raise Exception("Dataframe is empty after dropping NaNs. \
                            Try lowering dropna_percent_threshold.")
        melt_df = df.melt(id_vars=["Protein.Ids", "Genes"],
                          var_name="Compound",
                          value_name="Abundance")
        melt_df = melt_df.loc[melt_df["Abundance"].notna()]
        return melt_df

    def _median_normalize(self, melt_df):
        def subtract_median(group):
            # For a protein in a batch, subtractract the median abundance
            group["Abundance"] = group["Abundance"] - \
                group["Abundance"].median()
            return group
        normalized_df = melt_df.groupby(["Genes", "batch"]) \
            .apply(subtract_median, include_groups=False).reset_index()
        dropcol = [col for col in normalized_df.columns \
                   if col.startswith("level")][0]
        normalized_df = normalized_df.drop(columns=dropcol)
        return normalized_df
        
@dataclass
class ProteinZScoreCalculator:

    

    def _compute_z_score(self, subdf):
        # Get the median abundance for the current screen
        med = subdf["Abundance"].median()

        # Get median absolute deviation
        subdf["abs dev"] = abs(subdf["Abundance"] - med)
        MAD = subdf["abs dev"].median()
        subdf.drop(columns=["abs dev"], inplace=True)

        # Calculate Z Score
        subdf["Z Score"] = (subdf["Abundance"] - med) / MAD
        return subdf

    def _get_median_z_score(self, z_scores):
        if "screen" in z_scores.columns.to_list():
            groups = ["screen", "Genes", "Compound"]
        else:
             groups = ["Genes", "Compound"]
        z_scores["med Z Score"] = z_scores.groupby(groups)["Z Score"] \
            .transform('median')
        return z_scores

    def compute_z_score(self, data_container):
        if data_container.datatype == "peptide":
            raise ValueError("Function received peptide data. \
                Provide protein data or use PeptideZScoreCalculator.")
        
        data = data_container.normalized_df.copy()
        if "screen" in data.columns.to_list():
            groups = ["screen", "Genes"]
        else:
             groups = ["Genes"]
        z_scores = data.groupby(groups).apply(self._compute_z_score, 
                                              include_groups=False) \
                                              .reset_index()
        z_scores = self._get_median_z_score(z_scores)

        dropcol = [col for col in z_scores if col.startswith("level")]
        z_scores = z_scores.drop(columns=dropcol)
        data_container.z_scores = z_scores
        # return data_container

@dataclass
class PeptideZScoreCalculator:

    def _compute_z_score(self, subdf):
        # Get median abundance for all peptides in the protein
        quant_cols = [col for col in subdf.columns \
                      if col not in [('batch', '', ''),\
                                      ('Compound', '', ''), ('screen', '', '')]]

        for column in tqdm(quant_cols, 
                            desc="Computing peptide z scores", 
                            unit="peptide"):
            MAD = abs(subdf[column] - subdf[column].median()).median()
            subdf[column] = (subdf[column] - subdf[column].median())/MAD
        return subdf
    
    def _check_data_type(self, data_container):
        if data_container.datatype == "protein":
            raise ValueError("Function received protein data. \
                Provide peptide data or use ProteinZScoreCalculator.")


    def compute_z_score(self, data_container):

        self._check_data_type(data_container)
        
        data = data_container.normalized_df
            
        if ("screen", "", "") in data.columns.to_list():
            groups = [("screen", "", "")]
            z_scores = data.groupby(groups).apply(self._compute_z_score, 
                                                  include_groups=False) \
                                                  .reset_index()
        else:
            z_scores = self._compute_z_score(data)

        dropcol = [col for col in z_scores.columns \
                   if col[0].startswith("level")]
        z_scores = z_scores.drop(columns=dropcol)
        data_container.z_scores = z_scores

    def _get_median_z_score(self, melted_z_scores):
        if "screen" in melted_z_scores.columns.to_list():
            groups = ["screen", "Genes", "Compound", "Precursor.Id"]
        else:
             groups = ["Genes", "Compound", "Precursor.Id"]
        melted_z_scores["med Z Score"] = melted_z_scores \
            .groupby(groups)["Z Score"].transform('median')
        return melted_z_scores
    
    def melt_z_score_df(self, data_container):
        self._check_data_type(data_container)

        z_scores_copy = data_container.z_scores.copy()
        if ("screen", "", "") in z_scores_copy.columns.to_list():
            id_cols = ['screen__', 'batch__', 'Compound__']
        else:
            id_cols = ['batch__', 'Compound__']

        z_scores_copy.columns = ['_'.join([str(i) for i in col]).strip() \
                                 for col in z_scores_copy.columns] # Combine mulitindex columns
        df_melted = pd.melt(
            z_scores_copy, 
            id_vars=id_cols,
            value_vars=[col for col in z_scores_copy.columns \
                        if col not in id_cols],
            var_name='multiindex', 
            value_name='Z Score'
        )
        if len(df_melted['multiindex'].iloc[0].split('_')) == 3:
            new_cols = ['Protein.Ids', 'Genes', 'Precursor.Id']
            df_melted[new_cols] = df_melted['multiindex'] \
                .str.split('_', expand=True)
        else:
            new_cols = ['Protein.Ids', 'Genes', 'Is TF', 'Precursor.Id']
            df_melted[new_cols] = df_melted['multiindex'] \
                .str.split('_', expand=True)
            df_melted["Is TF"] = df_melted["Is TF"] \
                .replace({'True': True, 'False': False})
            df_melted["Is TF"] = df_melted["Is TF"].astype(bool)
        
        df_melted = df_melted.drop(columns=['multiindex'])
        df_melted = df_melted.rename(columns= \
                                     {key: key.rstrip("_") for key in id_cols})

        df_melted = self._get_median_z_score(df_melted)

        dropcol = [col for col in df_melted if col.startswith("level")]
        df_melted = df_melted.drop(columns=dropcol)

        data_container.melted_z_scores = df_melted
        # return data_container
    
high_abundance_batches = """MSR8360_SET11REP2A2_FRA12000_DIA.d
MSR8363_SET11REP2A5_TAL0001080_DIA.d
MSR8368_SET11REP2A10_TAL0000561_DIA.d
MSR8371_SET11REP2B1_TAL0000576_DIA.d
MSR8373_SET11REP2B3_TAL0000803_DIA.d
MSR8376_SET11REP2B6_DMSO_DIA.d
MSR8378_SET11REP2B8_TAL0000087_DIA.d
MSR8380_SET11REP2B10_TAL0000610_DIA.d
MSR8385_SET11REP2C3_TAL0000981_DIA.d
MSR8386_SET11REP2C4_TAL0000252_DIA.d
MSR8387_SET11REP2C5_TAL0000900_DIA.d
MSR8388_SET11REP2C6_TAL0000204_DIA.d
MSR8392_SET11REP2C10_TAL0001052_DIA.d
MSR8395_SET11REP2D1_TAL0000853_DIA.d
MSR8398_SET11REP2D4_TAL0001701_DIA.d
MSR8403_SET11REP2D9_TAL0000400_DIA.d
MSR8405_SET11REP2D11_TAL0001701_DIA.d
MSR8410_SET11REP2E4_TAL0000490_DIA.d
MSR8412_SET11REP2E6_TAL0000729_DIA.d
MSR8413_SET11REP2E7_TAL0000896_DIA.d
MSR8417_SET11REP2E11_TAL0000305_DIA.d
MSR8421_SET11REP2F3_TAL0000387_DIA.d
MSR8422_SET11REP2F4_TAL0000240_DIA.d
MSR8423_SET11REP2F5_TAL0000693_DIA.d
MSR8425_SET11REP2F7_TAL0000294_DIA.d
MSR8426_SET11REP2F8_TAL0000764_DIA.d
MSR8428_SET11REP2F10_TAL0001058_DIA.d
MSR8429_SET11REP2F11_TAL0000397_DIA.d
MSR8437_SET11REP2G7_TAL0000989_DIA.d
MSR8439_SET11REP2G9_TAL0001073_DIA.d
MSR8448_SET11REP2H6_TAL0000442_DIA.d
MSR8449_SET11REP2H7_TAL0000342_DIA.d
MSR8450_SET11REP2H8_TAL0000105_DIA.d
MSR8451_SET11REP2H9_TAL0000398_DIA.d
MSR8453_SET11REP2H11_TAL0000752_DIA.d
MSR9222_SET4REP3H12_TAL0000309_DIA.d
MSR9306_SET11REP3G12_TAL0000817_DIA.d
MSR9318_SET11REP3H12_TAL0001052_DIA.d"""

bad_batches = high_abundance_batches.split("\n")