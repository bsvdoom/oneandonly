import time
import pyautogui
import numpy as np
import easyocr
import pygame
import torch


def capture_top_right_corner():
    screen_width, screen_height = pyautogui.size()
    capture_width = screen_width // 8  # 1/4th of the screen width
    capture_height = screen_height // 8  # 1/4th of the screen height

    while True:
        try:
            screenshot = pyautogui.screenshot(region=(screen_width - capture_width, 0, capture_width, capture_height))
            yield screenshot
            time.sleep(1)
        except KeyboardInterrupt:
            break


def extract_numbers(image):
    # Convert PIL image to grayscale
    grayscale_image = image.convert('L')

    # Convert grayscale image to NumPy array
    np_image = np.array(grayscale_image)

    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR
    results = reader.readtext(np_image)

    # Extract numbers
    numbers = ' '.join(result[1] for result in results)

    return numbers


def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


if __name__ == "__main__":
    print("Capturing top right corner of the screen. Press Ctrl+C to stop.")
    capture_generator = capture_top_right_corner()
    sound_file = "iamtheoneandonly.wav"
    already_played = False
    try:
        for i, screenshot in enumerate(capture_generator, start=1):
            # Extract numbers from the image
            numbers = extract_numbers(screenshot)

            # Print the extracted numbers
            print(f"Numbers in screenshot {i}:\n{numbers}")

            splitted = numbers.split(' ')
            if len(splitted) in [2, 3, 4] and splitted[0] == '2':  # Check conditions
                print("Logging message: Conditions met")
                if not already_played:
                    play_sound(sound_file)
                    already_played = True
            else:
                print("Conditions not met")
                print(splitted)
                print(len(splitted))
                print(numbers)



    except KeyboardInterrupt:
        print("\nCapture stopped.")