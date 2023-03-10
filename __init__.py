import json
import os
from pathlib import Path

import bpy
from bpy.app.handlers import persistent

from .utils import show_message, get_pose_data, get_selected_vertices
from .openpose import on_frame_change, frames, on_create_images


class OpenPoseDataItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    china_name: bpy.props.StringProperty()
    display_name: bpy.props.StringProperty()
    object_name: bpy.props.StringProperty()
    type: bpy.props.IntProperty(default=-1)
    vec_index: bpy.props.IntProperty()


class PoseDataPanel(bpy.types.Panel):
    bl_label = "openpose"
    bl_idname = "OPENPOSE_PT_POSEDATA"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Pose Data"

    def draw(self, context):
        layout = self.layout
        pose_data = context.scene.pose_data
        for i, item in enumerate(pose_data):
            row = layout.row()
            row.label(text=item.display_name)
            row.operator("openpose.update_pose_data", text="Update").index = i

        column = layout.column()
        column.prop(context.scene, "extension_hands")
        column.prop(context.scene, "export_images")
        if context.scene.export_images:
            column.prop(context.scene, "export_images_path")

        column.prop(context.scene, "export_movie")
        if context.scene.export_movie:
            column.prop(context.scene, "export_movie_path")
        column.operator("openpose.record_pose_data", text="开始录制" if not context.scene.record else '停止录制')


class UpdatePoseDataOperator(bpy.types.Operator):
    bl_idname = "openpose.update_pose_data"
    bl_label = "Update Pose Data"

    index: bpy.props.IntProperty()

    def execute(self, context):
        pose_data = context.scene.pose_data[self.index]

        # 判断当前物体
        obj = context.active_object
        if obj.mode == 'OBJECT':
            show_message("请进入编辑模式选择顶点！", '错误', 'ERROR')
            return {'CANCELLED'}
            # pose_data.object_name = obj.name
            # pose_data.type = 0
            # pose_data.display_name = f'{pose_data.china_name}: {obj.name}'
        else:
            vec, index = get_selected_vertices(obj)
            if not vec and index == 0:
                show_message("当前处于编辑模式，未选中顶点或者选择了多个顶点！", '错误', 'ERROR')
                return {'CANCELLED'}
            pose_data.object_name = obj.name
            pose_data.type = 1
            pose_data.vec_index = index
            pose_data.display_name = f'{pose_data.china_name}: {obj.name}[{index}]'

        return {'FINISHED'}


class RecordPoseDataOperator(bpy.types.Operator):
    bl_idname = "openpose.record_pose_data"
    bl_label = "Record Pose Data"

    index: bpy.props.IntProperty()

    def execute(self, context):
        if not context.scene.record:
            # 判断是否全部选中
            for data in context.scene.pose_data:
                if not data.object_name or data.type == -1:
                    show_message("未处理好姿态结构！请先处理姿态结构", '错误', 'ERROR')
                    return {'CANCELLED'}

            if not context.scene.export_images and not context.scene.export_movie:
                show_message("不导出吗？", '错误', 'ERROR')
                return {'CANCELLED'}
            if context.scene.export_images and not context.scene.export_images_path:
                show_message("还未设置图片导出目录。", '错误', 'ERROR')
                return {'CANCELLED'}

            if context.scene.export_movie and not context.scene.export_movie_path:
                show_message("还未设置视频导出目录。", '错误', 'ERROR')
                return {'CANCELLED'}

            if len(bpy.data.cameras) != 1:
                show_message("场景内不存在摄像机或存在多个摄像机。", '错误', 'ERROR')
                return {'CANCELLED'}
            frames.clear()
        else:
            images_path = None if not context.scene.export_images else context.scene.export_images_path
            movie_path = None if not context.scene.export_movie else context.scene.export_movie_path
            on_create_images(images_path, movie_path)

        context.scene.record = not context.scene.record
        return {'FINISHED'}


classes = [
    OpenPoseDataItem,
    PoseDataPanel,
    UpdatePoseDataOperator,
    RecordPoseDataOperator
]


@persistent
def register_pose_data(scene, depsgraph):
    if not scene.pose_data:
        for k, v in get_pose_data().items():
            data = scene.pose_data.add()
            data.name = k
            data.china_name = v['name']
            data.display_name = v['name']
            data.object_name = v['object_name']
            data.type = v['type']
            data.vec_index = v['vec_index']

    bpy.app.handlers.depsgraph_update_post.remove(register_pose_data)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pose_data = bpy.props.CollectionProperty(type=OpenPoseDataItem)

    bpy.types.Scene.extension_hands = bpy.props.BoolProperty(name='手部姿态(待更新)', default=False)

    bpy.types.Scene.export_images = bpy.props.BoolProperty(name='导出图片', default=True)
    bpy.types.Scene.export_images_path = bpy.props.StringProperty(name="图片目录",
                                                                  description="选择要保存图片的目录:",
                                                                  default="",
                                                                  maxlen=1024,
                                                                  subtype='DIR_PATH')

    bpy.types.Scene.export_movie = bpy.props.BoolProperty(name='导出视频', default=True)
    bpy.types.Scene.export_movie_path = bpy.props.StringProperty(name="视频目录",
                                                                 description="选择要保存视频的目录:",
                                                                 default="",
                                                                 maxlen=1024,
                                                                 subtype='DIR_PATH')
    bpy.types.Scene.record = bpy.props.BoolProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.pose_data
    del bpy.types.Scene.export_images
    del bpy.types.Scene.export_images_path
    del bpy.types.Scene.export_movie
    del bpy.types.Scene.export_movie_path
    del bpy.types.Scene.record
    del bpy.types.Scene.extension_hands
    if on_frame_change in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(on_frame_change)


if __name__ == '__main__':
    register()

if register_pose_data not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(register_pose_data)

if on_frame_change not in bpy.app.handlers.frame_change_pre:
    bpy.app.handlers.frame_change_pre.append(on_frame_change)

bl_info = {
    "name": "sd-webui-controlNet-openpose",
    "author": "scholar0",
    "description": "适用于sd-webui-controlNet-openpose的blender脚本",
    "blender": (3, 30, 0),
    "location": "View3D > UI",
    "warning": "",
    "category": "Generic"
}
