import base64
import os
import signal
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def test_apk(apk_path):
    # Set up desired capabilities
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '12.0',
        'deviceName': 'emulator-5554',
        'app': apk_path,
        'automationName': 'UiAutomator2',
        'noReset': True,  # To avoid reinstalling the app on every run
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
        "screen_changed": False,
        "video_path": None
    }

    try:
        # Start video recording
        print("Starting video recording...")
        driver.start_recording_screen()

        # Wait for the app to launch
        print("Waiting for the app to launch...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'android.widget.Button')))

          # Get the package name of the currently running app
        response["package_name"] = driver.capabilities['appPackage']
        print(f"Package Name: {response['package_name']}")

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

        # Ensure the directory for saving screenshots and video exists
        screenshot_dir = os.path.join("D:\AppTestSuite\media", "screenshots")
        videos_dir = os.path.join("D:\AppTestSuite\media", "videos")
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)

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
        # Stop video recording and save the file
        video_raw = driver.stop_recording_screen()
        video_data = base64.b64decode(video_raw)
        video_path = os.path.join(videos_dir, f"video_recording_{timestamp}.mp4")
        with open(video_path, "wb") as video_file:
            video_file.write(video_data)

        response["video_path"] = video_path
        print(f"Video recording saved at: {response['video_path']}")
        # Close the app after the test
        print("Closing the app...")
        driver.terminate_app(response['package_name'])
        # Quit the driver to close the Appium session
        driver.quit()
        print("Driver quit successfully.")

        # Optionally, kill any lingering processes related to the emulator
        # os.system('adb -s emulator-5554 emu kill')  # This will kill the emulator

    return response
