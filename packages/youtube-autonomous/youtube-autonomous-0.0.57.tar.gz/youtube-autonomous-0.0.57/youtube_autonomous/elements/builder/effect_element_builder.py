from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import EffectPremade
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip
from typing import Union


class EffectElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'EFFECT' content.
    """
    @classmethod
    def effect_name_to_class(cls, effect_name: str):
        """
        Returns the effect class according to the provided 'effect_name'
        parameter. It will return None if no effect found for that
        'effect_name' parameter.
        """
        valid_name = EffectPremade.get_valid_name(effect_name)

        if not valid_name:
            raise Exception(f'The provided effect premade name "{effect_name}" is not valid. The valid ones are: {EffectPremade.get_all_names_as_str()}')
        
        return EffectPremade[valid_name].value
    
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        effect_name = enhancement.keywords
        effect = cls.effect_name_to_class(effect_name)

        return effect

        # TODO: I need to send the segment, because the effect will
        # be aplied into the segment but with the enhancement
        # parameters
        return cls.build_custom_from_effect_name(effect_name, segment.video_clip, **extra_parameters)

    @classmethod
    def build_custom_from_effect_name(cls, effect_name: str, video_or_audio: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip], **parameters):
        # TODO: Apply VideoFileClip, AudioFileClip and the others
        ElementParameterValidator.validate_string_mandatory_parameter(effect_name, effect_name)
        # TODO: Validate keywords is a valid effect key name

        # TODO: Apply the effect in the provided 'video_or_audio'
        effect = cls.effect_name_to_class(effect_name)
        if not effect:
            raise Exception(f'No effect found for the "effect_name" parameter "{effect_name}" provided.')

        return effect(video_or_audio).apply(**parameters)

    @classmethod
    def build_custom(cls, effect, video_or_audio: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip], **parameters):
        # TODO: Make the effects implement an abstract class named
        # 'Effect' to be able to detect them as subclasses
        return effect(video_or_audio).apply(**parameters)
    
    @classmethod
    def get_building_parameters(cls, element: dict, parameters_to_ignore: list[str], not_extra_parameters: list[str]):
        """
        This method extracts the parameters needed for building the effect
        that exist in the 'extra_params' field of the provided 'element'
        dict, replaces the ones in 'not_extra_parameters' with the ones
        in the main 'element' dict and, finally, keeps the only parameters
        needed to build the effect and returns them. This means that only
        the 'mandatory' or 'optional' parameters to build the effect, if
        existing, will be returned extracted from where it was specified.
        """
        effect_name = element.keywords
        
        ElementParameterValidator.validate_effect_name(effect_name)

        effect_class = cls.effect_name_to_class(effect_name)
        parameters = ElementBuilder.extract_extra_params(element, effect_class.apply, parameters_to_ignore)

        # TODO: What if not extra parameter does not exist in main (?)
        for not_extra_parameter in not_extra_parameters:
            parameters[not_extra_parameter] = element.get(not_extra_parameter)
        
        actual_parameters = ParameterObtainer.get_parameters_from_method(effect_class.apply)

        # We keep only 'mandatory' or 'optional' parameters removing useless
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return parameters