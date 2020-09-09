import pyglet
import ratcave as rc
from pyglet.gl import *
from pyglet.window import key


def render():
    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = pyglet.window.Window(config=config, resizable=True, caption="Python 3D Test by Matthias Wurm")
    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    # Monkey Mesh Test
    obj_filename = rc.resources.obj_primitives
    monkey = rc.WavefrontReader(obj_filename).get_mesh("Cube")
    # Scene Creation
    scene = rc.Scene(monkey)
    scene.bgColor = 0.3, 0.2, 1
    # Monkey position & scale
    monkey.position.xyz = 0, 0, -5
    monkey.scale = .8
    monkey.uniforms["diffuse"] = 0.9, 0.6, 0.3

    # Engine Event Loop
    def move_camera(dt):
        camera_speed = 5
        if keys[key.LEFT]:
            scene.camera.position.x -= camera_speed * dt
        if keys[key.RIGHT]:
            scene.camera.position.x += camera_speed * dt
        if keys[key.UP]:
            scene.camera.position.z -= camera_speed * dt
        if keys[key.DOWN]:
            scene.camera.position.z += camera_speed * dt

    pyglet.clock.schedule(move_camera)

    def rotate_meshes(dt):
        monkey.rotation.y += 75 * dt
        monkey.rotation.x += 45 * dt

    pyglet.clock.schedule(rotate_meshes)

    @window.event
    def on_draw():
        window.clear()
        with rc.default_shader, rc.default_states:
            scene.draw()

    pyglet.app.run()
