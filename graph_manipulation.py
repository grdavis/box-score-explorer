import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_manipulation import calc_win_percentage_and_occurrences

def create_winp_weighted_avg_traces(data_column, quarter, trace_color, league_text):
    p_or_q = "P" if league_text == "NHL" else "Q"
    bins, winp, occurs = calc_win_percentage_and_occurrences(data_column)
    indices = list(np.where(np.logical_not(np.isnan(winp[:-1])))[0])
    weighted_avg_num = np.average([winp[i] for i in indices], weights=[occurs[i] for i in indices])
    probs = go.Scatter(
        x = bins[:-1], 
        y = winp[:-1],
        opacity = 0.5,
        mode = 'lines',
        line = dict(color=trace_color),
        name = '%s%s Win %%' % (p_or_q, quarter),
        hovertemplate="margin: %{x}<br>" + p_or_q + quarter + " win probability: %{y}<extra></extra>")
    weighted_avg = go.Scatter(
        x = bins,
        y = [weighted_avg_num]*len(bins),
        name = '%s%s Decided' % (p_or_q, quarter),
        mode = 'lines',
        line = dict(color=trace_color, width=4, dash='dashdot'),
        hovertemplate=p_or_q + quarter + " decidedness: %{y}<extra></extra>")
    occurs_line = go.Scatter(
        x = bins[:-1],
        y = occurs/sum(occurs),
        customdata = occurs,
        mode = 'none',
        fill = 'tozeroy',
        fillcolor = f"rgba{(int(trace_color[1:3], 16), int(trace_color[3:5], 16), int(trace_color[5:7], 16), 0.15)}",
        name = '%s%s Games' % (p_or_q, quarter),
        hovertemplate="margin: %{x}<br>games: %{customdata}<br>share of " + p_or_q + quarter + " games: %{y}<extra></extra>")

    return (probs, weighted_avg, occurs_line)

def final_quarter_trace(data_column, trace_color):
    occurs, bins = np.histogram(data_column, bins = range(min(data_column), max(data_column) + 2))
    occurs_line = go.Scatter(
        x = [0] + list(bins[:-1]),
        y = [0] + list(occurs/sum(occurs)),
        customdata = occurs,
        mode = 'none',
        fill = 'tozeroy',
        fillcolor = f"rgba{(int(trace_color[1:3], 16), int(trace_color[3:5], 16), int(trace_color[5:7], 16), 0.15)}",
        name = 'Final Games',
        hovertemplate="margin: %{x}<br>games: %{customdata}<br>share of game finals: %{y}<extra></extra>")
    return occurs_line

def create_margins_occurences_graphs(league_text, plots, save_path = None, save = False):
    period_or_quarter = "Period" if league_text == "NHL" else "Quarter"
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    final = plots[-1]
    for i in plots[:-1]:
        probs, weighted_avg, occurs_line = create_winp_weighted_avg_traces(i[1], i[0], i[2], league_text)
        fig.add_trace(occurs_line, secondary_y = True)
        fig.add_trace(probs, secondary_y = False)
        fig.add_trace(weighted_avg, secondary_y = False)
    fig.add_trace(final_quarter_trace(final[1], final[2]), secondary_y = True)
    
    fig.update_layout(title = "%s Scoring Margins, Win Probabilities, and 'Decidedness' by End of %s" % (league_text, period_or_quarter),
                     plot_bgcolor='rgba(0,0,0,0)', yaxis_tickformat = '%', yaxis2_tickformat = '%')
    fig.update_yaxes(title_text="Win Percentage", range = [.5, 1], secondary_y = False)
    fig.update_yaxes(title_text="Share of Games (n = %s)" % str(len(plots[0][1])), secondary_y = True)
    fig.update_xaxes(title_text="Scoring Margin", range = [0, max(plots[0][1])])

    if save:
        if save_path == None: 
            print("please provide a save_path")
            exit()
        fig.write_html("%s.html" % save_path)
        
    return fig