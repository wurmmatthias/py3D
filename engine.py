import ratcave as rc
from pyglet.gl import *
from pyglet.window import key, mouse
import numpy


def render():
    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = pyglet.window.Window(config=config, resizable=True, caption="Python 3D Test by Matthias Wurm")
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    window.set_mouse_visible(True)
    # Window Text Creation
    unit_label = pyglet.text.Label('Units: x',
                              font_name='Times New Roman',
                              font_size=16,
                              x=window.width // 2, y=window.height // 2,
                              anchor_x='center', anchor_y='center')

    # Mesh Test
    obj_filename = rc.resources.obj_primitives
    plane = rc.WavefrontReader(obj_filename).get_mesh("Plane")
    house = rc.WavefrontReader("./ressources/12.obj").get_mesh("12")

    # Scene Creation
    scene = rc.Scene([plane, house])
    scene.bgColor = 0.3, 0.2, 1

    # Terrain position & scale
    plane.position.xyz = 0, 0, -5
    plane.scale = 2
    plane.uniforms["diffuse"] = 0.5, 0.9, 0.5
    house.position.xyz = 0, 0, -5.1
    house.scale = 0.1
    house.rotation.x = 90
    house.uniforms["diffuse"] = 0.5, 0.1, 1

    # Camera Position and Rotation on Init
    scene.camera.rotation.x = 45

    def rotate_meshes(dt):
        plane.rotation.y += 75 * dt
        plane.rotation.x += 45 * dt

    # pyglet.clock.schedule(rotate_meshes)

    def camera_rotation(x, y):
        scene.camera.rotation.x = y
        scene.camera.rotation.y = numpy.invert(x)

    def camera_zoom(a):
        zoom_speed = 0.5
        if a < 0:
            scene.camera.position.z += zoom_speed
        elif a > 0:
            scene.camera.position.z -= zoom_speed

    # Engine Event Loop
    def move_camera(dt):
        camera_speed = 5
        if keys[key.A] or keys[key.LEFT]:
            scene.camera.position.x -= camera_speed * dt
        if keys[key.D] or keys[key.RIGHT]:
            scene.camera.position.x += camera_speed * dt
        if keys[key.W] or keys[key.UP]:
            scene.camera.position.y += camera_speed * dt
        if keys[key.S] or keys[key.DOWN]:
            scene.camera.position.y -= camera_speed * dt

    pyglet.clock.schedule(move_camera)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            camera_rotation(x, y)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        camera_zoom(scroll_y)

    @window.event
    def on_draw():
        window.clear()
        with rc.default_shader, rc.default_states:
            scene.draw()

    pyglet.app.run()
