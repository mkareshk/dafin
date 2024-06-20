import logging

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

# Set seaborn as default
sns.set()

# Set seaborn style
sns.set_style("whitegrid")

# Define default sizes for plots
DEFAULT_SIZE = (15, 8)
DEFAULT_SIZE_SQUARE = (15, 15)

# Configuration for matplotlib aesthetics
params = {
    "font.family": "serif",
    "legend.fontsize": "large",
    "figure.figsize": DEFAULT_SIZE,
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "large",
    "ytick.labelsize": "large",
}

# Apply the configuration
pylab.rcParams.update(params)


class Plot:
    def __init__(self):

        # Set up logging for this class using the module's name
        self.logger = logging.getLogger(__name__)

    def plot_box(
        self, df, title="", xlabel="", ylabel="", figsize=DEFAULT_SIZE, yscale="symlog"
    ):
        """
        Plot a box plot for the given DataFrame.

        Parameters:
        - df (pd.DataFrame): Input data.
        - title (str, optional): Title for the box plot. Defaults to an empty string.
        - xlabel (str, optional): Label for the x-axis. Defaults to an empty string.
        - ylabel (str, optional): Label for the y-axis. Defaults to an empty string.
        - figsize (tuple, optional): Dimensions for the plot. Default is DEFAULT_SIZE.
        - yscale (str, optional): The scale for the y-axis. Default is "symlog".

        Returns:
        - fig (matplotlib.figure.Figure): Figure object.
        - ax (matplotlib.axes._subplots.AxesSubplot): Axes object.

        >>> import pandas as pd  # assuming a mock dataframe for doctest
        >>> df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
        >>> instance = Plot()  # Assuming the class name is 'Plot'
        >>> fig, ax = instance.plot_box(df, title="Box plot of A", xlabel="A")
        """

        fig, ax = plt.subplots(figsize=figsize)

        # Plot the box plot
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

        # Set y-scale
        linthresh = 0.001 if yscale != "linear" else None
        ax.set_yscale(yscale, linthresh=linthresh)

        # Adjust x-axis labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        # Set grid and adjust layout
        ax.yaxis.grid(True)
        fig.tight_layout()

        return fig, ax

    def plot_heatmap(
        self, df, relation_type, title="", annotate=True, figsize=DEFAULT_SIZE
    ):
        """
        Plot a heatmap based on the relation type specified.

        Parameters:
        - df (pd.DataFrame): Input data.
        - relation_type (str): Type of relation to visualize. Supports 'corr' for correlation and 'cov' for covariance.
        - title (str, optional): Title of the heatmap. Defaults to an empty string.
        - annotate (bool, optional): Flag to determine if the heatmap should be annotated. Default is True.
        - figsize (tuple, optional): Dimensions for the heatmap. Default is DEFAULT_SIZE.

        Returns:
        - fig (matplotlib.figure.Figure): Figure object.
        - ax (matplotlib.axes._subplots.AxesSubplot): Axes object.

        Raises:
        - NotImplementedError: If the relation type provided is not 'corr' or 'cov'.

        >>> import pandas as pd  # assuming a mock dataframe for doctest
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [2, 3, 4]})
        >>> instance = Plot()  # Assuming the class name is 'Plot'
        >>> fig, ax = instance.plot_heatmap(df, relation_type="corr", title="Heatmap of Correlation")
        """

        fig, ax = plt.subplots(figsize=figsize)

        # Determine the type of relation and set appropriate parameters
        if relation_type == "corr":
            relations = df.corr()
            annot_fmt = "0.2f"
            vmin, vmax = -1, 1
        elif relation_type == "cov":
            relations = df.cov()
            annot_fmt = "1.1g"
            vmin, vmax = relations.min().min(), relations.max().max()
        else:
            raise NotImplementedError(f"Unsupported relation type: {relation_type}")

        # Set mask for heatmap
        mask = np.zeros_like(relations)
        mask[np.triu_indices_from(mask, k=1)] = True

        # Plot heatmap
        sns.heatmap(
            relations,
            cmap="RdYlGn",
            mask=mask,
            annot=annotate,
            fmt=annot_fmt,
            annot_kws={"fontsize": 14},
            vmin=vmin,
            vmax=vmax,
            ax=ax,
            xticklabels=relations.columns,
            yticklabels=relations.columns,
        )

        # Adjust x and y ticks
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

        # Set title
        ax.set_title(title)

        # Adjust layout
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
        """
        Plot a trend graph using data from the provided DataFrame.

        Parameters:
        - df (pd.DataFrame): Data to be plotted.
        - title (str, optional): Title of the graph. Default is an empty string.
        - xlabel (str, optional): Label for the x-axis. Default is an empty string.
        - ylabel (str, optional): Label for the y-axis. Default is an empty string.
        - figsize (tuple, optional): Dimensions for the figure. Default is DEFAULT_SIZE.
        - alpha (float, optional): Transparency of the lines. Default is 1.0.
        - legend (bool, optional): Flag to determine if a legend should be shown. Default is True.
        - marker (str, optional): Marker style. Default is 'o'.
        - yscale (str, optional): Y-axis scale. Default is 'linear'. Supports 'linear' and 'symlog'.

        Returns:
        - fig (matplotlib.figure.Figure): Figure object.
        - ax (matplotlib.axes._subplots.AxesSubplot): Axes object.

        Raises:
        - NotImplementedError: If the yscale provided is not 'linear' or 'symlog'.

        >>> import pandas as pd  # assuming a mock dataframe for doctest
        >>> df = pd.DataFrame({"A": [1, 2, 3]})
        >>> instance = Plot()  # Assuming the class name is 'Plot'
        >>> fig, ax = instance.plot_trend(df, title="Trend Plot", xlabel="Index", ylabel="Value")
        """

        fig, ax = plt.subplots(figsize=figsize)

        # Plot the data
        df.plot(
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            linewidth=1.5,
            alpha=alpha,
            ax=ax,
            marker=marker,
        )

        # Handle the legend
        if legend:
            ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        else:
            ax.get_legend().remove()

        # Handle yscale settings
        if yscale == "linear":
            ax.set_yscale(yscale)
        elif yscale == "symlog":
            df_np = np.fabs(df.to_numpy())
            min_abs = np.min(df_np[df_np > 0])
            ax.set_yscale("symlog", linthresh=min_abs)
        else:
            raise NotImplementedError(f"Unsupported yscale: {yscale}")

        # Set grid and adjust layout
        ax.grid(True)
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
        """
        Plots a bar graph using the data from the given DataFrame.

        Parameters:
        - df (pd.DataFrame): Data to be plotted.
        - yscale (str, optional): Y-axis scale. Default is "linear".
        - title (str, optional): Title of the graph. Default is an empty string.
        - xlabel (str, optional): Label for x-axis. Default is an empty string.
        - ylabel (str, optional): Label for y-axis. Default is an empty string.
        - legend (bool, optional): Flag to determine if a legend should be shown. Default is False.
        - figsize (tuple, optional): Dimensions for the figure. Default is DEFAULT_SIZE.

        Returns:
        - fig (matplotlib.figure.Figure): Figure object.
        - ax (matplotlib.axes._subplots.AxesSubplot): Axes object.

        >>> import pandas as pd  # assuming a mock dataframe for doctest
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> instance = Plot()  # Assuming the class name is 'Plot'
        >>> fig, ax = instance.plot_bar(df, title="Bar Plot", xlabel="Index", ylabel="Value")
        """

        fig, ax = plt.subplots(figsize=figsize)
        df.plot.bar(ax=ax, legend=legend)
        ax.grid(True, axis="y")
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df.index, rotation=45)
        ax.set_yscale(yscale)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        if legend:
            ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)

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
        """
        Plot a scatter graph of given dataframe values with labels.

        Parameters:
        - df (pd.DataFrame): DataFrame containing columns 'sd' and 'mean' for plotting.
        - title (str): Title of the graph. Default is an empty string.
        - xlabel (str): Label for x-axis. Default is an empty string.
        - ylabel (str): Label for y-axis. Default is an empty string.
        - figsize (tuple): Figure size. Default is DEFAULT_SIZE.
        - colour (str): Color of scatter points. Default is "tab:blue".
        - fig (matplotlib.figure.Figure, optional): Figure object if provided, else will create a new one.
        - ax (matplotlib.axes._subplots.AxesSubplot, optional): Axes object if provided, else will create a new one.

        Returns:
        - fig (matplotlib.figure.Figure): Figure object.
        - ax (matplotlib.axes._subplots.AxesSubplot): Axes object.

        >>> import pandas as pd  # assuming a mock dataframe for doctest
        >>> df = pd.DataFrame({"sd": [1, 2, 3], "mean": [2, 3, 1]})
        >>> instance = SomeClass()
        >>> fig, ax = instance.plot_scatter(df, title="Test", xlabel="SD", ylabel="Mean")
        """

        # Create a new figure and axes if not provided
        if not ax:
            fig, ax = plt.subplots(figsize=figsize)

        # Set major formatter for x and y axes
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        # Scatter plot
        df.plot.scatter(x="sd", y="mean", c=colour, ax=ax, s=200, alpha=1.0)

        x_diff = df["sd"].max() - df["sd"].min()
        y_diff = df["mean"].max() - df["mean"].min()

        # Label each point with its index
        for i, point in df.iterrows():
            r = np.random.choice([-1, 1])
            ax.text(
                point["sd"] - x_diff * 0.03,
                point["mean"] + r * y_diff * 0.03,
                i,
                fontsize=12,
            )

        # Grid, labels, and title
        plt.grid(True, axis="y")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        # Adjusting plot limits
        ax.set_xlim(
            left=df["sd"].min() - 0.1 * x_diff, right=df["sd"].max() + 0.1 * x_diff
        )
        ax.set_ylim(
            bottom=df["mean"].min() - 0.1 * y_diff, top=df["mean"].max() + 0.1 * y_diff
        )

        # Adjust layout
        fig.tight_layout()

        return fig, ax
