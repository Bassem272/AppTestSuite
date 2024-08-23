# from appium import webdriver
# from time import sleep

# from django.conf import settings

# def test_apk(apk_path):
#     # Set up desired capabilities
#     desired_caps = {
#         'platformName': 'Android',
#         'platformVersion': '12.0',  # Set this to match your emulator's Android version
#         'deviceName': 'emulator-5554',  # This is the name of your running emulator
#         'app': apk_path,  # Path to the APK file being tested
#         'automationName': 'UiAutomator2',  # Recommended automation engine for Android
#     }

#     # Create an instance of the Appium driver
#     driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # Use desired_caps directly

#     # Example of interacting with the app
#     try:
#         # Wait for the app to launch
#         sleep(5)

#         # Take a screenshot of the first screen
#         first_screenshot_path = settings.MEDIA_ROOT +"/first_screen.png"
#         driver.save_screenshot(first_screenshot_path)

#         # Find a button by its ID (example) and click it
#         button = driver.find_element_by_id('com.example:id/button_id')
#         button.click()

#         # Wait for the screen to change
#         sleep(5)

#         # Take a screenshot of the second screen
#         second_screenshot_path = settings.MEDIA_ROOT +"/second_screen.png"
#         driver.save_screenshot(second_screenshot_path)

#         # Capture UI hierarchy
#         ui_hierarchy = driver.page_source

#         # Determine if the screen changed (this is just a basic example)
#         screen_changed = first_screenshot_path != second_screenshot_path  # Simplified

#         return {
#             "first_screenshot": first_screenshot_path,
#             "second_screenshot": second_screenshot_path,
#             "ui_hierarchy": ui_hierarchy,
#             "screen_changed": screen_changed
#         }
#     finally:
#         # Quit the driver
#         driver.quit()
# from appium import webdriver
# from appium.options.android import UiAutomator2Options  # Correct options class for Android
# from time import sleep
# from selenium.webdriver.common.by import By  # Import By for locating elements
# import os

# def test_apk(apk_path):
#     # Set up desired capabilities
#     desired_caps = {
#         'platformName': 'Android',
#         'platformVersion': '12.0',  # Set this to match your emulator's Android version
#         'deviceName': 'emulator-5554',  # This is the name of your running emulator
#         'app': apk_path,  # Path to the APK file being tested
#         'automationName': 'UiAutomator2',  # Recommended automation engine for Android
#     }

#     # Convert capabilities to an options instance
#     capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

#     # Create an instance of the Appium driver
#     driver = webdriver.Remote('http://localhost:4723', options=capabilities_options)  # Use options directly

#     # Example of interacting with the app
#     try:
#         # Wait for the app to launch
#         sleep(5)

#         # Ensure the directory for saving screenshots exists
#         screenshot_dir = "path_to_save_screenshots"
#         os.makedirs(screenshot_dir, exist_ok=True)

#         # Take a screenshot of the first screen
#         first_screenshot_path = os.path.join(screenshot_dir, "first_screen.png")
#         driver.save_screenshot(first_screenshot_path)

#         # Find a button by its ID (example) and click it
#         try:
#             button = driver.find_element(By.ID, 'com.example:id/button_id')
#             button.click()
#         except Exception as e:
#             print(f"Error finding or clicking the button: {e}")
#             return {"error": str(e)}

#         # Wait for the screen to change
#         sleep(5)

#         # Take a screenshot of the second screen
#         second_screenshot_path = os.path.join(screenshot_dir, "second_screen.png")
#         driver.save_screenshot(second_screenshot_path)

#         # Capture UI hierarchy
#         ui_hierarchy = driver.page_source

#         # Determine if the screen changed (this is just a basic example)
#         screen_changed = first_screenshot_path != second_screenshot_path  # Simplified

#         return {
#             "first_screenshot": first_screenshot_path,
#             "second_screenshot": second_screenshot_path,
#             "ui_hierarchy": ui_hierarchy,
#             "screen_changed": screen_changed
#         }
#     finally:
#         # Quit the driver
#         driver.quit()

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'android.widget.Button')))

        # Find all buttons on the screen
        buttons = driver.find_elements(By.CLASS_NAME, 'android.widget.Button')

        if not buttons:
            response["error"] = "No buttons found on the screen."
            return response

        # Extract attributes of the first button found
        first_button = buttons[0]
        response["button_id"] = first_button.get_attribute('resourceId')  # Extract ID
        response["button_class"] = first_button.get_attribute('class')    # Extract class name

        # Print extracted attributes for debugging
        print(f"Button ID: {response['button_id']}")
        print(f"Button Class: {response['button_class']}")

        # Take a screenshot of the first screen
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        response["first_screenshot"] = os.path.join(screenshot_dir, "first_screen.png")
        driver.save_screenshot(response["first_screenshot"])

        # Click the button
        first_button.click()

        # Wait for the screen to change
        WebDriverWait(driver, 10).until(EC.staleness_of(first_button))

        # Take a screenshot of the second screen
        response["second_screenshot"] = os.path.join(screenshot_dir, "second_screen.png")
        driver.save_screenshot(response["second_screenshot"])

        # Capture UI hierarchy
        response["ui_hierarchy"] = driver.page_source

        # Determine if the screen changed
        response["screen_changed"] = response["first_screenshot"] != response["second_screenshot"]

    finally:
        # Quit the driver
        driver.quit()

    return response
