import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_group_bar(
        anc_control,
        group="mmilow",
        ref_group="mmihigh",
        top_n=30,
        fc_cut=0.0,
        top_name_map=None,
        ax=None,
):
    
    """
    Significant value log2FC barplotting to ANCOM-BC results.

    Parameters
    -----------
    anc_control : pandas.DataFrame
        after reset_index(), DF have "Covariate", "Log2(FC)", "Signif", "FeatureID"... etc
    covariate_value : str
        Covariate value by using filtering. (e.g. Group[T.#Groupvalue]).
    top_n : int
        show top N feature by selection rank to | log2FC | value.
    fc_cut : float
        folc change cut-off by using to significant category classification.
    top_name_map : dict or None
        Make feature-id name simply.
    ax :  matplotlib.axes.Axes or None
        visualization by existing axes. if None, make new Figure/Axes.


    Returns
    -----------
    ax: matplotlib.axes.Axes
    """

    covariate_value = f"Group[T.{group}]"

    vi = anc_control.reset_index()
    # covariate_value use.
    low_rows = vi[vi["Covariate"] == covariate_value].copy()
    
    low_rows.rename(columns={"Log2(FC)":"log2FC"}, inplace=True)
    
    # fc_cut은 factor use.
    def label_cat(row):
        if row["Signif"] and row["log2FC"] > fc_cut:
            return f"{group}"
        elif row["Signif"] and row["log2FC"] < -fc_cut:
            return f"{ref_group}"
        else:
            return "nonsignificant"
    
    low_rows["category"] = low_rows.apply(label_cat, axis=1)   


    if top_name_map is not None:
        low_rows["FeatureID"] = low_rows["FeatureID"].replace(top_name_map)

    top = (
        low_rows
        .sort_values("log2FC", key=lambda s: s.abs(), ascending=False)
        .head(top_n)
    )


    # x-axis feature scaling by feature abundance ranking
    order_feat = top.sort_values("log2FC")["FeatureID"]

    # I think this palette change. e.g. covariate_value.
    palette = {
        f"{group}": "#9fbccaa0",      # + sign
        f"{ref_group}": "#326a81a0",     # - sign 
        "nonsignificant": "lightgray",
    }
    
    if ax is None:
        N = top_n
        plt.figure(figsize=(2.5, N / 10 + 0.5), dpi=300)
        ax = plt.gca()
    
    ax = sns.barplot(
        data=top,
        x="log2FC",
        y="FeatureID",
        hue="category",
        palette=palette,
        order=order_feat,
        ax=ax,
    )

    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Log2 fold change")
    ax.set_ylabel("Feature")

    # legend 정리
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc="upper left")
