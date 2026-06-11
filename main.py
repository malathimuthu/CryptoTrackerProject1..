from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import time

# Chrome options
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

data = []

try:
    print("Opening CoinMarketCap...")
    driver.get("https://coinmarketcap.com/")

    wait = WebDriverWait(driver, 30)

    # Wait for table rows
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    # Extra safe wait (important for dynamic data)
    time.sleep(60)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    print("Rows Found:", len(rows))

    if len(rows) == 0:
        print("❌ No data loaded. Try again.")
    else:
        for row in rows[:10]:   # TOP 10 ONLY

            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 8:
                try:
                    coin_name = cols[2].text.split("\n")[0]
                    price = cols[3].text
                    change_24h = cols[4].text
                    market_cap = cols[7].text

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    data.append([
                        timestamp,
                        coin_name,
                        price,
                        change_24h,
                        market_cap
                    ])

                    print(f"{coin_name} | {price}")

                except:
                    pass

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()

# SAVE CSV (always runs)
with open("crypto_data.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Timestamp",
        "Coin",
        "Price",
        "24h Change",
        "Market Cap"
    ])

    writer.writerows(data)

print("\nCSV Saved Successfully!")
print("Total Coins Saved:", len(data))