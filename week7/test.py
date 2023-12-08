# from PIL import Image, ImageDraw, ImageFont
#
# # Function to create an image with the specified letter
# def create_letter_image(letter, image_size=100, font_size=80):
#     # Create a blank image with a white background
#     img = Image.new('RGB', (image_size, image_size), color='white')
#     draw = ImageDraw.Draw(img)
#
#     # Use a font (change the path to a font file on your system if needed)
#     font = ImageFont.truetype("Roboto_regular.ttf", font_size)
#
#     # Get text size to center the letter in the image
#     text_width, text_height = draw.textsize(letter, font=font)
#     position = ((image_size - text_width) // 2, (image_size - text_height) // 2)
#
#     # Draw the letter on the image
#     draw.
#     draw.text(position, letter, fill='green', font=font)
#
#     return img
#
# # Generate an image of the letter 'A' and display it
# letter_image = create_letter_image('A')
# letter_image.show()  # Show the image
# letter_image.save('letter_A.png')  # Save the image as 'letter_A.png'
