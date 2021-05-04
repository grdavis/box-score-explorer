import pandas as pd
from graph_manipulation import create_margins_occurences_graphs

nhl_data = pd.read_csv("Data/nhl_cleaned.csv")
nhl_plots = [("1", nhl_data.P1M, "#1f77b4"), ("2", nhl_data.P2M, "#ff7f0e"), ("F", nhl_data.FinalMargin, "#e377c2")]

nba_data = pd.read_csv("Data/nba_cleaned.csv")
nba_plots = [("1", nba_data.Q1M, "#1f77b4"), ("2", nba_data.Q2M, "#ff7f0e"), ("3", nba_data.Q3M, "#2ca02c"), ("F", nba_data.FinalMargin, "#e377c2")]

nfl_data = pd.read_csv("Data/nfl_cleaned.csv")
nfl_plots = [("1", nfl_data.Q1M, "#1f77b4"), ("2", nfl_data.Q2M, "#ff7f0e"), ("3", nfl_data.Q3M, "#2ca02c"), ("F", nfl_data.FinalMargin, "#e377c2")]

nhl_graph = create_margins_occurences_graphs('NHL', nhl_plots, save = True, save_path = "Outputs/nhl_summary")
nba_graph = create_margins_occurences_graphs('NBA', nba_plots, save = True, save_path = "Outputs/nba_summary")
nfl_graph = create_margins_occurences_graphs('NFL', nfl_plots, save = True, save_path = "Outputs/nfl_summary")