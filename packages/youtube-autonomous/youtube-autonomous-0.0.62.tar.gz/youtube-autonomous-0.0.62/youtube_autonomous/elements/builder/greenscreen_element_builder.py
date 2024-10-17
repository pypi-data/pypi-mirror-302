from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from yta_multimedia.greenscreen.custom.image_greenscreen import ImageGreenscreen
from yta_multimedia.greenscreen.custom.video_greenscreen import VideoGreenscreen
from yta_general_utils.file.checker import file_exists, file_is_video_file, file_is_image_file
from yta_general_utils.checker.url import is_google_drive_url
from yta_general_utils.downloader.google_drive import download_file_from_google_drive
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip
from typing import Union


class GreenscreenElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'GREENSCREEN' content.
    """
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        filename = enhancement.filename
        url = enhancement.url

        if not url and not filename:
            # TODO: Can this happen (?)
            raise Exception('No "url" nor "filename" provided and at least one is needed.')

        if url and not filename:
            # Download the file from url and use as filename
            if not is_google_drive_url(url):
                raise Exception(f'The provided "url" parameter "{url}" is not a valid Google Drive url.')
            
            filename = download_file_from_google_drive(url)

        # Priority is filename
        if not file_exists(filename):
            raise Exception(f'The provided "filename" parameter "{filename}" file does not exist.')
        
        if not file_is_video_file(filename) and not file_is_image_file(filename):
            raise Exception(f'The provided "filename" parameter "{filename}" is not a valid image nor video.')

        # Here we have the file, so treat it as image or video
        if file_is_image_file(filename):
            greenscreen = ImageGreenscreen(filename)
        elif file_is_video_file(filename):
            greenscreen = VideoGreenscreen(filename)
        else:
            raise Exception(f'The "filename" file "{filename}" is not a valid image nor video file.')
            
        # I return the greenscreen object to be used in the other class 
        # to wrap and build the whole clip we need to wrap with greenscreen
        return greenscreen

    @classmethod
    def build(cls, video: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip]):
        """
        Basic example to test that the building process and
        the class are working correctly.

        TODO: Remove this in the future when 'custom' is 
        working perfectly.
        """
        return ImageGreenscreen('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing')

        return ImageGreenscreen('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing').from_video_to_video(video)
        # return VideoGreenscreen('https://drive.google.com/file/d/1hL677Q87jn-_y5vqSwev3lir_dCYRQwS/view?usp=sharing').apply()