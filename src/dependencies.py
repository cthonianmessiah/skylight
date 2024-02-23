# External dependency inspection

import importlib

from . import utils

# Skyfield provides ephemeris calculation for celestial bodies
dep_skyfield = False
dep_requests = False

# Textures are downloaded courtesy of NASA's Scientific Visualization Studio
dep_sky_texture = False
dep_moon_texture = False
dep_de421_spice = False

def update():
    """Evaluates whether this addon's dependencies have been satisfied."""
    global dep_skyfield
    global dep_requests
    global dep_sky_texture
    global dep_moon_texture
    global dep_de421_spice
    dep_skyfield = False
    dep_requests = False
    dep_sky_texture = False
    dep_moon_texture = False
    dep_de421_spice = False

    if utils.CONST_SKYFIELD_MODULE_NAME in globals():
        importlib.reload(globals()[utils.CONST_SKYFIELD_MODULE_NAME])
        dep_skyfield = True
    else:
        try:
            globals()[utils.CONST_SKYFIELD_MODULE_NAME] = importlib.import_module(utils.CONST_SKYFIELD_MODULE_NAME)
            dep_skyfield = True
        except ModuleNotFoundError:
            utils.logger.warning("The Skyfield module is required but not installed.")

    sky_path = utils.get_sky_path()
    if sky_path.is_file():
        dep_sky_texture = True
    else:
        utils.logger.warning(f"Sky texture file not found at '{sky_path.resolve()}'")

    moon_path = utils.get_moon_path()
    if moon_path.is_file():
        dep_moon_texture = True
    else:
        utils.logger.warning(f"Moon libration video not found at '{moon_path.resolve()}'")

    de421_path = utils.get_de421_path()
    if de421_path.is_file():
        dep_de421_spice = True
    else:
        utils.logger.warning(f"DE421 SPICE kernel not found at '{de421_path.resolve()}'")

    if not satisfied():
        if utils.CONST_REQUESTS_MODULE_NAME in globals():
            importlib.reload(globals()[utils.CONST_REQUESTS_MODULE_NAME])
            dep_requests = True
        else:
            try:
                globals()[utils.CONST_REQUESTS_MODULE_NAME] = importlib.import_module(utils.CONST_REQUESTS_MODULE_NAME)
                dep_requests = True
            except ModuleNotFoundError:
                utils.logger.warning("The Requests module is required to download dependencies but is not installed.")

def satisfied():
    """Returns True if this addon's external dependencies have been satisfied, otherwise returns False."""
    return dep_skyfield and dep_de421_spice and dep_sky_texture and dep_moon_texture
