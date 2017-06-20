#!/usr/bin/python
"""
Sikana's content is organized as follow:
- There is top level set of categories (e.g. Health, Nature, Art, ...)
- Each category has programs (e.g. "Learn how to save a life", "Epidemics", ...)
- Each program has chapters
- Finally, each chapter has contents like videos, images, or PDF files.
"""
import sys
import yaml
from enum import Enum
from ricecooker.classes.nodes import ChannelNode
from ricecooker.classes.licenses import get_license
from le_utils.constants import licenses
from sikana_api import *

from ricecooker.classes import nodes, questions, files
from ricecooker.classes.licenses import get_license
from ricecooker.exceptions import UnknownContentKindError, UnknownFileTypeError, UnknownQuestionTypeError, raise_for_invalid_channel
from le_utils.constants import content_kinds,file_formats, format_presets, licenses, exercises, languages
from pressurecooker.encodings import get_base64_encoding

from pprint import pprint


### Global variables

# Reading API credentials from parameters.yml
with open('parameters.yml', 'r') as f:
    parameters = yaml.load(f)

# Sikana's API access
SIKANA_CLIENT_ID = parameters["api"]["client_id"]
SIKANA_SECRET = parameters["api"]["secret"]



def construct_channel(**kwargs):
    """
    Constructs a Kolibri channel for given language
    """

    # Channel language
    if 'language_code' in kwargs:
        language_code = kwargs["language_code"]
    else:
        language_code = 'en'

    channel = ChannelNode(
        source_domain = "sikana.tv",
        source_id = "sikana-channel-"+language_code,
        title = "Sikana " + language_code,
        description = "Sikana is an NGO aiming at producing educative videos to share practical knowledge and skills.",
        thumbnail = "./sikana_logo.png"
    )

    _build_tree(channel, language_code) # Filling the channel with Sikana content
    raise_for_invalid_channel(channel)  # Raising exceptions

    return channel


def _build_tree(node, language_code):
    """
    Builds the content tree with Sikana content
    using Sikana API
    """

    # Building an access to Sikana API
    sikana_api = SikanaApi(
        SIKANA_CLIENT_ID,
        SIKANA_SECRET
    )

    # Taking categories from Sikana API
    categories = sikana_api.get_categories(language_code)

    # Adding categories to tree
    for cat in categories['categories']:
        category_node = nodes.TopicNode( # category node
            source_id=cat['name'],
            title=cat['localizedName']
        )
        node.add_child(category_node)

        # Getting programs belonging to this category from Sikana API
        programs = sikana_api.get_programs(language_code, cat['name'])

        for prog in programs:
            program_node = nodes.TopicNode( # program node
                source_id=programs[prog]["nameCanonical"],
                title=programs[prog]["name"],
                description=programs[prog].get("description"),
                thumbnail=programs[prog].get("image"),
            )
            category_node.add_child(program_node)

            # Getting program details from Sikana API
            program = sikana_api.get_program(language_code, programs[prog]['nameCanonical'])

            for chap in program['listChaptersVideos']:
                chapter_node = nodes.TopicNode( # chapter node
                    source_id=str(program['listChaptersVideos'][chap]['infos']['id']),
                    title=program['listChaptersVideos'][chap]['infos']['name'],
                )
                program_node.add_child(chapter_node)
                chapter_tree = program['listChaptersVideos'][chap].get("children", [])

                # For each video in this chapter
                # for v in chap['videos']:
                #     # Getting video details from Sikana API
                #     video = sikana_api.get_video(language_code, v['nameCanonical'])
                #     child_node = nodes.VideoNode(
                #         source_id=v['video']["id"],
                #         title=v['video']["title"],
                #         description=v['video']['description'],
                #         derive_thumbnail=False, # video-specific data
                #         thumbnail=v['video'].get('thumbnail'),
                #     )
                    # todo: if youtube addfile youtube else addfile from iguane

    return node
