# Skylight constants and utility functions

import bpy
import logging
import os
import subprocess
from pathlib import Path

CONST_ADDON_NAME = 'skylight'
CONST_SKYFIELD_MODULE_NAME = 'skyfield'
CONST_REQUESTS_MODULE_NAME = 'requests'
CONST_SKY_TEXTURE_NAME = 'assets/sky.exr'
#CONST_SKY_TEXTURE_URL = 'http://localhost/media/starmap_2020_8k.exr'
CONST_SKY_TEXTURE_URL = 'https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004851/starmap_2020_8k.exr'
CONST_MOON_LIBRATION_NAME = 'assets/moon.mp4'
#CONST_MOON_LIBRATION_URL = 'http://localhost/media/phases_2021_plain_2160p30.mp4'
CONST_MOON_LIBRATION_URL = 'https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004874/phases_2021_plain_2160p30.mp4'
CONST_DE421_NAME = 'assets/de421.bsp'
#CONST_MOON_LIBRATION_URL = 'http://localhost/media/de421.bsp'
CONST_DE421_URL = 'https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/de421.bsp'
CONST_BLEND_NAME = 'skylight.blend'
CONST_WORLD_NAME = 'Earth'
CONST_MEGABYTE = 1048576

# Blender addon path
addon_path = bpy.utils.user_resource('SCRIPTS', path='addons')

# Module-level logger
logger = logging.getLogger(CONST_ADDON_NAME)


# Paths to addon assets
def get_sky_path():
    """Calculates the path of the sky texture .exr in this addon's assets folder."""
    return Path(f"{addon_path}/{CONST_ADDON_NAME}/{CONST_SKY_TEXTURE_NAME}")


def get_moon_path():
    """Calculates the path of the moon texture .mp4 in this addon's assets folder."""
    return Path(f"{addon_path}/{CONST_ADDON_NAME}/{CONST_MOON_LIBRATION_NAME}")


def get_de421_path():
    """Calculates the path of the DE421 SPICE kernel in this addon's assets folder."""
    return Path(f"{addon_path}/{CONST_ADDON_NAME}/{CONST_DE421_NAME}")


def get_blend_path():
    """Calculates the path of the Skylight blend file containing the world shader."""
    return Path(f"{addon_path}/{CONST_ADDON_NAME}/{CONST_BLEND_NAME}")


def install_pip():
    """Attempts to make sure that Python's pip package manager is available.
       May require elevated permissions on Windows."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_module(module_name):
    """Attempts to install the named Python module using pip. May require elevated permissions on Windows."""
    install_pip()
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True, env=environ_copy)


def background_invoke(l):
    """Runs the provided parameterless function in a background thread."""
    from threading import Thread
    Thread(target=l).start()


def download_resource(url, target, chunk_size, show_progress, show_finished, check_cancelled):
    """Attempts to download a file from the provided URL to the provided target path,
       saving chunks of the specified size.
       Invokes show_progress with a string describing current progress.
       Invokes show_finished with no parameters when the download has completed.
       Invokes check_cancelled for each chunk and if it returns True,
       it aborts the download and deletes the partial file."""
    import requests
    from time import sleep

    cancelled = False
    with open(target, 'wb') as f:
        progress = "HTTP GET"
        show_progress(progress)
        sleep(0.1)
        response = requests.get(url, stream=True)
        downloaded = 0
        total_length = int(response.headers.get('content-length')) or 0
        for data in response.iter_content(chunk_size=chunk_size):
            if check_cancelled():
                cancelled = True
                break
            downloaded += len(data)
            f.write(data)
            progress = f"{downloaded*100/total_length:.2f}%" if total_length > 0 else f"{downloaded/utils.CONST_MEGABYTE:.2f}MB"
            show_progress(progress)
            sleep(0.1)
    if cancelled:
        Path(target).unlink()
    show_finished()


def initialize_property(obj, prop):
    """Ensures that the provided property definition exists as a custom Blender property on the provided object.
       If the property already exists, this does nothing.
       If the property doesn't exist, it attempts to populate the default value and apply property metadata."""
    name = prop['name']
    default = prop['default']
    if name in obj:
        return
    obj[name] = default
    ui = obj.id_properties_ui(name)
    ui.update(default=default)
    if 'description' in prop:
        ui.update(description = prop['description'])
    if 'min' in prop:
        ui.update(min = prop['min'])
    if 'soft_min' in prop:
        ui.update(soft_min = prop['soft_min'])
    if 'max' in prop:
        ui.update(max = prop['max'])
    if 'soft_max' in prop:
        ui.update(soft_max = prop['soft_max'])
    if 'step' in prop:
        ui.update(step = prop['step'])
    if 'precision' in prop:
        ui.update(precision = prop['precision'])
    if 'subtype' in prop:
        ui.update(subtype = prop['subtype'])


def make_registered(c):
    """Makes the provided type registered in Blender.
       If the type is already registered, it will be un-registered first."""
    make_unregistered(c)
    bpy.utils.register_class(c)


def make_unregistered(c):
    """Makes the provide type un-registered in Blender.
       If the type is already not registered, the exception is ignored."""
    try:
        bpy.utils.unregister_class(c)
    except Exception:
        # There doesn't appear to be a better way to make this idempotent, which is disappointing
        pass


def align_preferences():
    """Sets the registration state of the dependency download and warning panels depending on whether the
       addon has satisfied its external dependencies."""
    from .operators.SKYLIGHT_preferences import SKYLIGHT_preferences
    from .operators.SKYLIGHT_PT_missing_dependency_warning import SKYLIGHT_PT_missing_dependency_warning
    from . import dependencies
    if dependencies.satisfied():
        make_unregistered(SKYLIGHT_preferences)
        make_unregistered(SKYLIGHT_PT_missing_dependency_warning)
    else:
        make_registered(SKYLIGHT_preferences)
        make_registered(SKYLIGHT_PT_missing_dependency_warning)
