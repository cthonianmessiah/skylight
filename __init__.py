# Copyright © 2024 by Gregory Dow and available under the MIT License. (see LICENSE.txt)

# NOT AN ENDORSEMENT BY NASA
# Credit for external sky and Moon textures downloaded by this addon goes to:
# NASA's Scientific Visualization Studio
#   Visualizer
#     Ernie Wright (USRA) [Lead]
#   Scientists
#     Noah Petro (NASA/GSFC) [Lead]
#     John Keller (NASA/GSFC)
#   Producer
#     David Ladd (USRA) [Lead]
# https://svs.gsfc.nasa.gov/
#
# Credit for the DE421 SPICE kernel used for ephemeris calculation goes to:
# Dr. William Folkner (SSD/JPL)
#
# This addon's use of NASA imagery and data does not require licensing in the United States:
# https://www.nasa.gov/nasa-brand-center/images-and-media/
# Per the terms stated above, this addon does not include use of NASA logos.
# The credit attribution above is *NOT* intended to claim or imply any endorsement by NASA
# of the content of this addon. None of the people credited above were involved in creating
# or reviewing this Blender addon.

# Credit for ephemeris calculation in Python goes to the Skyfield module by Brandon Rhodes.
# https://rhodesmill.org/skyfield/
# Available under the MIT License: https://github.com/skyfielders/python-skyfield/blob/master/LICENSE

assert  __name__ != '__main__', "This script is for registering an addon and can't be run directly."

bl_info = {
    "name": "Skylight Environment Builder",
    "description": "Build an accurate sky using real astronomical data.",
    "author": "Gregory Dow",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Tools > Skylight", # TODO: Validate this actually works
    "warning": "Requires installing Skyfield module and downloading texture data from NASA.",
    "doc_url": "TBD", # TODO
    "tracker_url": "TBD", # TODO
    "support": "COMMUNITY",
    "category": "Lighting"
}

import sys

reload_detected = 'bpy' in locals()
if reload_detected:
    if __name__ in sys.modules:
        del sys.modules[__name__]

    dotted = __name__ + '.'
    for name in tuple(sys.modules):
        if name.startswith(dotted):
            del sys.modules[name]

import bpy

from .src import dependencies, utils

from .src.operators.SKYLIGHT_preferences import SKYLIGHT_preferences
from .src.operators.SKYLIGHT_PT_missing_dependency_warning import SKYLIGHT_PT_missing_dependency_warning
from .src.operators.SKYLIGHT_OT_install_skyfield import SKYLIGHT_OT_install_skyfield
from .src.operators.SKYLIGHT_OT_download_sky import SKYLIGHT_OT_download_sky
from .src.operators.SKYLIGHT_OT_download_moon import SKYLIGHT_OT_download_moon
from .src.operators.SKYLIGHT_OT_download_de421 import SKYLIGHT_OT_download_de421
from .src.operators.SKYLIGHT_OT_rebuild_world import SKYLIGHT_OT_rebuild_world
from .src.operators.SKYLIGHT_OT_update_world import SKYLIGHT_OT_update_world
from .src.operators.SKYLIGHT_PT_main import SKYLIGHT_PT_main


def register():
    dependencies.update()
    utils.align_preferences()
    [utils.make_registered(x)
        for x in [SKYLIGHT_OT_install_skyfield,
                  SKYLIGHT_OT_download_sky,
                  SKYLIGHT_OT_download_moon,
                  SKYLIGHT_OT_download_de421,
                  SKYLIGHT_OT_rebuild_world,
                  SKYLIGHT_OT_update_world,
                  SKYLIGHT_PT_main]]


def unregister():
    [utils.make_unregistered(x)
        for x in [SKYLIGHT_preferences,
                  SKYLIGHT_PT_missing_dependency_warning,
                  SKYLIGHT_OT_install_skyfield,
                  SKYLIGHT_OT_download_sky,
                  SKYLIGHT_OT_download_moon,
                  SKYLIGHT_OT_download_de421,
                  SKYLIGHT_OT_rebuild_world,
                  SKYLIGHT_OT_update_world,
                  SKYLIGHT_PT_main]]


if reload_detected:
    dependencies.update()
