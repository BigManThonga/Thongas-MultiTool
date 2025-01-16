import sys
import os
import pygame
from PIL import Image
import tkinter as tk
from tkinter.filedialog import askopenfilename

# Pygame initialization
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Image to ASCII Converter')

# Fonts and colors
font = pygame.font.Font(None, 36)
button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)
text_color = (255, 255, 255)

# ASCII characters used for art
ASCII_CHARS = "@%#*+=-:. "

# Function to resize the image for ASCII conversion
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Function to convert image to grayscale
def grayscale_image(image):
    return image.convert("L")

# Function to map each pixel to an ASCII character
def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 32]  # Divide by 32 to map pixel brightness to an ASCII character
    return ascii_str

# Convert image to ASCII art
def image_to_ascii(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file: {e}")
        return None

    # Convert image to ASCII
    image = resize_image(image)
    grayscale = grayscale_image(image)
    ascii_str = pixels_to_ascii(grayscale)

    # Format the ASCII string
    ascii_art = ""
    width = grayscale.width
    for i in range(0, len(ascii_str), width):
        ascii_art += ascii_str[i:i + width] + "\n"

    return ascii_art

# Function to open file dialog to select image
def select_image_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    root.destroy()
    return file_path

# Function to save ASCII art to a text file
def save_ascii_art(ascii_art, original_path):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    base_name = os.path.basename(original_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join("outputs", f"{name_without_ext}.txt")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {output_path}")
    except Exception as e:
        print(f"Failed to save ASCII art: {e}")

# Load and scale the buttons
button_rect = pygame.Rect(200, 150, 200, 50)
file_select_rect = pygame.Rect(200, 250, 200, 50)

# Main program loop
running = True
image_path = None  # No image selected initially

while running:
    screen.fill((30, 30, 30))  # Dark background color

    # Draw "Convert" button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    # Draw "Select File" button
    if file_select_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, file_select_rect)
    else:
        pygame.draw.rect(screen, button_color, file_select_rect)

    # Button texts
    convert_text = font.render("Convert", True, text_color)
    select_text = font.render("Select File", True, text_color)
    screen.blit(convert_text, (button_rect.x + 50, button_rect.y + 10))
    screen.blit(select_text, (file_select_rect.x + 30, file_select_rect.y + 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if file_select_rect.collidepoint(mouse_pos):
                # Open file dialog to select image
                selected_path = select_image_file()
                if selected_path:
                    image_path = selected_path
                    print(f"Selected image: {image_path}")
            elif button_rect.collidepoint(mouse_pos):
                if image_path:
                    # Convert the selected image to ASCII
                    ascii_art = image_to_ascii(image_path)
                    if ascii_art:
                        print(ascii_art)
                        # Save the ASCII art to a text file
                        save_ascii_art(ascii_art, image_path)
                else:
                    print("Please select an image first.")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
