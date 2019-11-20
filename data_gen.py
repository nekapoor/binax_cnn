from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import csv

### THIS SHOULD BE ALL OF THE REQUIRED DATA NEEDED IN ORDER TO DYNAMICALLY GENERATE TRAINING DATA ###
BINAX_NOW_PACKAGE_PIL_IMAGE = Image.open('BinaxPackage.png')
BINAX_PACKAGE_IMAGE_WIDTH, BINAX_PACKAGE_IMAGE_HEIGHT = BINAX_NOW_PACKAGE_PIL_IMAGE.size
BINAX_PACKAGE_WIDTH = 64 # mm
BINAX_PACKAGE_HEIGHT = 76 # mm
BINAX_PACKAGE_DIST_TO_STRIP_FROM_Y = 24. # mm (first guess was 28 mm)
BINAX_PACKAGE_DIST_TO_STRIP_FROM_X = 26.5 # mm (first guess was 28 mm)
BINAX_WIDTH = 6 # mm
BINAX_HEIGHT = 14. # mm
LINE_HEIGHT = 0.6 # mm
CL_HEIGHT_POSITION = 5 # relative to top, in mm
TL1_HEIGHT_POSITION = 7 # relative to top
TL2_HEIGHT_POSITION = 9 # relative to top
#DISTANCE_BETWEEN_LINES = 2. # mm
### END REQUIRED DATA NEEDED TO DYNAMICALLY GENERATE TRAINING DATA

IMAGE_WIDTH = (BINAX_WIDTH * 1.0 / BINAX_PACKAGE_WIDTH) * BINAX_PACKAGE_IMAGE_WIDTH # in px
HEIGHT_TO_WIDTH_RATIO = BINAX_HEIGHT / BINAX_WIDTH
IMAGE_HEIGHT = HEIGHT_TO_WIDTH_RATIO * IMAGE_WIDTH

STRIP_TOP_LEFT_POS_X = (BINAX_PACKAGE_DIST_TO_STRIP_FROM_X / BINAX_PACKAGE_WIDTH) * BINAX_PACKAGE_IMAGE_WIDTH
STRIP_TOP_LEFT_POS_Y = (BINAX_PACKAGE_DIST_TO_STRIP_FROM_Y / BINAX_PACKAGE_HEIGHT) * BINAX_PACKAGE_IMAGE_HEIGHT

CROP_TOP_LEFT_X = 21 # mm
CROP_TOP_LEFT_Y = 20 # mm
BOTTOM_RIGHT_X = 36 # mm
BOTTOM_RIGHT_Y = 42 # mm

CROP_TOP_LEFT_IMAGE_POS_X = (CROP_TOP_LEFT_X / BINAX_PACKAGE_WIDTH) * BINAX_PACKAGE_IMAGE_WIDTH
CROP_TOP_LEFT_IMAGE_POS_Y = (CROP_TOP_LEFT_Y / BINAX_PACKAGE_HEIGHT) * BINAX_PACKAGE_IMAGE_HEIGHT
CROP_BOTTOM_RIGHT_IMAGE_POS_X = (BOTTOM_RIGHT_X / BINAX_PACKAGE_WIDTH) * BINAX_PACKAGE_IMAGE_WIDTH
CROP_BOTTOM_RIGHT_IMAGE_POS_Y = (BOTTOM_RIGHT_Y / BINAX_PACKAGE_HEIGHT) * BINAX_PACKAGE_IMAGE_HEIGHT

CL_POSITION_TO_HEIGHT_RATIO = CL_HEIGHT_POSITION / BINAX_HEIGHT
TL1_POSITION_TO_HEIGHT_RATIO = TL1_HEIGHT_POSITION / BINAX_HEIGHT
TL2_POSITION_TO_HEIGHT_RATIO = TL2_HEIGHT_POSITION / BINAX_HEIGHT

CL_POSITION_MIDDLE = CL_POSITION_TO_HEIGHT_RATIO * IMAGE_HEIGHT
CL_POSITION_TOP = CL_POSITION_MIDDLE - ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
CL_POSITION_BOTTOM = CL_POSITION_TOP + ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
CL_POSITION_COORDINATES = (0, CL_POSITION_TOP, IMAGE_WIDTH, CL_POSITION_BOTTOM)

TL1_POSITION_MIDDLE = TL1_POSITION_TO_HEIGHT_RATIO * IMAGE_HEIGHT
TL1_POSITION_TOP = TL1_POSITION_MIDDLE - ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
TL1_POSITION_BOTTOM = TL1_POSITION_TOP + ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
TL1_POSITION_COORDINATES = (0, TL1_POSITION_TOP, IMAGE_WIDTH, TL1_POSITION_BOTTOM)

TL2_POSITION_MIDDLE = TL2_POSITION_TO_HEIGHT_RATIO * IMAGE_HEIGHT
TL2_POSITION_TOP = TL2_POSITION_MIDDLE - ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
TL2_POSITION_BOTTOM = TL2_POSITION_TOP + ((LINE_HEIGHT / 2) / BINAX_HEIGHT) * IMAGE_HEIGHT
TL2_POSITION_COORDINATES = (0, TL2_POSITION_TOP, IMAGE_WIDTH, TL2_POSITION_BOTTOM)

STRIP_DIMENSIONS=(int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
CL_POSITION = CL_POSITION_COORDINATES
TL1_POSITION = TL1_POSITION_COORDINATES
TL2_POSITION = TL2_POSITION_COORDINATES

DEFAULT_BACKGROUND_COLOR = (250, 250, 250) # I picked 230, 230, 230 instead of 255, 255, 255 to better represent background color of strip in real life settings
DEFAULT_CONTROL_COLOR=(255, 0, 0)
DEFAULT_TL1_COLOR=(255, 0, 0)
DEFAULT_TL2_COLOR=(255, 0, 10)

def draw_binax(
        control_color=DEFAULT_CONTROL_COLOR,
        tl_color=DEFAULT_TL1_COLOR,
        t2_color=DEFAULT_TL2_COLOR,
        output_name='pil_text.png',
        plus_minus_offset_value=1,
        pixel_offset_value=0):

    strip = Image.new('RGB', STRIP_DIMENSIONS, color = DEFAULT_BACKGROUND_COLOR)
    draw_line(strip, CL_POSITION, control_color)
    draw_line(strip, TL1_POSITION, tl_color)
    draw_line(strip, TL2_POSITION, t2_color)
    final_strip = strip.filter(ImageFilter.GaussianBlur(radius = 2))
    BINAX_NOW_PACKAGE_PIL_IMAGE.paste(final_strip, (int(STRIP_TOP_LEFT_POS_X), int(STRIP_TOP_LEFT_POS_Y)))
    BINAX_NOW_PACKAGE_PIL_IMAGE.save(output_name) # this is the full package with the strip on it

    ### CROPPING SECTION OF THIS METHOD ###
    # now let's crop this to be just the portion we want with these defaults
    top_left_x = CROP_TOP_LEFT_IMAGE_POS_X + plus_minus_offset_value*pixel_offset_value
    top_left_y = CROP_TOP_LEFT_IMAGE_POS_Y + plus_minus_offset_value*pixel_offset_value
    bottom_right_x = CROP_BOTTOM_RIGHT_IMAGE_POS_X + plus_minus_offset_value*pixel_offset_value
    bottom_right_y = CROP_BOTTOM_RIGHT_IMAGE_POS_Y + plus_minus_offset_value*pixel_offset_value

    full_image = Image.open(output_name)
    cropped_image = full_image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    cropped_image.save(output_name)

def draw_line(pil_image, position, color):
    line = ImageDraw.Draw(pil_image)
    line.rectangle(position, fill=color)

def generate_filename(label, sample, directory="data", ext="png"):
    filename = directory + "/" + str(label) + "/" + str(sample) + "_" + str(label) + "." + ext
    return filename

def get_random_color(color_min, color_max):
    color = random.randrange(color_min, color_max, 1)
    return (color, color, color)

def get_colors(label):
    if label == 0:
        cl_color_min = 0
        cl_color_max = 251
        tl1_color_min = 251
        tl1_color_max = 256
        tl2_color_min = 251
        tl2_color_max = 256
    elif label == 1:
        cl_color_min = 0
        cl_color_max = 251
        tl1_color_min = 0
        tl1_color_max = 251
        tl2_color_min = 251
        tl2_color_max = 256
    elif label == 2:
        cl_color_min = 0
        cl_color_max = 251
        tl1_color_min = 251
        tl1_color_max = 256
        tl2_color_min = 0
        tl2_color_max = 251
    elif label == 3:
        cl_color_min = 0
        cl_color_max = 251
        tl1_color_min = 0
        tl1_color_max = 251
        tl2_color_min = 0
        tl2_color_max = 251
    elif label == 4:
        cl_color_min = 251
        cl_color_max = 256
        tl1_color_min = 0
        tl1_color_max = 251
        tl2_color_min = 0
        tl2_color_max = 251
    cl_color = get_random_color(cl_color_min, cl_color_max)
    tl1_color = get_random_color(tl1_color_min, tl1_color_max)
    tl2_color = get_random_color(tl2_color_min, tl2_color_max)
    return (cl_color, tl1_color, tl2_color)

"""
    0:  control line
    1:  control line + malarial strain 1
    2:  control line + malarial strain 2
    3:  control line + malarial strain 1 + malarial strain 2
    4:  malarial strain 1 + malarial strain 2
"""
def generate_data(label, sample_count = 1000, test_data = False):
    for i in range(sample_count):
        cl_color, tl1_color, tl2_color = get_colors(label)
        filename = generate_filename(label, i)

        # generate image
        draw_binax(cl_color, tl1_color, tl2_color, filename)


def generate_csv():
    #data/label/instance_label.png
    with open("image_data.csv", "wt") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['id', 'label'])
        for label in range(5):
            for instance in range(4000):
                image_name = 'data/' + str(label) + '/' + str(instance) + '_' + str(label) + '.png'
                filewriter.writerow([image_name, str(label)])
