import logging

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.ticker import FormatStrFormatter

sns.set()  # set seaborn as default
sns.set_style("whitegrid")  # set seaborn style

# general configuration for matplotlib
DEFAULT_SIZE = (15, 8)  # default figure size
DEFAULT_SIZE_SQUARE = (15, 15)  # default figure size for square plots

params = {
    "font.family": "serif",
    "legend.fontsize": "large",
    "figure.figsize": DEFAULT_SIZE,
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "large",
    "ytick.labelsize": "large",
}  # default figure size
pylab.rcParams.update(params)


class Plot:
    def __init__(self):

        # log
        self.logger = logging.getLogger(__name__)

    def plot_box(
        self, df, title="", xlabel="", ylabel="", figsize=DEFAULT_SIZE, yscale="symlog"
    ):
        fig, ax = plt.subplots(figsize=figsize)
        df.plot.box(
            showfliers=False,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            sym=None,
            patch_artist=True,
            boxprops=dict(facecolor="royalblue", color="black"),
            medianprops=dict(linestyle="-", linewidth=2.5, color="khaki"),
            ax=ax,
        )

        if yscale == "linear":
            ax.set_yscale(yscale)
        else:
            ax.set_yscale(yscale, linthresh=0.001)

        ax.set_xlabel(xlabel)
        plt.grid(True, axis="y")
        locs, labels = plt.xticks()
        plt.xticks(locs, labels, rotation=45)
        fig.tight_layout()

        return fig, ax

    def plot_heatmap(
        self, df, relation_type, title="", annotate=True, figsize=DEFAULT_SIZE
    ):

        fig, ax = plt.subplots(figsize=figsize)

        if relation_type == "corr":
            relations = df.corr()
            annot_fmt = "0.2f"
            shift = 1
            vmin, vmax = -1, 1
        elif relation_type == "cov":
            relations = df.cov()
            annot_fmt = "1.1g"
            shift = 1
            vmin, vmax = relations.min().min(), relations.max().max()
        else:
            raise NotImplementedError
        mask = np.zeros_like(relations)

        if relation_type in ["cov", "corr"]:
            mask[np.triu_indices_from(mask, k=shift)] = True
            xticklabels = relations.columns
            yticklabels = relations.columns

        sns.heatmap(
            relations,
            cmap="RdYlGn",
            mask=mask,
            xticklabels=xticklabels,
            yticklabels=yticklabels,
            annot=annotate,
            fmt=annot_fmt,
            annot_kws={"fontsize": 14},
            vmin=vmin,
            vmax=vmax,
            ax=ax,
        )

        if relation_type == "corr":
            locs, labels = plt.xticks()
            plt.xticks(locs, labels)
            locs, labels = plt.yticks()
            plt.yticks(locs, labels)

        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.title(title)
        fig.tight_layout()

        return fig, ax

    def plot_trend(
        self,
        df,
        title="",
        xlabel="",
        ylabel="",
        figsize=DEFAULT_SIZE,
        alpha=1.0,
        legend=True,
        marker="o",
        yscale="linear",
    ):
        fig, ax = plt.subplots(figsize=figsize)

        df.plot(
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            linewidth=1.5,
            alpha=alpha,
            ax=ax,
        )
        if legend:
            current_handles, current_labels = plt.gca().get_legend_handles_labels()
            plt.legend(
                current_handles,
                current_labels,
                bbox_to_anchor=(1.05, 1),
                loc=2,
                borderaxespad=0.0,
            )
        else:
            ax.get_legend().remove()

        if yscale == "linear":
            plt.yscale(yscale)
        elif yscale == "symlog":
            df_np = np.fabs(df.to_numpy())
            min_abs = np.min(df_np[df_np > 0])
            plt.yscale("symlog", linthresh=min_abs)
        else:
            raise NotImplementedError

        plt.grid(True)
        fig.tight_layout()

        return fig, ax

    def plot_bar(
        self,
        df,
        yscale="linear",
        title="",
        xlabel="",
        ylabel="",
        legend=False,
        figsize=DEFAULT_SIZE,
    ):
        fig, ax = plt.subplots(figsize=figsize)
        df.plot.bar(ax=ax, legend=False)
        plt.grid(True, axis="y")
        locs, labels = plt.xticks()
        plt.xticks(locs, labels, rotation=45)
        ax.set_yscale(yscale)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        if legend:
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        fig.tight_layout()

        return fig, ax

    def plot_scatter(
        self,
        df,
        title="",
        xlabel="",
        ylabel="",
        figsize=DEFAULT_SIZE,
        colour="tab:blue",
        fig=None,
        ax=None,
    ):
        if not ax:
            fig, ax = plt.subplots(figsize=figsize)

        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        df.plot.scatter(x="sd", y="mean", c=colour, ax=ax, s=200, alpha=1.0)

        x_diff = df["sd"].max() - df["sd"].min()
        y_diff = df["mean"].max() - df["mean"].min()

        for i, point in df.iterrows():

            r = np.random.choice([-1, 1])

            ax.text(
                point["sd"] - x_diff * 0.03,
                point["mean"] + r * y_diff * 0.03,
                i,
                fontsize=12,
            )

        plt.grid(True, axis="y")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        x_min = df["sd"].min() - 0.1 * x_diff
        x_max = df["sd"].max() + 0.1 * x_diff
        y_min = df["mean"].min() - 0.1 * y_diff
        y_max = df["mean"].max() + 0.1 * y_diff

        ax.set_xlim(left=x_min, right=x_max)
        ax.set_ylim(bottom=y_min, top=y_max)

        fig.tight_layout()

        return fig, ax
