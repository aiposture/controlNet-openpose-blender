import json
import os.path
from pathlib import Path

from PIL import Image, ImageColor
from PIL.ImageDraw import Draw

file = os.path.dirname(__file__)
colors = json.loads(Path(os.path.join(file, 'config.json')).read_text())


def to_rgba(color, alpha=255):
    c = ImageColor.getcolor(color, 'RGBA')

    return c[0], c[1], c[2], alpha


def create_image(data):
    with Image.new('RGB', (data.width, data.height)) as image:
        draw = Draw(image, 'RGBA')
        # 组合成线
        left_eye = data.poses.left_eye
        left_ear = data.poses.left_ear
        left_shoulder = data.poses.left_shoulder
        left_elbow = data.poses.left_elbow
        left_hand = data.poses.left_hand
        left_waist = data.poses.left_waist
        left_knee = data.poses.left_knee
        left_foot = data.poses.left_foot
        right_eye = data.poses.right_eye
        right_ear = data.poses.right_ear
        right_shoulder = data.poses.right_shoulder
        right_elbow = data.poses.right_elbow
        right_hand = data.poses.right_hand
        right_waist = data.poses.right_waist
        right_knee = data.poses.right_knee
        right_foot = data.poses.right_foot
        nose = data.poses.nose
        chest = data.poses.chest

        lines = []

        left_eye_ear = {
            'name': 'left_eye_ear',
            'start': {'x': left_eye.x, 'y': left_eye.y},
            'end': {'x': left_ear.x, 'y': left_ear.y},
            'distance': left_ear.y  # 左眼和左耳，取左耳到摄像机的距离
        }
        lines.append(left_eye_ear)

        left_eye_nose = {
            'name': 'left_eye_nose',

            'start': {'x': left_eye.x, 'y': left_eye.y},
            'end': {'x': nose.x, 'y': nose.y},
            'distance': left_eye.y  # 左眼到鼻子，取左眼的距离
        }
        lines.append(left_eye_nose)

        right_eye_ear = {
            'name': 'right_eye_ear',

            'start': {'x': right_eye.x, 'y': right_eye.y},
            'end': {'x': right_ear.x, 'y': right_ear.y},
            'distance': right_ear.y  # 右眼到右耳，取右耳
        }
        lines.append(right_eye_ear)

        right_eye_nose = {
            'name': 'right_eye_nose',

            'start': {'x': right_eye.x, 'y': right_eye.y},
            'end': {'x': nose.x, 'y': nose.y},
            'distance': right_eye.y  # 右眼到鼻子，取右眼
        }
        lines.append(right_eye_nose)

        nose_chest = {
            'name': 'nose_chest',

            'start': {'x': nose.x, 'y': nose.y},
            'end': {'x': chest.x, 'y': chest.y},
            'distance': nose.y  # 鼻子到胸口 取鼻子
        }
        lines.append(nose_chest)

        chest_left_shoulder = {
            'name': 'chest_left_shoulder',

            'start': {'x': chest.x, 'y': chest.y},
            'end': {'x': left_shoulder.x, 'y': left_shoulder.y},
            'distance': chest.y  # 胸口到左肩，取胸口
        }
        lines.append(chest_left_shoulder)

        chest_right_shoulder = {
            'name': 'chest_right_shoulder',

            'start': {'x': chest.x, 'y': chest.y},
            'end': {'x': right_shoulder.x, 'y': right_shoulder.y},
            'distance': chest.y  # 胸口到右肩，取胸口
        }
        lines.append(chest_right_shoulder)

        left_shoulder_elbow = {
            'name': 'left_shoulder_elbow',

            'start': {'x': left_shoulder.x, 'y': left_shoulder.y},
            'end': {'x': left_elbow.x, 'y': left_elbow.y},
            'distance': left_shoulder.y  # 左肩到左臂，取左肩
        }
        lines.append(left_shoulder_elbow)

        right_shoulder_elbow = {
            'name': 'right_shoulder_elbow',

            'start': {'x': right_shoulder.x, 'y': right_shoulder.y},
            'end': {'x': right_elbow.x, 'y': right_elbow.y},
            'distance': right_shoulder.y  # 右肩到右臂，取右肩
        }
        lines.append(right_shoulder_elbow)

        left_elbow_hand = {
            'name': 'left_elbow_hand',

            'start': {'x': left_elbow.x, 'y': left_elbow.y},
            'end': {'x': left_hand.x, 'y': left_hand.y},
            'distance': left_elbow.y  # 左臂到左手，取左臂
        }
        lines.append(left_elbow_hand)

        right_elbow_hand = {
            'name': 'right_elbow_hand',

            'start': {'x': right_elbow.x, 'y': right_elbow.y},
            'end': {'x': right_hand.x, 'y': right_hand.y},
            'distance': right_elbow.y  # 右臂到右手，取右臂
        }
        lines.append(right_elbow_hand)

        chest_left_waist = {
            'name': 'chest_left_waist',

            'start': {'x': chest.x, 'y': chest.y},
            'end': {'x': left_waist.x, 'y': left_waist.y},
            'distance': chest.y  # 胸口到左胯骨，取胸口
        }
        lines.append(chest_left_waist)

        chest_right_waist = {
            'name': 'chest_right_waist',

            'start': {'x': chest.x, 'y': chest.y},
            'end': {'x': right_waist.x, 'y': right_waist.y},
            'distance': chest.y  # 胸口到右胯骨，取胸口
        }
        lines.append(chest_right_waist)

        left_waist_knee = {
            'name': 'left_waist_knee',

            'start': {'x': left_waist.x, 'y': left_waist.y},
            'end': {'x': left_knee.x, 'y': left_knee.y},
            'distance': left_waist.y  # 左胯骨到左膝盖，取左胯骨
        }
        lines.append(left_waist_knee)

        right_waist_knee = {
            'name': 'right_waist_knee',

            'start': {'x': right_waist.x, 'y': right_waist.y},
            'end': {'x': right_knee.x, 'y': right_knee.y},
            'distance': right_waist.y  # 右胯骨到右膝盖，取右胯骨
        }
        lines.append(right_waist_knee)

        left_knee_foot = {
            'name': 'left_knee_foot',

            'start': {'x': left_knee.x, 'y': left_knee.y},
            'end': {'x': left_foot.x, 'y': left_foot.y},
            'distance': left_knee.y  # 左膝盖到左脚，取左膝盖
        }
        lines.append(left_knee_foot)

        right_knee_foot = {
            'name': 'right_knee_foot',

            'start': {'x': right_knee.x, 'y': right_knee.y},
            'end': {'x': right_foot.x, 'y': right_foot.y},
            'distance': right_knee.y  # 右膝盖到右脚，取右膝盖
        }
        lines.append(right_knee_foot)

        # 排序
        lines.sort(key=lambda x: int(x['distance']))

        line_width = 10
        point_width = 10
        line_area = 200

        for line in lines:

            start = (line['start']['x'], line['start']['y'])
            end = (line['end']['x'], line['end']['y'])

            start_point = (start[0] - point_width // 2, start[1] - point_width // 2,
                           start[0] + point_width // 2, start[1] + point_width // 2)

            end_point = (end[0] - point_width // 2, end[1] - point_width // 2,
                         end[0] + point_width // 2, end[1] + point_width // 2)

            match line['name']:
                case 'left_eye_ear':
                    draw.line((start, end), fill=to_rgba(colors['left_eye_ear'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_eye'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_ear'], point_width)

                case 'right_eye_ear':
                    draw.line((start, end), fill=to_rgba(colors['right_eye_ear'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_eye'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_ear'], point_width)

                case 'left_eye_nose':
                    draw.line((start, end), fill=to_rgba(colors['left_eye_nose'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_eye'], point_width)
                    draw.arc(end_point, 0, 360, colors['nose'], point_width)

                case 'right_eye_nose':
                    draw.line((start, end), fill=to_rgba(colors['right_eye_nose'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_eye'], point_width)
                    draw.arc(end_point, 0, 360, colors['nose'], point_width)

                case 'nose_chest':
                    draw.line((start, end), fill=to_rgba(colors['nose_chest'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['nose'], point_width)
                    draw.arc(end_point, 0, 360, colors['chest'], point_width)

                case 'chest_left_shoulder':
                    draw.line((start, end), fill=to_rgba(colors['chest_left_shoulder'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['chest'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_shoulder'], point_width)

                case 'chest_right_shoulder':
                    draw.line((start, end), fill=to_rgba(colors['chest_right_shoulder'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['chest'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_shoulder'], point_width)

                case 'left_shoulder_elbow':
                    draw.line((start, end), fill=to_rgba(colors['left_shoulder_elbow'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_shoulder'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_elbow'], point_width)

                case 'right_shoulder_elbow':
                    draw.line((start, end), fill=to_rgba(colors['right_shoulder_elbow'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_shoulder'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_shoulder_elbow'], point_width)

                case 'left_elbow_hand':
                    draw.line((start, end), fill=to_rgba(colors['left_elbow_hand'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_elbow'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_hand'], point_width)

                case 'right_elbow_hand':
                    draw.line((start, end), fill=to_rgba(colors['right_elbow_hand'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_elbow'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_hand'], point_width)

                case 'chest_left_waist':
                    draw.line((start, end), fill=to_rgba(colors['chest_left_waist'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['chest'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_waist'], point_width)

                case 'chest_right_waist':
                    draw.line((start, end), fill=to_rgba(colors['chest_right_waist'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['chest'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_waist'], point_width)

                case 'left_waist_knee':
                    draw.line((start, end), fill=to_rgba(colors['left_waist_knee'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_waist'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_knee'], point_width)

                case 'right_waist_knee':
                    draw.line((start, end), fill=to_rgba(colors['right_waist_knee'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_waist'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_knee'], point_width)

                case 'left_knee_foot':
                    draw.line((start, end), fill=to_rgba(colors['left_knee_foot'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['left_knee'], point_width)
                    draw.arc(end_point, 0, 360, colors['left_foot'], point_width)

                case 'right_knee_foot':
                    draw.line((start, end), fill=to_rgba(colors['right_knee_foot'], line_area), width=line_width)
                    draw.arc(start_point, 0, 360, colors['right_knee'], point_width)
                    draw.arc(end_point, 0, 360, colors['right_foot'], point_width)

        return image
