from PIL import Image, ImageDraw
im = Image.open("output.png")
d = ImageDraw.Draw(im)

top = (1594, 71)
left = (200, 225)
right = (300, 325)

line_color = (0, 0, 255)

d.line([top, left, right, top], fill=line_color, width=2)

im.save("drawn.png")
