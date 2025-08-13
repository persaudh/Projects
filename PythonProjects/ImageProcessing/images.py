from PIL import Image, ImageFilter

img = Image.open("./astro.jpg")
smaller_img = img
smaller_img.thumbnail((400,400))
smaller_img.save("tumbnail.jpg")