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
 
## FAQ / Troubleshooting
 * **Why do the Sun and Moon look so small?**
The actual angular size of the Sun and Moon are each about half a degree. This looks bigger to the human eye when we focus on these objects. If you want these objects to take more of the camera's field of view, you can use a longer focal length.
* **Why is the Sun a plan disc?**
A typical .exr world texture taken from a photographic panorama will include optical effects such as bloom and glare that affected the camera sensor at the time the photograph was taken. In Blender, you'll have to recreate these effects using post-processing such as a glare filter.

## Roadmap / Feature Backlog
* Clouds
* Improve accuracy of sky brightness using solar elevation and twilight definitions
* Add an Earth curvature guide based on elevation
* Map higher-resolution stars onto the camera FOV for longer focal lengths to reduce pixelation