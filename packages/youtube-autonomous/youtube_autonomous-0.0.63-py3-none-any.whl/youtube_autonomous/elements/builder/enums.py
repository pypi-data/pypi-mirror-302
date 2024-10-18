from yta_multimedia.video.generation.google.google_search import GoogleSearch
from yta_multimedia.video.generation.google.youtube_search import YoutubeSearch
from yta_multimedia.video.generation.manim.classes.text.text_triplets_manim_animation import TextTripletsManimAnimation
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from yta_multimedia.video.generation.manim.classes.text.simple_text_manim_animation import SimpleTextManimAnimation
from yta_multimedia.video.generation.manim.classes.text.rain_of_words_manim_animation import RainOfWordsManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_static_manim_animation import MagazineTextStaticManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_is_written_manim_animation import MagazineTextIsWrittenManimAnimation
from yta_multimedia.video.edition.effect.color.black_and_white_video_effect import BlackAndWhiteVideoEffect
from yta_multimedia.video.edition.effect.moviepy.blink_video_effect import BlinkVideoEffect
from yta_multimedia.video.edition.effect.moviepy.blur_video_effect import BlurVideoEffect
from yta_multimedia.video.edition.effect.speed.change_speed_effect import ChangeSpeedVideoEffect
from yta_multimedia.video.edition.effect.open_close.fade_in_video_effect import FadeInVideoEffect
from yta_multimedia.video.edition.effect.open_close.fade_out_video_effect import FadeOutVideoEffect
from yta_multimedia.video.edition.effect.display.flip_horizontally_video_effect import FlipHorizontallyVideoEffect
from yta_multimedia.video.edition.effect.display.flip_vertically_video_effect import FlipVerticallyVideoEffect
from yta_multimedia.video.edition.effect.display.multiplied_video_effect import MultipliedVideoEffect
from yta_multimedia.video.edition.effect.custom.photo_video_effect import PhotoVideoEffect
from yta_multimedia.video.edition.effect.speed.reversed_video_effect import ReversedVideoEffect
from yta_multimedia.video.edition.effect.custom.sad_moment_video_effect import SadMomentVideoEffect
from yta_multimedia.video.edition.effect.display.scroll_video_effect import ScrollVideoEffect
from yta_multimedia.video.edition.effect.zoom.linear_zoom_video_effect import LinearZoomVideoEffect
from yta_multimedia.video.edition.effect.speed.stopmotion_video_effect import StopMotionVideoEffect
from yta_multimedia.video.edition.effect.moviepy.position.slide_random_position_moviepy_effect import SlideRandomPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static.circles_at_position_moviepy_effect import CirclesAtPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static.stay_at_position_moviey_effect import StayAtPositionMoviepyEffect
from yta_general_utils.programming.enum import YTAEnum as Enum


class Premade(Enum):
    """
    Premade enum class to make our multimedia premades available for the
    app by matching the corresponding class with an Enum variable that is
    used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    GOOGLE_SEARCH = GoogleSearch
    YOUTUBE_SEARCH = YoutubeSearch

class TextPremade(Enum):
    """
    Text premade enum class to make our multimedia text premades available
    for the app by matching the corresponding class with an Enum variable
    that is used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    TRIPLETS = TextTripletsManimAnimation
    WORD_BY_WORD = TextWordByWordManimAnimation
    SIMPLE = SimpleTextManimAnimation
    RAIN_OF_WORDS = RainOfWordsManimAnimation
    MAGAZINE_STATIC = MagazineTextStaticManimAnimation
    MAGAZINE_IS_WRITTEN = MagazineTextIsWrittenManimAnimation

class EffectPremade(Enum):
    """
    Effect premade enum class to make our multimedia effects available for
    the app by matching the corresponding class with an Enum variable that
    is used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    BLACK_AND_WHITE = BlackAndWhiteVideoEffect
    BLINK = BlinkVideoEffect
    BLUR = BlurVideoEffect
    CHANGE_SPEED = ChangeSpeedVideoEffect
    FADE_IN = FadeInVideoEffect
    FADE_OUT = FadeOutVideoEffect
    FLIP_HORIZONTALLY = FlipHorizontallyVideoEffect
    FLIP_VERTICALLY = FlipVerticallyVideoEffect
    MULTIPLIED = MultipliedVideoEffect
    PHOTO = PhotoVideoEffect
    REVERSED = ReversedVideoEffect
    SAD_MOMENT = SadMomentVideoEffect
    SCROLL = ScrollVideoEffect
    LINEAR_ZOOM = LinearZoomVideoEffect
    STOP_MOTION = StopMotionVideoEffect
    SLIDE_RANDOM = SlideRandomPositionMoviepyEffect
    # Positioned
    CIRCLES_AT_POSITION = CirclesAtPositionMoviepyEffect
    STAY_AT_POSITION = StayAtPositionMoviepyEffect
