import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Function to calculate the % of all players that have a better ELO
def calculate_percentile_given_elo(df, input_elo):
    better_players = df[df["ELO"] > input_elo]
    percentile = 100 * len(better_players) / len(df)
    return percentile


# Function to find the ELO threshold given a percentile
def calculate_elo_given_percentile(df, input_percentile):
    elo_threshold = np.percentile(df["ELO"], 100 - input_percentile)
    return elo_threshold


def plot_rough(df, percentiles):
    # Plotting the ELO distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df["ELO"], bins=20, color="blue", alpha=0.7, label="ELO Distribution")
    for label, value in percentiles.items():
        plt.axvline(
            x=value, color="red", linestyle="--", label=f"{label} ({value:.2f})"
        )
    plt.xlabel("ELO Rating")
    plt.ylabel("Number of Players")
    plt.title("ELO Distribution of Players")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("./elo_distribution.png")
    plt.show()


def plot_smooth(df, name, show_plots=False):
    elo_starts = [0, 100]
    for elo_start in elo_starts:
        plt.figure(figsize=(12, 6))
        filtered_df = df[df["ELO"] > elo_start]

        sns.kdeplot(
            filtered_df["ELO"],
            color="blue",
            shade=True,
            label="ELO Distribution",
            bw_adjust=0.5,
        )

        # Define different line styles for the percentiles
        line_styles = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (3, 5, 1, 5))]
        # Calculate the percentiles for the ELOs
        percentiles_values = [99.9, 99, 95, 90, 75, 50]
        percentiles = {
            f"Top {round(100-p, 1)}%": round(np.percentile(filtered_df["ELO"], p), 0)
            for p in percentiles_values
        }

        # Plot the percentile thresholds with different line styles
        for (label, elo), ls in zip(percentiles.items(), line_styles):
            plt.axvline(x=elo, color="red", linestyle=ls, label=f"{label} ({elo:.2f})")

        # Setting the x-axis to start at 0 and end at a value slightly higher than the max ELO to center the plot
        plt.xlim(left=elo_start, right=df["ELO"].max() + 50)
        # Setting ticks on the x-axis to be every 50 ELO
        plt.xticks(np.arange(elo_start, df["ELO"].max() + 50, 50))
        plt.xlabel("ELO Rating")
        plt.ylabel("Density")
        if elo_start == 0:
            plt.title(
                f"Smooth ELO Distribution of ALL {name} Players ({len(filtered_df)} players)"
            )
        else:
            plt.title(
                f"Smooth ELO Distribution of {name} Players above {elo_start} ELO ({len(filtered_df)} players)"
            )
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if elo_start == 0:
            plt.savefig(f"../results/{name}_all_elo_distribution.png")
        else:
            plt.savefig(f"../results/{name}_elo_distribution.png")
        if show_plots:
            plt.show()


# def compare_distributions(df1, df2, name1, name2, show_plots=False):
#     elo_starts = [0, 100]
#     for elo_start in elo_starts:
# plt.figure(figsize=(12, 6))

# # Filter the DataFrames
# filtered_df1 = df1[df1["ELO"] > elo_start]
# filtered_df2 = df2[df2["ELO"] > elo_start]

# # Plot the first distribution
# sns.kdeplot(
#     filtered_df1["ELO"],
#     color="blue",
#     shade=True,
#     label=f"{name1} ELO Distribution",
#     bw_adjust=0.5,
# )

# # Plot the second distribution
# sns.kdeplot(
#     filtered_df2["ELO"],
#     color="green",
#     shade=True,
#     label=f"{name2} ELO Distribution",
#     bw_adjust=0.5,
# )

# # Calculate the percentiles for the ELOs
# percentiles_values = [75]
# line_styles = ["-"]
# line_styles2 = ["--"]

# # Calculate and plot percentiles for the first distribution
# percentiles_1 = {
#     f"{name1} Top {round(100-p, 1)}%": round(
#         np.percentile(filtered_df1["ELO"], p), 0
#     )
#     for p in percentiles_values
# }
# for (label, elo), ls in zip(percentiles_1.items(), line_styles):
#     plt.axvline(x=elo, color="darkblue", linestyle=ls, label=f"{label} ({elo})")

# # Calculate and plot percentiles for the second distribution
# percentiles_2 = {
#     f"{name2} Top {round(100-p, 1)}%": round(
#         np.percentile(filtered_df2["ELO"], p), 0
#     )
#     for p in percentiles_values
# }
# for (label, elo), ls in zip(percentiles_2.items(), line_styles2):
#     plt.axvline(
#         x=elo, color="darkgreen", linestyle=ls, label=f"{label} ({elo})"
#     )

# # Set the x-axis and y-axis labels
# plt.xlim(left=elo_start, right=max(df1["ELO"].max(), df2["ELO"].max()) + 50)
# plt.xticks(
#     np.arange(elo_start, max(df1["ELO"].max(), df2["ELO"].max()) + 50, 50)
# )
# plt.xlabel("ELO Rating")
# plt.ylabel("Density")

# # Set the title based on the ELO start
# if elo_start == 0:
#     plt.title(
#         f"Comparison of ALL Players' ELO Distribution: {name1} vs {name2}"
#     )
# else:
#     plt.title(f"Comparison of Players above {elo_start} ELO {name1} vs {name2}")


# if elo_start == 0:
#     plt.savefig(f"../results/{name1}_vs_{name2}_all_elo_distribution.png")
# else:
#     plt.savefig(f"../results/{name1}_vs_{name2}_elo_distribution.png")
# if show_plots:
#     plt.show()
def compare_distributions(df1, df2, name1, name2, show_plots=False):
    elo_starts = [0, 100]
    for elo_start in elo_starts:
        plt.figure(figsize=(12, 6))

        # Filter the DataFrames
        filtered_df1 = df1[df1["ELO"] > elo_start]
        filtered_df2 = df2[df2["ELO"] > elo_start]

        # Plot the first distribution
        sns.kdeplot(
            filtered_df1["ELO"],
            color="blue",
            shade=True,
            label=f"{name1} Distribution",
            bw_adjust=0.5,
        )

        # Plot the second distribution
        sns.kdeplot(
            filtered_df2["ELO"],
            color="green",
            shade=True,
            label=f"{name2} Distribution",
            bw_adjust=0.5,
        )

        plt.legend()

        # Calculate the percentiles for the ELOs for both distributions
        percentiles_values = [75]
        percentiles1 = {
            round(np.percentile(filtered_df1["ELO"], p), 0) for p in percentiles_values
        }
        percentiles2 = {
            round(np.percentile(filtered_df2["ELO"], p), 0) for p in percentiles_values
        }

        # Plot the percentile thresholds for each game
        for elo in percentiles1:
            plt.axvline(
                x=elo,
                color="darkblue",
                linestyle="-",
                label=f"{name1} 75th Percentile ({elo})"
                if elo == list(percentiles1)[0]
                else "",
            )
        for elo in percentiles2:
            plt.axvline(
                x=elo,
                color="darkgreen",
                linestyle="--",
                label=f"{name2} 75th Percentile ({elo})"
                if elo == list(percentiles2)[0]
                else "",
            )

        plt.xlim(
            left=elo_start,
            right=max(filtered_df1["ELO"].max(), filtered_df2["ELO"].max()) + 50,
        )
        plt.xticks(
            np.arange(
                elo_start,
                max(filtered_df1["ELO"].max(), filtered_df2["ELO"].max()) + 50,
                50,
            )
        )
        plt.xlabel("ELO Rating")
        plt.ylabel("Density")
        if elo_start == 0:
            plt.title(
                f"Comparison of ALL Players' ELO Distribution: {name1} vs {name2}"
            )
        else:
            plt.title(f"Comparison of Players above {elo_start} ELO {name1} vs {name2}")

        if elo_start == 0:
            plt.savefig(
                f"../comparison_results/{name1}_vs_{name2}_all_elo_distribution.png"
            )
        else:
            plt.savefig(
                f"../comparison_results/{name1}_vs_{name2}_elo_distribution.png"
            )
        if show_plots:
            plt.show()


def create_game_paths_dict(leaderboards_path):
    games_paths = {}

    # List all csv files in the given directory
    for filename in os.listdir(leaderboards_path):
        if filename.endswith(".csv"):
            # Extract the game name as the first word of the filename
            game_name = filename.split("_")[0]
            # Create a path for the file
            file_path = os.path.join(leaderboards_path, filename)
            # Add to the dictionary
            games_paths[game_name] = file_path

    return games_paths


def plot_all_games():
    # games_paths = {
    #     "Azul": "../leaderboards/azul_leaderboard.csv",
    #     "Quoridor": "../leaderboards/Quoridor_full_leaderboard.csv",
    #     "RaceForTheGalaxy": "../leaderboards/RaceForTheGalaxy_full_leaderboard.csv",
    #     "Yatzy": "../leaderboards/Yatzy_full_leaderboard.csv",
    #     "Patchwork": "../leaderboards/Patchwork_full_leaderboard.csv",
    # }

    games_paths = create_game_paths_dict("../leaderboards/")
    print(games_paths)

    for game in games_paths.keys():
        # Load the CSV data into a DataFrame
        # df = pd.read_csv('')
        df = pd.read_csv(games_paths[game])
        # Example usage of the functions
        elo_input = 700
        percentile_output = calculate_percentile_given_elo(df, elo_input)
        print(f"Percentile of players with ELO > {elo_input}: {percentile_output:.2f}%")
        percent_input = 20
        elo_output = calculate_elo_given_percentile(df, percent_input)
        print(
            f"ELO threshold for the top {percent_input}% of players: {elo_output:.2f}"
        )

        # plot_rough(df, percentiles)
        plot_smooth(df, game, show_plots=False)


def compare_games():
    games_paths = create_game_paths_dict("../leaderboards/")
    print(games_paths)

    game1 = "Azul"
    game2 = "Yatzy"
    df1 = pd.read_csv(games_paths[game1])
    df2 = pd.read_csv(games_paths[game2])
    compare_distributions(df1, df2, game1, game2, show_plots=True)


# plot_all_games()
compare_games()
