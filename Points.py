from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
import time

urls = {
    "https://www.twitch.tv/yourSTREAM": ("Default", "C:\\Users\\YOURUSERNAME\\AppData\\Local\\Google\\Chrome\\NAMEOFYOURCHROMECOPY\\"),
}

def check_stream(driver):
    try:
        driver.find_element(By.CLASS_NAME, "Layout-sc-1xcs6mc-0.ScChannelStatusTextIndicatorMask-sc-qtgrnb-1.dbboLV.mIiJT")
        return True  
    except NoSuchElementException:
        return False  
def visit_url(url, profile_directory, profile_path, options):
    options.add_argument(f"--profile-directory={profile_directory}")
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--headless")
    options.add_argument("--log-level=3")

    while True:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)

        islive = check_stream(driver)

        if not islive:
            print("Not live on", url, "going dormant")
            driver.quit()  
            time.sleep(1800)  
            continue

        print("Streamer is live on", url, "starting to collect points")

        points_timer = 0

        while islive:
            
            if points_timer >= 10:
                points_timer = 0

                try:
                    points = driver.find_element(By.CLASS_NAME, "ScCoreButton-sc-ocjdkq-0.ScCoreButtonSuccess-sc-ocjdkq-5.ibtYyW.kIlsPe")
                    points.click()
                    print("Points collected on", url)
                except NoSuchElementException:
                    print("Points not ready on", url)

            time.sleep(1)

            points_timer += 1

            islive = check_stream(driver)
            if not islive:
                print("Stream has stopped on", url)
                break

        driver.quit()
        print("Browser closed for", url,"going dormant")
        time.sleep(1800) 

threads = []
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

for url, (profile_directory, profile_path) in urls.items():
    thread_options = Options()
    thread_options.add_experimental_option("detach", True)
    thread_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    thread_options.add_experimental_option('useAutomationExtension', False)

    thread = threading.Thread(target=visit_url, args=(url, profile_directory, profile_path, thread_options))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All sites visited Exiting...")