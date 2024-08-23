from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

def test_apk(apk_path):
    # Set up desired capabilities
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '12.0',
        'deviceName': 'emulator-5554',
        'app': apk_path,
        'automationName': 'UiAutomator2',
    }

    # Convert capabilities to an options instance
    capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

    # Create an instance of the Appium driver
    driver = webdriver.Remote('http://localhost:4723', options=capabilities_options)

    # Initialize response dictionary
    response = {
        "button_id": None,
        "button_class": None,
        "first_screenshot": None,
        "second_screenshot": None,
        "ui_hierarchy": None,
        "screen_changed": False
    }

    try:
        # Wait for the app to launch
        print("Waiting for the app to launch...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'android.widget.Button')))

        # Find all buttons on the screen
        buttons = driver.find_elements(By.CLASS_NAME, 'android.widget.Button')

        if not buttons:
            response["error"] = "No buttons found on the screen."
            print(response["error"])
            return response

        # Extract attributes of the first button found
        first_button = buttons[0]
        response["button_id"] = first_button.get_attribute('resourceId')  # Extract ID
        response["button_class"] = first_button.get_attribute('class')    # Extract class name

        # Print extracted attributes for debugging
        print(f"Button ID: {response['button_id']}")
        print(f"Button Class: {response['button_class']}")

        # Ensure the directory for saving screenshots exists
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Create a unique timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Take a screenshot of the first screen
        response["first_screenshot"] = os.path.join(screenshot_dir, f"first_screen_{timestamp}.png")
        driver.save_screenshot(response["first_screenshot"])
        print(f"First screenshot saved at: {response['first_screenshot']}")

        # Click the button
        print("Clicking the button...")
        first_button.click()

        # Wait for the screen to change
        print("Waiting for the screen to change...")
        WebDriverWait(driver, 10).until(EC.staleness_of(first_button))

        # Take a screenshot of the second screen
        response["second_screenshot"] = os.path.join(screenshot_dir, f"second_screen_{timestamp}.png")
        driver.save_screenshot(response["second_screenshot"])
        print(f"Second screenshot saved at: {response['second_screenshot']}")

        # Capture UI hierarchy
        response["ui_hierarchy"] = driver.page_source

        # Determine if the screen changed
        response["screen_changed"] = response["first_screenshot"] != response["second_screenshot"]

    except Exception as e:
        response["error"] = str(e)
        print(f"Exception occurred: {e}")

    finally:
        # Quit the driver
        driver.quit()

    return response
