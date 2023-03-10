import json
import os.path
from pathlib import Path

import bpy
from box import Box
from bpy.app.handlers import persistent

from .images import create_image
from .utils import get_vec_for_obj_index, get_vec_for_obj, calc_location, calc_pixel, images_to_video

frames = []


@persistent
def on_frame_change(scene, depsgraph):
    if not scene.record:
        return

    # 获取场景信息
    width = scene.render.resolution_x
    height = scene.render.resolution_y
    camera_name = bpy.data.cameras[0].name
    camera = bpy.data.objects[camera_name]

    depsgraph = bpy.context.evaluated_depsgraph_get()

    json_data = {
        'frame': scene.frame_current,
        'width': width,
        'height': height,
        'poses': {}
    }

    for data in scene.pose_data:
        object_name = data.object_name
        vec_index = data.vec_index
        ob = bpy.data.objects[object_name]

        if data.type == 0:
            # 取中心模式
            vec = get_vec_for_obj(ob, depsgraph)
        else:
            # 计算点模式
            vec = get_vec_for_obj_index(ob, vec_index, depsgraph)

        x, y, z = calc_location(vec, camera)

        x, y, z = calc_pixel(x, y, z, width, height)

        pose = {
            'label': data.name,
            'x': x,
            'y': y,
            'z': z
        }
        json_data['poses'][data.name] = pose

    frames.append(json_data)


def on_create_images(save_images_path, save_video_path):
    images = {}
    w, h = 0, 0
    for frame in frames:
        data = Box(frame)
        image = create_image(data)
        if not w and not h:
            w = data.width
            h = data.height

        if save_images_path:
            image.save(os.path.join(save_images_path, f'frame_{str(data.frame).zfill(5)}.jpg'))

        if save_video_path:
            images[data.frame] = image

    if save_video_path and len(images.values()):
        index = len([
            file
            for file in os.listdir(save_video_path)
            if file.endswith('.mp4')
        ]) + 1
        path = os.path.join(save_video_path, f'{str(index).zfill(5)}.mp4')

        images_to_video(images.values(), 30, 'mp4v', w, h, path)
