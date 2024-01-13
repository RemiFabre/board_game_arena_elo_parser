# First, let's write a code snippet to read the CSV file and calculate the ELO distribution along with the percentile thresholds.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Function to calculate the % of all players that have a better ELO
def calculate_percentile_given_elo(input_elo):
    better_players = df[df["ELO"] > input_elo]
    percentile = 100 * len(better_players) / len(df)
    return percentile


# Function to find the ELO threshold given a percentile
def calculate_elo_given_percentile(input_percentile):
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


def plot_smooth(df, name):
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
            plt.savefig(f"./{name}_all_smooth_elo_distribution.png")
        else:
            plt.savefig(f"./{name}_smooth_elo_distribution.png")
        plt.show()


games_paths = {
    "Azul": "azul_leaderboard.csv",
    "Quoridor": "Quoridor_full_leaderboard.csv",
    "RaceForTheGalaxy": "RaceForTheGalaxy_full_leaderboard.csv",
    "Yatzy": "Yatzy_full_leaderboard.csv",
}


for game in games_paths.keys():
    # Load the CSV data into a DataFrame
    # df = pd.read_csv('')
    df = pd.read_csv(games_paths[game])
    # Example usage of the functions
    elo_input = 716
    percentile_output = calculate_percentile_given_elo(elo_input)
    print(f"Percentile of players with ELO > {elo_input}: {percentile_output:.2f}%")
    percent_input = 20
    elo_output = calculate_elo_given_percentile(percent_input)
    print(f"ELO threshold for the top {percent_input}% of players: {elo_output:.2f}")

    # plot_rough(df, percentiles)
    plot_smooth(df, game)
