import pandas as pd
from pathlib import Path
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from skbio.stats.composition import ancombc
from ancombc_viz.simple_name import extract_p_g_or_f

class Analyzer:
    def __init__(self):
        self.ft = None
        self.ft_group_T = None
        self.mt = None
        self.formula = None
        self.mt_index = None
        self.results = None
        self.ancombc_signif = None
        self.feature_name_map = None

    def set_feature_table(self, ft, feature_name_map=None):
        self.ft = ft
        self.feature_name_map = feature_name_map
    def set_metadata(self, mt, formula="Group"):
        self.formula = formula
        self.mt = mt.loc[self.ft.index, [formula]].copy()
        self.ft_group_T = self.ft.copy()
        self.ft_group_T[formula] = self.mt[formula]
    
    def ancombc_analysis(self, feature_name_map=None):
        otu = self.ft + 1
        meta = self.mt

        self.results = ancombc(otu, meta, formula=self.formula) ## ANCOM-BC activation
        
        self.ancombc_signif = (self.results.query('Covariate != "Intercept" & Signif == True').round(3).reset_index().copy())

        name_map = feature_name_map or self.feature_name_map

        if name_map is not None:
            self.ancombc_signif["FeatureID"] = (self.ancombc_signif["FeatureID"].replace(name_map))

        return self.ancombc_signif
    

## ana = Analyzer()
## ana.set_feature_table(ft)
## ana.set_metadata(mt)
## sig = ana.ancombc_analysis()

        