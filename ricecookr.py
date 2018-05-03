#!/usr/bin/python
"""
Sikana's content is organized as follow:
- There is a top level set of categories (e.g. Health, Nature, Art, ...)
- Each category has programs (e.g. "Learn how to save a life", "Epidemics", ...)
- Each program has chapters
- Finally, each chapter has contents like videos, images, or PDF files.
"""
import sys
import yaml
from enum import Enum
from ricecooker.classes import nodes, questions, files
from ricecooker.classes.nodes import ChannelNode
from ricecooker.classes.licenses import get_license
from ricecooker.exceptions import UnknownContentKindError, UnknownFileTypeError, UnknownQuestionTypeError, raise_for_invalid_channel

from le_utils.constants import licenses, languages
from sikana_api import *


### Global variables

# Reading API credentials from parameters.yml
with open("parameters.yml", "r") as f:
    parameters = yaml.load(f)

# Sikana's API access
SIKANA_CLIENT_ID = parameters["api"]["client_id"]
SIKANA_SECRET = parameters["api"]["secret"]

BASE_URL = "https://www.sikana.tv"


def construct_channel(**kwargs):
    """
    Constructs a Kolibri channel for given language
    """

    # Channel language
    if "language_code" in kwargs:
        language_code = kwargs["language_code"]
    else:
        language_code = "en"

    channel = ChannelNode(
        source_domain = "sikana.tv",
        source_id = "sikana-channel-" + language_code,
        title = "Sikana " + language_code.upper(),
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
    for key, cat in categories["categories"].items():
        print("#### CATEGORY: {}".format(cat["name"]))
        category_node = nodes.TopicNode( # category node
            source_id = cat["name"],
            title = cat["localizedName"]
        )
        node.add_child(category_node)

        # Getting programs belonging to this category from Sikana API
        programs = sikana_api.get_programs(language_code, cat["name"])

        for prog in programs:
            print("### PROGRAM: {}".format(programs[prog]["name"]))
            program_node = nodes.TopicNode( # program node
                source_id = programs[prog]["nameCanonical"],
                title = programs[prog]["name"],
                description = programs[prog].get("description"),
                thumbnail = programs[prog].get("image"),
            )
            category_node.add_child(program_node)

            # Getting program details from Sikana API
            program = sikana_api.get_program(language_code, programs[prog]["nameCanonical"])

            for chap in program["listChaptersVideos"]:
                print("## CHAPTER: {}. {}".format(program["listChaptersVideos"][chap]["infos"]["id"], program["listChaptersVideos"][chap]["infos"]["name"]))
                chapter_node = nodes.TopicNode( # chapter node
                    source_id = str(program["listChaptersVideos"][chap]["infos"]["id"]),
                    title = program["listChaptersVideos"][chap]["infos"]["name"],
                )
                program_node.add_child(chapter_node)

                # For each video in this chapter
                if "videos" in program["listChaptersVideos"][chap]:
                    for v in program["listChaptersVideos"][chap]["videos"]:
                        # Getting video details from Sikana API
                        video = sikana_api.get_video(language_code, v['nameCanonical'])

                        print("# VIDEO: {}".format(video["video"]["title"]))

                        # If no description, we use an empty string
                        try:
                            description = video["video"]["description"]
                        except KeyError:
                            description = ""

                        video_node = nodes.VideoNode(
                            source_id = v["nameCanonical"],
                            title = video["video"]["title"],
                            description = description,
                            derive_thumbnail = False, # video-specific data
                            license = get_license(licenses.CC_BY_NC_ND, copyright_holder="Sikana Education"),
                            thumbnail = "https://img.youtube.com/vi/{}/maxresdefault.jpg".format(video["video"]["youtube_id"]),
                        )
                        chapter_node.add_child(video_node)
                        video_node.add_file(files.YouTubeVideoFile(youtube_id=video["video"]["youtube_id"]))

                        # For each subtitle of this video
                        for sub in video["subtitles"]:
                            code = video["subtitles"][sub]["code"] if video["subtitles"][sub]["code"] != "pt-br" else "pt"

                            sub_file = files.SubtitleFile(
                                path = BASE_URL + video["subtitles"][sub]["fileUrl"],
                                language = languages.getlang(code).code,
                            )
                            video_node.add_file(sub_file)

    return node
