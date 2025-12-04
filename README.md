# Usage

## Setup
1. Install Google Chrome (or Chrome for Testing) locally.
2. Create and activate a virtual environment (optional but recommended).
3. Install the Python dependencies:
   ```
   pip install selenium webdriver-manager beautifulsoup4 matplotlib numpy pandas seaborn
   ```

## Download leaderboard data
1. Edit `src/scrap.py`:
   - Add any missing games in the `games_paths` dictionary.
   - Add the games you want to scrape to `list_of_games`.
2. Run the scraper:
   ```
   cd src
   python scrap.py
   ```

This opens a Chrome window via Selenium, navigates to each Board Game Arena leaderboard and downloads the “All-time” ranking. Results are stored as CSV files inside `leaderboards/<Game>_full_leaderboard.csv`.

### Troubleshooting
- **ChromeDriver download issues** – `webdriver_manager` downloads the right binary automatically, but it needs internet access and a locally installed Chrome version. If the machine cannot reach Google’s endpoints you will need to download the matching driver manually and place it inside `~/.wdm/drivers/`.
- **Exec format errors / THIRD_PARTY_NOTICES** – if a previous webdriver download cached only notice files, delete the stale folder inside `~/.wdm/drivers/chromedriver/` and re-run the scraper so a fresh executable can be fetched.

## Plot and compare results
`src/analyze_data.py` contains helpers to render smooth histograms of the collected CSV files.

- Generate figures for each game:
  ```
  cd src
  python analyze_data.py
  ```
  (call `plot_all_games()` / `compare_games()` as needed inside the script.)

- Comparison graphics are written to `comparison_results/` while single-game plots live in `results/`.

## Update this README’s gallery
Regenerate the “Results” section after producing plots by running:
```
python update_readme.py
```


# Results
### Azul
**Azul vs Yatzy all elo distribution**
![Azul_vs_Yatzy_all_elo_distribution.png](./comparison_results/Azul_vs_Yatzy_all_elo_distribution.png)
**Azul vs Yatzy elo distribution**
![Azul_vs_Yatzy_elo_distribution.png](./comparison_results/Azul_vs_Yatzy_elo_distribution.png)
### Agricola
**Agricola all elo distribution**
![Agricola_all_elo_distribution.png](./results/Agricola_all_elo_distribution.png)
**Agricola elo distribution**
![Agricola_elo_distribution.png](./results/Agricola_elo_distribution.png)
### ArkNova
**ArkNova all elo distribution**
![ArkNova_all_elo_distribution.png](./results/ArkNova_all_elo_distribution.png)
**ArkNova elo distribution**
![ArkNova_elo_distribution.png](./results/ArkNova_elo_distribution.png)
### Azul
**Azul all elo distribution**
![Azul_all_elo_distribution.png](./results/Azul_all_elo_distribution.png)
**Azul elo distribution**
![Azul_elo_distribution.png](./results/Azul_elo_distribution.png)
### Carcassonne
**Carcassonne all elo distribution**
![Carcassonne_all_elo_distribution.png](./results/Carcassonne_all_elo_distribution.png)
**Carcassonne elo distribution**
![Carcassonne_elo_distribution.png](./results/Carcassonne_elo_distribution.png)
### Catan
**Catan all elo distribution**
![Catan_all_elo_distribution.png](./results/Catan_all_elo_distribution.png)
**Catan elo distribution**
![Catan_elo_distribution.png](./results/Catan_elo_distribution.png)
### Patchwork
**Patchwork all elo distribution**
![Patchwork_all_elo_distribution.png](./results/Patchwork_all_elo_distribution.png)
**Patchwork elo distribution**
![Patchwork_elo_distribution.png](./results/Patchwork_elo_distribution.png)
### Quoridor
**Quoridor all elo distribution**
![Quoridor_all_elo_distribution.png](./results/Quoridor_all_elo_distribution.png)
**Quoridor elo distribution**
![Quoridor_elo_distribution.png](./results/Quoridor_elo_distribution.png)
### RaceForTheGalaxy
**RaceForTheGalaxy all elo distribution**
![RaceForTheGalaxy_all_elo_distribution.png](./results/RaceForTheGalaxy_all_elo_distribution.png)
**RaceForTheGalaxy elo distribution**
![RaceForTheGalaxy_elo_distribution.png](./results/RaceForTheGalaxy_elo_distribution.png)
### SevenWonders
**SevenWondersDuel all elo distribution**
![SevenWondersDuel_all_elo_distribution.png](./results/SevenWondersDuel_all_elo_distribution.png)
**SevenWondersDuel elo distribution**
![SevenWondersDuel_elo_distribution.png](./results/SevenWondersDuel_elo_distribution.png)
**SevenWonders all elo distribution**
![SevenWonders_all_elo_distribution.png](./results/SevenWonders_all_elo_distribution.png)
**SevenWonders elo distribution**
![SevenWonders_elo_distribution.png](./results/SevenWonders_elo_distribution.png)
### SevenWondersDuel
**SevenWondersDuel all elo distribution**
![SevenWondersDuel_all_elo_distribution.png](./results/SevenWondersDuel_all_elo_distribution.png)
**SevenWondersDuel elo distribution**
![SevenWondersDuel_elo_distribution.png](./results/SevenWondersDuel_elo_distribution.png)
### TicketToRide
**TicketToRide all elo distribution**
![TicketToRide_all_elo_distribution.png](./results/TicketToRide_all_elo_distribution.png)
**TicketToRide elo distribution**
![TicketToRide_elo_distribution.png](./results/TicketToRide_elo_distribution.png)
### Wingspan
**Wingspan all elo distribution**
![Wingspan_all_elo_distribution.png](./results/Wingspan_all_elo_distribution.png)
**Wingspan elo distribution**
![Wingspan_elo_distribution.png](./results/Wingspan_elo_distribution.png)
### Yatzy
**Yatzy all elo distribution**
![Yatzy_all_elo_distribution.png](./results/Yatzy_all_elo_distribution.png)
**Yatzy elo distribution**
![Yatzy_elo_distribution.png](./results/Yatzy_elo_distribution.png)
