# appmanager/utils.py

from appium import webdriver
from time import sleep

def test_apk(apk_path):
    # Set up desired capabilities
    desired_caps = {
        "platformName": "Android",
        "deviceName": "emulator-5554",  # Use `adb devices` to find your emulator name
        "app": apk_path,  # Path to the APK file
        "automationName": "UiAutomator2"
    }

    # Create an instance of the Appium driver
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    # Example of interacting with the app
    try:
        # Wait for the app to launch
        sleep(5)

        # Take a screenshot of the first screen
        first_screenshot_path = "path_to_save_screenshots/first_screen.png"
        driver.save_screenshot(first_screenshot_path)

        # Find a button by its ID (example) and click it
        button = driver.find_element_by_id('com.example:id/button_id')
        button.click()

        # Wait for the screen to change
        sleep(5)

        # Take a screenshot of the second screen
        second_screenshot_path = "path_to_save_screenshots/second_screen.png"
        driver.save_screenshot(second_screenshot_path)

        # Capture UI hierarchy
        ui_hierarchy = driver.page_source

        # Determine if the screen changed (this is just a basic example)
        screen_changed = first_screenshot_path != second_screenshot_path  # Simplified

        return {
            "first_screenshot": first_screenshot_path,
            "second_screenshot": second_screenshot_path,
            "ui_hierarchy": ui_hierarchy,
            "screen_changed": screen_changed
        }
    finally:
        # Quit the driver
        driver.quit()
