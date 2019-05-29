#!/usr/bin/env python3
"""
Plotting functions
"""
import matplotlib.pyplot as plt
from math import pi             # For radar graph.

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

def radar(angles, categories, values, ylim, yticks):
    """
    Helps plot a radar graph.

    Args:
        angles (list): Angles to plot spines of radar graph. Should be in
            radians. Spans from [0, 2*pi].
        categories (list): Categories to write on each spine.
        values (list): Values to plot for each spine.
        ylim (int): How big to make the circle.
        yticks (list(int)): The labels mark on each spine.
    """
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles, categories, color='black', size=10)
    
    
    # Make sure the xtick labels don't overlap the graph.
    for label,rot in zip(ax.get_xticklabels(),angles):
        
        # All labels on left side are right aligned.
        # All labels on right side are left aligned.
        if rot <= pi / 2 or rot >= 3 * pi / 2:
            label.set_horizontalalignment("left")
        else:
            label.set_horizontalalignment("right")


    # Draw ylabels
    yticks_labels = [str(tick) for tick in yticks]
    ax.set_rlabel_position(0)
    plt.yticks(yticks, yticks_labels, color="black", size=7)
    plt.ylim(0, ylim)
    
    # Angles/Values double first.
    angles_first_doubled = angles + angles[:1]
    values_first_doubled = values + values[:1]
    

    # Plot data
    ax.plot(angles_first_doubled, values_first_doubled, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles_first_doubled, values_first_doubled, 'b', alpha=0.1)

def plot_radar(categories, values, num_yticks=5):
    """
    Helps plot a radar graph.

    Args:
        categories (list): Categories to write on each spine.
        values (list): Values to plot for each spine.
        num_yticks (int): Optional. Defaults to 5. The number of ticks to show
            on each spine.
    """
    N = len(categories)
    
    max_value = int(max(values))
    step_size = int(max_value / num_yticks)
    
    yticks = list(range(step_size, max_value , step_size))
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]

    radar(angles, categories, values, max_value + step_size, yticks)
    
def plot_radar_df(df, column_names, xlabels=None):
    """
    Helps plot a radar graph.

    Args:
        df (pandas.DataFrame): The data to be accessed to be plotted.
        column_names (list(str)): The names of the columns to be plotted on the
            graph.
        xlabels (dict(str->str)): Maps each column name to human readable label.
            Optional. When not specified, the column names are used as the
            labels.
    """
    # Get sums.
    sums = df.sum()

    # Grab only the qualities we want.
    sums = sums[column_names]

    # Convert it to a dict.
    sums = sums.to_dict()

    # Pull column names and values.
    if xlabels is not None:
        names = list(sums.keys())
        categories = [xlabels[name] for name in names]
    else:
        categories = list(sums.keys())
    
    values = list(sums.values())

    # Plot it.
    plot_radar(categories, values)
