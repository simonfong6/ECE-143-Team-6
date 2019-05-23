"""
Plotting functions
"""
import matplotlib.pyplot as plt

def histogram(df, column_name, title, xlabel, ylabel):
    column = df[column_name]
    ax = plt.gca()
    column.hist(ax=ax, alpha=0.9, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def histograms(column_name, original, filtered, title, xlabel, ylabel):
    orig_column = original[column_name]
    filt_column = filtered[column_name]

    _, (ax1, ax2) = plt.subplots(1, 2)

    orig_column.hist(ax=ax1, alpha=0.9, color='blue')
    ax1.set_title('Original {title} Histogram'.format(title=title))
    ax1.set(xlabel=xlabel, ylabel=ylabel)

    filt_column.hist(ax=ax2, alpha=0.9, color='blue')
    ax2.set_title('Filtered {title} Histogram'.format(title=title))
    ax2.set(xlabel=xlabel, ylabel=ylabel)

def graph_labels(title, xlabel=None, ylabel=None):
    """
    Helps write title and axis labels.g
    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def pie_chart(percentages, column_name, yes_label, no_label, title):
    """
    Helps plot a pie chart for yes or no data.
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
