import logging

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.ticker import FormatStrFormatter

sns.set()
sns.set_style("whitegrid")

# general configuration for matplotlib
DEFAULT_SIZE = (15, 8)
DEFAULT_SIZE_SQUARE = (15, 15)

params = {
    "font.family": "serif",
    "legend.fontsize": "large",
    "figure.figsize": DEFAULT_SIZE,
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "large",
    "ytick.labelsize": "large",
}
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

        mask = np.zeros_like(relations)
        mask[np.triu_indices_from(mask, k=shift)] = True

        sns.heatmap(
            relations,
            cmap="RdYlGn",
            mask=mask,
            xticklabels=relations.columns,
            yticklabels=relations.columns,
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
    ):
        fig, ax = plt.subplots(figsize=figsize)

        df.plot(
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            linewidth=2,
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
        plt.grid(True)
        fig.tight_layout()

        return fig, ax

    def plot_bar(
        self, df, yscale="linear", title="", xlabel="", ylabel="", figsize=DEFAULT_SIZE
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
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        fig.tight_layout()

        return fig, ax

    def plot_scatter(
        self,
        df,
        title="",
        xlabel="",
        ylabel="",
        figsize=DEFAULT_SIZE_SQUARE,
        colour="tab:blue",
        fig=None,
        ax=None,
    ):
        if not ax:
            fig, ax = plt.subplots(figsize=figsize)

        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

        df.plot.scatter(x="sd", y="mean", c=colour, ax=ax, s=200, alpha=1.0)

        x_min, x_max = df["sd"].min(), df["sd"].max()
        x_diff = x_max - x_min
        y_min, y_max = df["mean"].min(), df["mean"].max()
        y_diff = y_max - y_min

        for i, point in df.iterrows():
            ax.text(
                point["sd"] - x_diff * 0.03,
                point["mean"] + y_diff * 0.03,
                i,
                fontsize=14,
            )

        plt.grid(True, axis="y")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        axis_max = max(x_max + 0.2 * x_diff, y_max + 0.2 * y_diff)
        x_min = 0.0
        y_min = min(0.0, y_min - 0.2 * y_diff)

        ax.set_xlim(left=x_min, right=axis_max)
        ax.set_ylim(bottom=y_min, top=axis_max)

        fig.tight_layout()

        return fig, ax
