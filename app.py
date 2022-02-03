from itertools import count
from PIL import Image, ImageDraw, ImageChops
import random
import os
import glob
from config import IMAGES_COUNT, IMAGE_TARGET_SIZE

images_count = int(IMAGES_COUNT)
target_size_px = int(IMAGE_TARGET_SIZE)
scale_factor = 4
image_size_px = target_size_px * scale_factor
image_size = (image_size_px, image_size_px)
image_padding_percent = 10
image_padding_px = int(image_size_px * image_padding_percent / 100)
images_path = 'images/'
images_format = 'png'

def clear_all_images():
    files = glob.glob('{}/*.{}'.format(images_path, images_format))
    if (len(files) > 0):
        print('Started removing {} files from "{}" folder'.format(len(files), images_path))
        for f in files:
            os.remove(f)
        print('Deleted {} images from "{}" folder'.format(len(files), images_path))

def interpolate (start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )

def generate_images():
    for _ in range(images_count):
        image = Image.new(
            mode='RGB', 
            size=image_size, 
            color=get_random_color_tuple()
        )
        image = draw_line(image, 10)
        image = image.resize((target_size_px, target_size_px), resample=Image.ANTIALIAS)
        image.save('{}/{}.{}'.format(images_path, _, images_format))

def generate_gifs():
    frames = [Image.open(image) for image in glob.glob(f"{images_path}/*.{images_format}")]
    frame_one = frames[0]
    frame_one.save(
        "logo.gif", 
        format="GIF", 
        append_images=frames,
        save_all=True, 
        duration=10,
        loop=0
    )

def get_random_color_tuple(len = 3):
    return tuple(random.randint(0, 255) for _ in range(len))

def draw_line(image, lines_count):
    thickness = 1
    points = []
    
    for _ in range(lines_count):
        point = (
            random.randint(image_padding_px, image_size_px - image_padding_px), 
            random.randint(image_padding_px, image_size_px - image_padding_px)
        )
        points.append(point)

    # calculating min and max to center the image
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])


    # centering the image
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)
    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    # draw the points
    p2 = None
    start_color = get_random_color_tuple()
    end_color = get_random_color_tuple()
    
    for i, point in enumerate(points):
        overlay_image = Image.new(
            mode='RGB', 
            size=image_size, 
            color=(0, 0, 0)
        )
        overlay_draw = ImageDraw.Draw(overlay_image)
        p1 = point
        if (i == len(points) - 1):
            p2 = points[0]
        else:
            p2 = points[i + 1]
        thickness += scale_factor
        
        random_points = [
            p1, 
            p2
        ]
        
        xy = (random_points[0], random_points[1])
        color_factor = i / len(points)
        fill = interpolate(start_color, end_color, color_factor)
        overlay_draw.line(
            xy=xy,
            fill=fill,
            width=thickness
        )
        image = ImageChops.add(image, overlay_image)
    
    return image

if __name__ == '__main__':
    clear_all_images()
    generate_images()
    generate_gifs()