from yta_multimedia.video.utils import parse_parameter_as_moviepy_clip
from yta_general_utils.image.checker import has_transparency
from yta_general_utils.file.checker import is_valid_image
from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image


class Alphascreen:
    """
    Class to handle images with alphascreen regions and insert
    other images or videos on it.
    """
    image = None
    image_filename: str = None
    top_left: list
    bottom_right: list

    def __init__(self, filename: str):
        if not isinstance(filename, str):
            raise Exception(f'No str "filename" parameter "{filename}" provided.')
        
        if not is_valid_image(filename):
            raise Exception(f'The provided "filename" parameter "{filename}" is not a valid image.')
        
        # TODO: Read the image with transparency
        # C:/Users/dania/Desktop/tmp_greenscreens/google_meet_alpha.png
        image = Image.open(filename)

        if not has_transparency(image):
            raise Exception('The provided image "filename" parameter "{filename}" does not have any alpha channel.')

        self.image_filename = filename
        self.image = image
        alpha_area = self.get_alpha_area(self.image)
        self.top_left = alpha_area['top_left']
        self.bottom_right = alpha_area['bottom_right']

    def insert_image(self, image, duration: float):
        # TODO: Validate 'image' param properly
        video = ImageClip(image, duration = duration)

        return self.insert_video(video)

    def insert_video(self, video):
        """
        This method returns a CompositeVideoClip with the provided
        'video' fitting in the alphascreen area and centered on it
        by applying a mask that let it be seen through that mask.
        """
        video = parse_parameter_as_moviepy_clip(video)

        alphascreen_clip = ImageClip(self.image_filename, duration = video.duration)

        # We resize the video to fit the alphascreen region dimensions
        video = self.make_video_fit_alphascreen_region_size(video)

        # We position it in the center of the alphascreen region
        x = (self.bottom_right[0] + self.top_left[0]) / 2 - video.w / 2
        y = (self.bottom_right[1] + self.top_left[1]) / 2 - video.h / 2
        video = video.set_position((x, y))

        composite_clip = CompositeVideoClip([
            video,
            alphascreen_clip
        ], size = alphascreen_clip.size)

        return composite_clip
    
    def make_video_fit_alphascreen_region_size(self, video):
        """
        This method rescales the provided 'video' to make it fit in
        the alphascreen region. Once it's been rescaled, this video
        should be placed in the center of the alphascreen region.
        """
        video = parse_parameter_as_moviepy_clip(video)

        # We have the alphascreen area corners and video corners
        alphascreen_width = self.bottom_right[0] - self.top_left[0]
        alphascreen_height = self.bottom_right[1] - self.top_left[1]

        # We force 16:9 scale ratio.
        # If we want to keep dimensions correctly, we will increase
        # (or decrease) the dimensions by these values below for each
        # step
        STEP_X = 16 * 2
        STEP_Y = 9 * 2

        # If video is larger than alphascreen area, we need to make it
        # smaller. In any other case, bigger
        if video.w > alphascreen_width and video.h > alphascreen_height:
            STEP_X = -STEP_X
            STEP_Y = -STEP_Y

        do_continue = True
        tmp_size = [video.w, video.h]
        while (do_continue):
            tmp_size = [tmp_size[0] + STEP_X, tmp_size[1] + STEP_Y]

            if STEP_X < 0 and (tmp_size[0] < alphascreen_width or tmp_size[1] < alphascreen_height):
                # The previous step had the right dimensions
                tmp_size[0] += abs(STEP_X)
                tmp_size[1] += abs(STEP_Y)
                do_continue = False
            elif STEP_X > 0 and (tmp_size[0] > alphascreen_width and tmp_size[1] > alphascreen_height):
                # This step is ok
                do_continue = False

        video = video.resize((tmp_size[0], tmp_size[1]))

        return video

    @classmethod
    def get_alpha_area(cls, image):
        """
        This method iterates through the provided image (image
        opened with PIL library Image.open) and returns the 
        'top_left' and 'bottom_right' corners, as [x, y] arrays
        of the alpha area.

        This area is useful to place another resource on that 
        position.

        This method will raise an Exception if the provided 
        'image' does not have any alpha pixel or is not an
        opened image with Image.open().
        """
        # TODO: Refactor this to accept other 'image' type params
        top_left = [99999, 99999]
        bottom_right = [-99999, -99999]

        # TODO: If you can make this loop faster, thank you
        # This loop will iterate over all alpha pixels that would be
        # creating an area similar to a rectangle so we get the
        # corners of that rectangle to be able to place a resource
        # just there to fit the alpha channel and be seen through
        width, height = image.size
        for x in range(width):
            for y in range(height):
                _, _, _, a = image.getpixel((x, y))
                if a == 0:  # Verifica si el canal alfa es 0 (transparente)
                    if x < top_left[0]:
                        top_left[0] = x
                    if y < top_left[1]:
                        top_left[1] = y
                    if x > bottom_right[0]:
                        bottom_right[0] = x
                    if y > bottom_right[1]:
                        bottom_right[1] = y

        if top_left == [99999, 99999] or bottom_right == [-99999, -99999]:
            raise Exception(f'The provided "image" parameter does not have any alpha pixel.') 

        return {
            'top_left': top_left,
            'bottom_right': bottom_right
        }