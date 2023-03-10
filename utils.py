import bmesh
import bpy
import cv2
import numpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector


def get_pose_data():
    pose_data = {
        "left_ear": {"name": "左耳", "object_name": "", "type": 0, "vec_index": 0},
        "right_ear": {"name": "右耳", "object_name": "", "type": 0, "vec_index": 0},
        "left_eye": {"name": "左眼", "object_name": "", "type": 0, "vec_index": 0},
        "right_eye": {"name": "右眼", "object_name": "", "type": 0, "vec_index": 0},
        "nose": {"name": "鼻子", "object_name": "", "type": 0, "vec_index": 0},
        "chest": {"name": "胸口", "object_name": "", "type": 0, "vec_index": 0},
        "left_shoulder": {"name": "左肩", "object_name": "", "type": 0, "vec_index": 0},
        "right_shoulder": {"name": "右肩", "object_name": "", "type": 0, "vec_index": 0},
        "left_elbow": {"name": "左胳膊肘", "object_name": "", "type": 0, "vec_index": 0},
        "right_elbow": {"name": "右胳膊肘", "object_name": "", "type": 0, "vec_index": 0},
        "left_hand": {"name": "左手", "object_name": "", "type": 0, "vec_index": 0},
        "right_hand": {"name": "右手", "object_name": "", "type": 0, "vec_index": 0},
        "left_waist": {"name": "左腰", "object_name": "", "type": 0, "vec_index": 0},
        "right_waist": {"name": "右腰", "object_name": "", "type": 0, "vec_index": 0},
        "left_knee": {"name": "左膝盖", "object_name": "", "type": 0, "vec_index": 0},
        "right_knee": {"name": "右膝盖", "object_name": "", "type": 0, "vec_index": 0},
        "left_foot": {"name": "左脚", "object_name": "", "type": 0, "vec_index": 0},
        "right_foot": {"name": "右脚", "object_name": "", "type": 0, "vec_index": 0}
    }
    return pose_data


def show_message(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def get_aabb_center(obj):
    """
    通过创建aabb盒子来获取center
    :param obj:
    :return:
    """

    pass


def get_selected_vertices(ob):
    """
    获取选中的顶点
    :return:vert index
    """

    bm = bmesh.from_edit_mesh(ob.data)
    verts = [(vert.co, vert.index) for vert in bm.verts if vert.select]
    if len(verts) != 1:
        return None, 0
    return verts[0]


def get_vec_for_obj_index(ob, index, depsgraph):
    bm = bmesh.new()
    bm.from_object(ob, depsgraph)
    bm.verts.ensure_lookup_table()
    v = bm.verts[index].co
    mat = ob.matrix_world
    loc = mat @ v
    return loc


def get_vec_for_obj(ob, depsgraph):
    bm = bmesh.new()
    bm.from_object(ob, depsgraph)
    bm.verts.ensure_lookup_table()

    bbox = [b.co for b in bm.verts]
    ob_matrix = ob.matrix_world

    # Transform the bounding box coordinates into world coordinates
    bbox = [ob_matrix @ b for b in bbox]

    # Calculate the minimum and maximum coordinates
    min_x = min(b.x for b in bbox)
    max_x = max(b.x for b in bbox)
    min_y = min(b.y for b in bbox)
    max_y = max(b.y for b in bbox)
    min_z = min(b.z for b in bbox)
    max_z = max(b.z for b in bbox)

    # Calculate the center point of the bounding box
    center_x = (max_x + min_x) / 2.0
    center_y = (max_y + min_y) / 2.0
    center_z = (max_z + min_z) / 2.0

    # Return the center point as a world coordinate
    return ob_matrix @ Vector((center_x, center_y, center_z))


def calc_location(vec, camera):
    x, y, z = world_to_camera_view(bpy.context.scene, camera, vec)
    y = 1 - y
    return x, y, z


def calc_pixel(x, y, z, w, h):
    return x * w, y * h, z * 1000


def images_to_video(images, frames, mode, w, h, out_path):
    fourcc = cv2.VideoWriter_fourcc(*mode)
    video = cv2.VideoWriter(out_path, fourcc, frames, (w, h))
    for image in images:
        img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
        video.write(img)
    video.release()
