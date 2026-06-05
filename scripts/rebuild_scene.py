"""
rebuild_scene.py — 台中洲際段1098地號 3D 建模重建腳本
在 Blender 5.1.2 的 Scripting 分頁貼入並執行即可從頭重建場景骨架。

注意：此腳本只建結構量體與材質；PolyHaven 家具素材需另行下載。
完整場景請直接開啟 blend/1098_final_with_roads.blend。
"""

import bpy
import math
from mathutils import Vector


# ── 清場 ──────────────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)


# ── 材質工廠 ──────────────────────────────────────────────────────────────────
def make_mat(name, color, alpha=1.0, metallic=0.0, roughness=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*color, 1.0)
    b.inputs['Alpha'].default_value = alpha
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = roughness
    if alpha < 1.0:
        m.blend_method = 'BLEND'
    return m


# 結構材質
MAT = {
    'Site':     make_mat('SiteGnd',   (0.45,0.55,0.40), alpha=0.20),
    'Road':     make_mat('Road_Asph', (0.15,0.15,0.15), alpha=0.25),
    'Sidewalk': make_mat('Sidewalk',  (0.75,0.72,0.65), alpha=0.30),
    'Slab':     make_mat('Slab',      (0.75,0.75,0.75), alpha=0.35),
    'Concrete': make_mat('Concrete',  (0.65,0.65,0.65)),
    # 外殼半透明（各層用色）
    'Sh_B1':   make_mat('Sh_B1',   (0.35,0.35,0.35), alpha=0.30),
    'Sh_1F':   make_mat('Sh_1F',   (0.90,0.55,0.20), alpha=0.30),
    'Sh_2F':   make_mat('Sh_2F',   (0.20,0.45,0.80), alpha=0.30),
    'Sh_3F':   make_mat('Sh_3F',   (0.25,0.70,0.35), alpha=0.30),
    'Sh_4F':   make_mat('Sh_4F',   (0.25,0.70,0.35), alpha=0.30),
    'Sh_5F':   make_mat('Sh_5F',   (0.65,0.25,0.80), alpha=0.30),
    'Sh_Roof': make_mat('Sh_Roof', (0.65,0.45,0.20), alpha=0.30),
}


# ── 量體工廠 ──────────────────────────────────────────────────────────────────
def box(name, x0, x1, y0, y1, z0, z1, mat=None):
    cx, cy, cz = (x0+x1)/2, (y0+y1)/2, (z0+z1)/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    o = bpy.context.active_object
    o.name = name
    o.scale = (x1-x0, y1-y0, z1-z0)
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        o.data.materials.clear()
        o.data.materials.append(mat)
    return o


# ── 建物各層量體 ──────────────────────────────────────────────────────────────
# 座標系：X=東西（0~23.7m），Y=南北（0~24.6m），Z=高度
# 各層 Z 範圍
FLOORS = {
    'B1':  (-3.50,  0.00, 0.00, 23.70,  0.00, 23.10, 'Sh_B1'),
    '1F':  ( 0.00,  4.00, 0.00, 23.70,  2.60, 16.60, 'Sh_1F'),
    '2F':  ( 4.00,  7.50, 0.00, 23.70,  4.50, 16.60, 'Sh_2F'),
    '3F':  ( 7.50, 10.50, 0.00, 23.70,  6.70, 16.60, 'Sh_3F'),
    '4F':  (10.50, 13.50, 0.00, 23.70,  6.70, 16.60, 'Sh_4F'),
    '5F':  (13.50, 16.50, 5.00, 23.70,  8.00, 14.40, 'Sh_5F'),
    'Roof':(16.50, 19.00, 5.00, 11.00,  8.00, 14.40, 'Sh_Roof'),
}

for fname, (z0, z1, x0, x1, y0, y1, mkey) in FLOORS.items():
    box(f'{fname}_Shell', x0, x1, y0, y1, z0, z1, MAT[mkey])

# 樓板
SLABS = [
    ('B1_Slab',   0.00, 23.70,  0.00, 23.10, -3.50, -3.20),
    ('1F_Slab',   0.00, 23.70,  2.60, 16.60,  0.00,  0.30),
    ('2F_Slab',   0.00, 23.70,  4.50, 16.60,  4.00,  4.30),
    ('3F_Slab',   0.00, 23.70,  6.70, 16.60,  7.50,  7.80),
    ('4F_Slab',   0.00, 23.70,  6.70, 16.60, 10.50, 10.80),
    ('5F_Slab',   5.00, 23.70,  8.00, 14.40, 13.50, 13.80),
    ('Roof_Slab', 5.00, 11.00,  8.00, 14.40, 16.50, 16.80),
]
for name, x0, x1, y0, y1, z0, z1 in SLABS:
    box(name, x0, x1, y0, y1, z0, z1, MAT['Slab'])


# ── 基地地面與道路 ────────────────────────────────────────────────────────────
box('Site_Ground', -10.0, 50.0, -25.0, 40.0, -0.15, 0.0, MAT['Site'])

# 道路（簡化版，僅主要路面）
roads = [
    ('Road_ChongDe',  23.70, 43.70,  0.00, 16.60),   # 崇德十路二段（東）
    ('Road_FengLe3',   0.00, 23.70, -20.00,  0.00),   # 豐樂路三段（南）
    ('Road_FengLe1', -12.00,  0.00,  0.00, 16.60),    # 豐樂一街（西）
    ('Road_FengLeN2',  0.00, 23.70, 16.60, 36.60),    # 豐樂北二路（北）
]
for name, x0, x1, y0, y1 in roads:
    box(name, x0, x1, y0, y1, -0.05, 0.0, MAT['Road'])


# ── 停車場（B1 東側）────────────────────────────────────────────────────────
# 8 格停車位 2.5m×5.3m，X[17.7,23.0]，Y 方向排列
for i in range(8):
    cy = 1.25 + i * 2.5
    box(f'B1_ParkingLine_{i+1}', 17.70, 17.75, cy-1.25, cy+1.25, -3.20, -3.18,
        make_mat(f'PLine_{i}', (1,1,1), roughness=0.9))


# ── 燈光設定 ──────────────────────────────────────────────────────────────────
def area_light(name, loc, energy=800, size=4.0):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.active_object
    l.name = name
    l.data.energy = energy
    l.data.size = size
    l.hide_viewport = True
    return l

floor_lights = [
    ('Light_B1',   (11.85,  8.0, -1.0)),
    ('Light_1F_a', (6.0,   8.0,  3.5)),
    ('Light_1F_b', (18.0,  8.0,  3.5)),
    ('Light_2F_a', (6.0,   8.0,  7.0)),
    ('Light_2F_b', (18.0,  8.0,  7.0)),
    ('Light_3F_a', (6.0,   8.0, 10.0)),
    ('Light_3F_b', (18.0,  8.0, 10.0)),
    ('Light_4F_a', (6.0,   8.0, 13.0)),
    ('Light_4F_b', (18.0,  8.0, 13.0)),
    ('Light_5F',   (14.0, 11.0, 16.0)),
]
for name, loc in floor_lights:
    area_light(name, loc)

# 天空光（Hosek-Wilkie 程序性天空）
world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    sky = world.node_tree.nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'HOSEK_WILKIE'
    sky.sun_direction = (0.5, -0.5, 0.7)
    sky.turbidity = 3.0
    world.node_tree.links.new(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 1.5


# ── 攝影機 ────────────────────────────────────────────────────────────────────
bpy.ops.object.camera_add(location=(-22, -18, 28))
cam = bpy.context.active_object
cam.name = 'Camera_Main'
cam.rotation_euler = (math.radians(55), 0, math.radians(-40))
cam.data.lens = 35
bpy.context.scene.camera = cam


# ── 渲染設定 ──────────────────────────────────────────────────────────────────
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080


print("=" * 60)
print("場景重建完成！")
print(f"物件數: {len(bpy.data.objects)}")
print(f"材質數: {len(bpy.data.materials)}")
print("注意：PolyHaven 家具素材需透過 blender-mcp 另行下載配置。")
print("完整場景請直接開啟 blend/1098_final_with_roads.blend。")
print("=" * 60)
