#!/usr/bin/env python3
"""
Plotting functions
"""
import matplotlib.pyplot as plt

def histogram(df, column_name, title, xlabel, ylabel):
    """
    Makes a histogram of the data.

    Args:
        df (pandas.DataFrame): All of the data.
        column_name (str): The specific data to use for the plot.
        title (str): The title of the plot.
        xlabel (str): The xlabel of the plot.
        ylabel (str): The ylabel of the plot.
    """
    # Get the data.
    column = df[column_name]
    ax = plt.gca()
    column.hist(ax=ax, alpha=0.9, color='blue')

    # Handle title and labels.
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def histograms(column_name, original, filtered, title, xlabel, ylabel):
    """
    Plots two histograms side by side.

    Args:
        column_name (str): The specific data to use for the plot.
        original (pandas.DataFrame): All of the data including outliers.
        filtered (pandas.DataFrame): All of the data without outliers.
        title (str): The title of the plot.
        xlabel (str): The xlabel of the plot.
        ylabel (str): The ylabel of the plot.
    """
    # Get the data.
    orig_column = original[column_name]
    filt_column = filtered[column_name]

    # Start a subplot.
    _, (ax1, ax2) = plt.subplots(1, 2)

    # Plot the data with outliers.
    orig_column.hist(ax=ax1, alpha=0.9, color='blue')
    ax1.set_title('Original {title} Histogram'.format(title=title))
    ax1.set(xlabel=xlabel, ylabel=ylabel)

    # Plot the data without outliers.
    filt_column.hist(ax=ax2, alpha=0.9, color='blue')
    ax2.set_title('Filtered {title} Histogram'.format(title=title))
    ax2.set(xlabel=xlabel, ylabel=ylabel)

def graph_labels(title, xlabel=None, ylabel=None):
    """
    Helps write title and axis labels.

    Args:
        title (str): The title of the plot.
        xlabel (str): The xlabel of the plot.
        ylabel (str): The ylabel of the plot.
    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def pie_chart(percentages, column_name, yes_label, no_label, title):
    """
    Helps plot a pie chart for yes or no data.

    Args:
        percentages (pandas.DataFrame): All of the data averaged.
        column_name (str): The specific data to use for the plot.
        yes_label (str): The label for the yes portion of the chart.
        no_label (str): The label for the no portion of the chart.
        title (str): The title of the plot.
    """
    yes_percentage = percentages[column_name]
    no_percentage = 1 - yes_percentage

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = yes_label, no_label
    sizes = [yes_percentage, no_percentage]

    # Explode the Yes.
    explode = (0.1, 0)

    ax = plt.gca()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    plt.title(title)
