#!/usr/bin/env python3
#
# See https://pandanote.info/?p=7456 for details.
#

import bpy
import math
import os

currentpath = os.environ['HOMEPATH'] + '/Documents/GitHub/torus_movie'


def remove_mesh_all():
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)


def draw_circle(location, radius, angle):
    # 回転させるときにはfill_typeの設定が反映されないようです。
    bpy.ops.mesh.primitive_circle_add(location=location, radius=radius,
                                      fill_type='NGON')
    bpy.ops.transform.rotate(value=math.pi/2, orient_axis='X')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.transform.rotate(value=math.pi*angle, orient_axis='Z')


def create_partial_torus(location, radius, _angle):
    angle = []
    angle.append(_angle[0]/180)
    angle.append(_angle[1]/180)
    delta_angle = angle[1]-angle[0]
    draw_circle(location, radius, angle[0])
    bpy.ops.object.modifier_add(type='SCREW')
    # Blenderの言語設定を「日本語」にするとmodifierの
    # 設定名は日本語でしか指定できないようです。
    scr = bpy.context.object.modifiers["スクリュー"]
    scr.angle = math.pi*delta_angle
    scr.axis = 'Y'
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["細分化"].levels = 3
    bpy.ops.object.convert(target='MESH')

    draw_circle(location, radius, angle[0])
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.object.convert(target='MESH')

    draw_circle(location, radius, angle[1])
    bpy.ops.object.convert(target='MESH')

    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select_set(True)

    bpy.ops.object.join()


def setup_color(i):
    mat = bpy.data.materials.new('Cube')
    r1 = 0.5 + 0.35*math.sin(i/180*math.pi)
    g1 = 0.5 + 0.35*math.sin(i/90*math.pi)
    b1 = 0.5 + 0.35*math.sin(i/45*math.pi)
    mat.diffuse_color = (r1, g1, b1, 0)
    bpy.context.view_layer.objects.active.data.materials.append(mat)


def generate_test_torus():
    j = -1
    for k in range(5):
        for i in range(181):
            j = j + 1
            remove_mesh_all()
            create_partial_torus((0.9, 0, 0), 0.3, (-i, i))
            setup_color(i*(k+1))
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.ops.render.render()
            bpy.data.images['Render Result'].save_render(
                currentpath + '/torus{:0=4}.png'.format(j))

        for i in reversed(range(181)):
            j = j + 1
            remove_mesh_all()
            create_partial_torus((0.9, 0, 0), 0.3, (-i, i))
            setup_color(i*(k+1))
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.ops.render.render()
            bpy.data.images['Render Result'].save_render(
                filepath=currentpath + '/torus{:0=4}.png'.format(j))


def generate_partial_torus():
    remove_mesh_all()
    create_partial_torus((0.9, 0, 0), 0.3, (0, 60))


# generate_partial_torus()
# for obj in bpy.data.objects:
#    if obj.type == "MESH" and obj.name == "円.002":
#        obj.name = "PartialTorus"

generate_test_torus()
