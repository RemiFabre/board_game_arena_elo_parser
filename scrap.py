import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

games_paths = {
    "Azul": "https://en.boardgamearena.com/gamepanel?game=azul",
    "Quoridor": "https://boardgamearena.com/gamepanel?game=quoridor",
    "RaceForTheGalaxy": "https://boardgamearena.com/gamepanel?game=raceforthegalaxy",
    "Yatzy": "https://boardgamearena.com/gamepanel?game=yatzy",
}

game = "Yatzy"


def scrape_azul_leaderboard():
    try:
        # Setup WebDriver
        print("Setting up WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # Open the website
        print("Opening the website...")
        driver.get(games_paths[game])

        # Wait for the page to load
        print("Waiting for the page to load...")
        time.sleep(2)  # Adjust sleep time as needed

        # Dismiss any potential popups (e.g., cookie consent)
        try:
            print("Looking for popups to dismiss...")
            popup = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'cc-window')]//a[contains(@class, 'cc-btn')]",
                    )
                )  # This XPath is an example; adjust based on the actual popup
            )
            popup.click()
            print("Popup dismissed.")
        except TimeoutException:
            print("No popup found or not clickable.")

        # Scroll the dropdown into view
        print("Scrolling to the dropdown...")
        dropdown = driver.find_element(
            By.XPATH, "//div[contains(text(), 'Current Season')]"
        )
        driver.execute_script("arguments[0].scrollIntoView();", dropdown)
        time.sleep(1)  # Give time for any lazy-loaded elements

        # Click the dropdown using JavaScript
        print("Clicking the dropdown using JavaScript...")
        driver.execute_script("arguments[0].click();", dropdown)

        # Wait for the "All-time" option to be visible and clickable
        print("Waiting for the 'All-time' option to appear...")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'All-time')]")
            )
        ).click()

        print("Clicked All-time!")
        time.sleep(1.0)

        # Scrape data until a condition is met
        player_data = []
        prev_first_player = None
        while True:
            # Parse page content with BeautifulSoup
            print("Parsing page content...")
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # print("Finding the 'Next' button...")
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Next')]")
                )
            )

            # Find player data
            # print("Finding player data...")
            found_10 = False
            first_loop = True
            consecutive_errors = 0
            while not found_10:  # Sometimes it didn't load well
                if consecutive_errors > 4:
                    print(
                        "WARNING: Too many consecutive errors, this is only OK if it's the last page"
                    )

                if not first_loop:
                    time.sleep(0.01)
                first_loop = False
                players = soup.find_all(
                    "div", class_="bga-ranking-entry"
                )  # Container for each player
                if len(players) == 10:
                    # Check if the first player is the same as the previous iteration
                    first_player = (
                        players[0].find("a", class_="playername").text.strip()
                    )
                    if first_player != prev_first_player:
                        found_10 = True
                    else:
                        print("WARNING: duplicate view, waiting for refresh...")
                        consecutive_errors += 1
                else:
                    print("WARNING: no 10 players found")
                    consecutive_errors += 1

            for player in players:
                # print("Reading player data...")

                # Find the player's name, which is inside an 'a' tag with class 'playername'
                name_tag = player.find("a", class_="playername")
                name = name_tag.text.strip() if name_tag else "Name not found"
                # print(f"Player name: {name}")

                # Find the ELO rating, which is in a 'div' tag with class 'bga-elo-label'
                elo_tag = player.find("div", class_="bga-elo-label")
                elo = elo_tag.text.strip() if elo_tag else "ELO not found"
                # print(f"ELO: {elo}")
                player_data.append([name, int(elo)])

            # print("Clicking the 'Next' button using JavaScript...")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(0.01)  # just in case
    except Exception as e:
        print(e)
    finally:
        print("Remove duplicates (keeping the highest ELO if names are the same)...")
        unique_players = {}
        anomalies = 0

        for name, elo in player_data:
            if name not in unique_players or elo > unique_players[name]:
                if name in unique_players:  # If the name is already in, it's an anomaly
                    anomalies += 1
                unique_players[name] = elo

        # Sort by ELO in decreasing order
        sorted_players = sorted(
            unique_players.items(), key=lambda item: item[1], reverse=True
        )

        # Convert back to list of lists
        sorted_player_data = [[name, elo] for name, elo in sorted_players]

        print(f"Anomalies found: {anomalies}")

        csv_file_name = f"{game}_full_leaderboard.csv"
        print(f"Writing to file {csv_file_name}")

        with open(csv_file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ELO"])
            for name, elo in sorted_player_data:
                writer.writerow([name, elo])

        # Close the WebDriver
        print("Finished, sleeping for ever...")
        time.sleep(100000)
        print("Closing WebDriver...")
        driver.quit()


scrape_azul_leaderboard()
