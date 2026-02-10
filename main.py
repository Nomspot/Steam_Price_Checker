from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading


STEAM_WEBSITE = "https://store.steampowered.com/app/"

def get_game_price(game_id):
    # Initialize the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--blink-settings=imagesEnabled=false") # Disable image loading to speed up page load times
    options.add_argument("--autoplay-policy=user-gesture-required") # Disable autoplay of videos to speed up page load times
    driver = webdriver.Chrome(options=options)

    print(f"Checking price for game ID: {game_id}...")
    print("Please wait while we fetch the price information...")
    print("This may take a few seconds...")

    # Create event object for stopping the dots thread
    stop_dots = threading.Event()

    # Create and start the thread for the dots animation
    t = threading.Thread(target=dots, args=(stop_dots,))
    t.start()

    try:
        # Navigate to steam game page
        driver.get(STEAM_WEBSITE + game_id)

        # Wait for a price element to be present on the page
        wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
    
        if wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='age_gate']"))):
            # If the age gate is present, set the dob to 2000 and click the "View Page" button to bypass it
            driver.find_element(By.XPATH, "//select[@id='ageYear']").send_keys("2000")
            view_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='view_product_page_btn']")))
            view_page_button.click()

        # Wait for the price elements to be present on the page -> for all vesrsions avalable to buy
        versions_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='game_area_purchase_game']")))

        # After finding all the versions for the element -> Wait for the dots thread to finish using 'join'
        stop_dots.set()
        t.join()
        
        print("\033c", end="") # Clear console after the dots animation is done using ANSI escape code (works on most terminals)

        # Through each of the founded versions that are availbe to buy -> extract the price and title of the game
        for element in versions_elements:
            try:
                if element.find_elements(By.XPATH, ".//div[@class='game_purchase_price price' and @data-price-final]"):
                    price = element.find_element(By.XPATH, ".//div[@class='game_purchase_price price' and @data-price-final]").text
                    title = element.find_element(By.XPATH, ".//h2[@class='title']").text
                    if title.startswith("Buy "):
                        title = title[4:]  # remove the first 4 chars "Buy " from the title
                    elif title.startswith("Pre-Purchase "):
                        title = title[13:]  # remove the first 13 chars "Pre-Purchase " from the title
                    print(f"Current price for '{title}' is: {price}")
            except Exception as e:
                print("Error while extracting price - ", e)

    except TimeoutException:
        print("Error while extracting price.")
    finally:
        # Close the browser to free up resources
        driver.quit()

def dots(stop):
    while not stop.is_set():
        print(".", end="", flush=True) # Print a dot without a newline and flush the output buffer to ensure it appears immediately
        if stop.wait(1): # Blocks for 1 second, but returns immediately if 'stop' is set
            break

if __name__ == "__main__":
    print("Welcome to the Steam Game Price Checker!")
    print("Please enter the Steam game store ID to get the current price.")
    game_id = input()

    get_game_price(game_id)
