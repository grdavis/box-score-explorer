import numpy as np

def calc_win_percentage_and_occurrences(data_column):
    #chances of winning at different margins of leads
    counts, bins = np.histogram(data_column, bins = range(min(data_column), max(data_column) + 2))
    counts, bins = list(counts), list(bins)
    new_counts, new_bins = [], bins[bins.index(0):]
    for new_bin in new_bins:
        if new_bin == 0: 
            new_counts.append(.5)
        elif -new_bin in bins:
            if counts[bins.index(new_bin)] + counts[bins.index(-new_bin)] == 0: new_counts.append(np.nan)
            else: new_counts.append(counts[bins.index(new_bin)]/(counts[bins.index(new_bin)] + counts[bins.index(-new_bin)]))
        else: 
        	if bins.index(new_bin) > (len(counts) - 1): new_counts.append(np.nan)
        	elif counts[bins.index(new_bin)] == 0: new_counts.append(np.nan)
        	else: new_counts.append(1)
    sizes = [counts[bins.index(0)]] + [(counts[bins.index(i)] + counts[bins.index(-i)]) if -i in bins else counts[bins.index(i)] for i in new_bins[1:-1]]
    
    return (new_bins, new_counts, sizes)