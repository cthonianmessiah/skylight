# Skylight Environment Builder
This is a Blender addon that provides a world shader that uses real astronomical data to draw the sky.
Once fully installed, you'll see a new tab in the 3d view that looks like this:

![skylight_main](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/skylight_main.png?raw=true)

Plug in time and space coordinates, and it will draw the sky for you!

![orion](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/orion.png?raw=true)

## Quickstart Guide
1. Download the latest release (ZIP file) from this Github repository's releases page.
2. Open Blender and click on Edit > Preferences and go to the Add-ons section.

![addons](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/addons.png?raw=true)

3. Click the "Install..." button and install the addon by navigating to your saved ZIP file.
4. Open the addon's preferences. It will show a set of buttons for installing the necessary Python dependencies and downloading public-domain image data from NASA.

![preferences](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/preferences.png?raw=true)

5. Click on the buttons to resolve dependencies. Note: On Windows, this may require elevated permissions. If you don't want to run Blender as an administrator, you can look at DOWNLOADING.txt for instructions on how to install these dependencies yourself outside of Blender.
6. Verify that the Skylight tab now shows a form for rebuilding a world shader. If this doesn't work, you may need to finish downloading dependencies.

![got_dependencies](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/got_dependencies.png?raw=true)

7. Click on the 'Rebuild World Shader' to import the Skylight world shader (default name: Earth) into your scene.
8. Enter the coordinates of your world origin and click 'Update World Properties'.
9. All done! You should be able to see the rendered sky in Render Preview mode or in rendered images.

## Cloud Controller
Once the world shader has been rebuilt, as of v0.3.0 you should also see a "Cloud Controller" panel in the Skylight controls. This allows you to add and configure cloud layers in your scene.

![cloud_panel](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/cloud_panel.png?raw=true)

You can click on the "Add Cloud Layer" button to add a cloud layer to your scene from a list of supported cloud types. Cloud layers managed by Skylight will appear in a scene-level collection named "Skylight Clouds". Once one or more cloud layers have been added to the scene, you can configure their properties by selecting them from the drop-down menu:

![cloud_configuration](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/cloud_configuration.png?raw=true)

The Cloud Controller properties are intended to work as follows:

* Altitude: The vertical height of the cloud layer relative to its default height. Increasing this value will move the cloud layer up, decreasing it will move the layer down.
* Clear Patch Size: The scale of "clear patches" containing no clouds. Increasing this value will make larger patches of clear sky, and decreasing it will make them smaller and more granular.
* Cloud Size: The scale of the cloud features themselves in areas of the sky containing clouds. Increasing this value will make cloud features larger and less detailed, decreasing it will make clouds smaller and more granular.
* Coverage: Increasing this value makes clouds cover a larger portion of the sky, and decreasing it makes clouds cover a smaller portion of the sky.
* Density: Increasing this value increases the density of clouds in areas where clouds are present, decreasing it makes clouds more sparse.
* Distance Scaling: This value controls nonlinear scaling, which allows the "cloud dome" to appear larger than it is as it approaches the horizon. If you don't like is scale disortion, you can weaken the effect by decreasing the value, or even eliminate it by setting it to zero.
* Offset X: Moves cloud coordinates along the X axis. If nonlinear scaling is enabled, this will also permute the clouds, causing them to change shape as they move.
* Offset Y: Moves cloud coordinates along the Y axis. If nonlinear scaling is enabled, this will also permute the clouds, causing them to change shape as they move.
* Opacity: Increasing this value makes clouds more opaque, and decreasing it makes them more transparent.
* Rotation: Rotates cloud coordinates about the Z axis.
* Seed: Change this integer value to generate different cloud patterns using the same configuration.
* World Radius: This is the horizontal "clear distance" of the cloud layer, such that the clouds will cross the horizon line beyond this distance from the world origin. If you find that the cloud layer is intersecting with your background objects, you can manipulate this value to change the scale of the cloud layer.

**Note: Cloud layers use volumetric shaders and require the Cycles rendering engine to dislpay properly.**

Once you've configured your clouds how you want (and set up your Cycles volumetric render settings), you can pretty easily get a sky and clouds in your scene:

![cloud_example](https://github.com/cthonianmessiah/skylight/blob/dev/readme_media/cloud_example.png?raw=true)

## FAQ / Troubleshooting
 * **Why do the Sun and Moon look so small?**
The actual angular size of the Sun and Moon are each about half a degree. This looks bigger to the human eye when we focus on these objects. If you want these objects to take more of the camera's field of view, you can use a longer focal length.
* **Why is the Sun a plain disc?**
A typical .exr world texture taken from a photographic panorama will include optical effects such as bloom and glare that affected the camera sensor at the time the photograph was taken. In Blender, you'll have to recreate these effects using post-processing such as a glare filter.

## Roadmap / Feature Backlog
* Clouds
* Improve accuracy of sky brightness using solar elevation and twilight definitions
* Add an Earth curvature guide based on elevation
* Map higher-resolution stars onto the camera FOV for longer focal lengths to reduce pixelation