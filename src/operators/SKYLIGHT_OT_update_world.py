import bpy
import math
import mathutils
from datetime import datetime

from ... import dependencies, utils


class SKYLIGHT_OT_update_world(bpy.types.Operator):
    """Attempts to set current world properties and update ephemeris calculations based on
       currently populated time and lat/long coordinates."""
    bl_idname = 'skylight.update_world'
    bl_label = "Update World Properties"
    bl_description = ("Recalculates world properties based on provided coordinates.")
    bl_options = {'REGISTER'}


    def ensure_world(self, context):
        scene = context.scene
        world = scene.world
        if world is None:
            world = bpy.data.worlds.new("Earth")
            scene.world = world
        utils.initialize_property(world, dict(
            name='date_time',
            description=("Time in the form YYYY-MM-DD HH:ss:mm.fffZ. UTC looks like '2000-01-01 12:34:56.789Z', "
                         "local time looks like '2000-01-01 07:34:56.789-05:00'"),
            default="2000-01-01 00:00:00+00:00"
            ))
        utils.initialize_property(world, dict(
            name='latitude',
            description=("The latitude of the world origin, where positive angles are north of the equator "
                         "and negative angles are south of the equator"),
            default=0.0,
            subtype='ANGLE',
            min=math.pi/-2,
            max=math.pi/2
            ))
        utils.initialize_property(world, dict(
            name='longitude',
            description=("The longitude of the world origin, where positive angles are east of the prime meridian "
                         "and negative angles are west of the prime meridian"),
            default=0.0,
            subtype='ANGLE',
            min=math.pi*-1,
            max=math.pi
            ))
        utils.initialize_property(world, dict(
            name='elevation',
            description=("The elevation in meters of the world origin relative to the surface of the WGS84 ellipsoid "
                         "(this is pretty close to sea level elevation)"),
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='heading',
            description=("The alignment of the positive Y axis of the world origin as a compass heading, "
                         "where 0 is north, 90 degrees is east, 180 degrees is south, and 270 degrees is west"),
            default=0.0,
            subtype='ANGLE',
            min=0.0,
            max=math.pi*2
            ))
        utils.initialize_property(world, dict(
            name='sky_rotation',
            description=("The rotation of background stars relative to their ICRF/J2000 geocentric coordinates. "
                         "Skylight can set this for you based on time and location"),
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='sun_rotation',
            description="The rotation of the Sun relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='moon_rotation',
            description="The rotation of the Moon relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='moon_phase',
            description="The phase of the moon where 0 is a new moon and 180 degrees is a full moon",
            default=0.0,
            subtype='ANGLE'
            ))
        utils.initialize_property(world, dict(
            name='venus_rotation',
            description="The rotation of Venus relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='venus_magnitude',
            description="The apparent magnitude of Venus from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='jupiter_rotation',
            description="The rotation of Jupiter relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='jupiter_magnitude',
            description="The apparent magnitude of Jupiter from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='mercury_rotation',
            description="The rotation of Mercury relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='mercury_magnitude',
            description="The apparent magnitude of Mercury from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='saturn_rotation',
            description="The rotation of Saturn relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='saturn_magnitude',
            description="The apparent magnitude of Saturn from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='mars_rotation',
            description="The rotation of Mars relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='mars_magnitude',
            description="The apparent magnitude of Mars from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='uranus_rotation',
            description="The rotation of Uranus relative to azimuth 0 (north) and elevation 0 (the horizon)",
            default=[0.0, 0.0, 0.0],
            subtype='EULER'
            ))
        utils.initialize_property(world, dict(
            name='uranus_magnitude',
            description="The apparent magnitude of Uranus from the observer's position",
            default=0.0
            ))
        utils.initialize_property(world, dict(
            name='ui_selected_cloud_layer',
            description="The currently selected cloud layer in the cloud controller panel",
            default=''
            ))


    def apply_skyfield(self, context):
        world = context.scene.world

        from skyfield import api
        from skyfield import almanac
        from skyfield.magnitudelib import planetary_magnitude

        ts = api.load.timescale()
        t = ts.from_datetime(datetime.fromisoformat(world['date_time']))
        eph = api.load(str(utils.get_de421_path().resolve()))
        frame = api.wgs84.latlon(
            math.degrees(world['latitude']),
            math.degrees(world['longitude']),
            elevation_m = world['elevation'])
        origin = (eph['earth'] + frame).at(t)

        # The Sky
        rot = frame.rotation_at(t)
        mat = mathutils.Matrix(rot)
        eu = mat.to_euler()
        sky_rotation = world['sky_rotation']
        sky_rotation[0] = eu.x
        sky_rotation[1] = eu.y
        sky_rotation[2] = eu.z * -1

        # The Sun
        sun = eph['sun']
        astrometric = origin.observe(sun)
        alt, az, _ = astrometric.apparent().altaz()
        sun_rotation = world['sun_rotation']
        sun_rotation[1] = alt.radians * -1
        sun_rotation[2] = az.radians * -1

        # The Moon
        moon = eph['moon']
        astrometric = origin.observe(moon)
        alt, az, _ = astrometric.apparent().altaz()
        moon_rotation = world['moon_rotation']
        moon_rotation[1] = alt.radians * -1
        moon_rotation[2] = az.radians * -1
        world['moon_phase'] = almanac.moon_phase(eph, t).radians

        # Venus
        venus = eph['venus']
        astrometric = origin.observe(venus)
        alt, az, _ = astrometric.apparent().altaz()
        venus_rotation = world['venus_rotation']
        venus_rotation[1] = alt.radians * -1
        venus_rotation[2] = az.radians * -1
        world['venus_magnitude'] = planetary_magnitude(astrometric)

        # Jupiter
        jupiter = eph['jupiter barycenter']
        astrometric = origin.observe(jupiter)
        alt, az, _ = astrometric.apparent().altaz()
        jupiter_rotation = world['jupiter_rotation']
        jupiter_rotation[1] = alt.radians * -1
        jupiter_rotation[2] = az.radians * -1
        world['jupiter_magnitude'] = planetary_magnitude(astrometric)

        # Mercury
        mercury = eph['mercury']
        astrometric = origin.observe(mercury)
        alt, az, _ = astrometric.apparent().altaz()
        mercury_rotation = world['mercury_rotation']
        mercury_rotation[1] = alt.radians * -1
        mercury_rotation[2] = az.radians * -1
        world['mercury_magnitude'] = planetary_magnitude(astrometric)

        # Saturn
        saturn = eph['saturn barycenter']
        astrometric = origin.observe(saturn)
        alt, az, _ = astrometric.apparent().altaz()
        saturn_rotation = world['saturn_rotation']
        saturn_rotation[1] = alt.radians * -1
        saturn_rotation[2] = az.radians * -1
        world['saturn_magnitude'] = planetary_magnitude(astrometric)

        # Mars
        mars = eph['mars']
        astrometric = origin.observe(mars)
        alt, az, _ = astrometric.apparent().altaz()
        mars_rotation = world['mars_rotation']
        mars_rotation[1] = alt.radians * -1
        mars_rotation[2] = az.radians * -1
        world['mars_magnitude'] = planetary_magnitude(astrometric)

        # Uranus
        uranus = eph['uranus barycenter']
        astrometric = origin.observe(uranus)
        alt, az, _ = astrometric.apparent().altaz()
        uranus_rotation = world['uranus_rotation']
        uranus_rotation[1] = alt.radians * -1
        uranus_rotation[2] = az.radians * -1
        world['uranus_magnitude'] = planetary_magnitude(astrometric)

        # Signal that world properties have been changed, triggering the shader to redraw
        world.update_tag()


    @classmethod
    def poll(self, context):
        return dependencies.satisfied()


    def execute(self, context):
        self.ensure_world(context)
        self.apply_skyfield(context)

        return {'FINISHED'}
