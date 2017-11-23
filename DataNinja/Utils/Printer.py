import matplotlib.pyplot as plt

def print_trend(y_data,x_data=None,x_labels=None,new_figure=False):

    if x_data is None:
        x_data = list(range(0, len(y_data)))

    if x_labels is None:
        x_labels = list(range(0, len(y_data)))

    x_ticks = list(range(0, len(y_data)))
    if new_figure:
        plt.figure()
    plt.plot(x_data, y_data)
    plt.xticks(x_ticks, x_labels, rotation='vertical')
    plt.margins(0.2)
    plt.ticklabel_format(axis='y', useOffset=False, style='plain')
    # plt.subplots_adjust(bottom=0.15)
    plt.show()