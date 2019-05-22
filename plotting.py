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
