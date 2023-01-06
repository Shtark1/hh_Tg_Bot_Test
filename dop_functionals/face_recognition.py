from deepface import DeepFace
import pathlib


async def face_analyze(photo):
    try:
        result_dict = DeepFace.analyze(img_path=photo, actions=['age', 'gender', 'race', 'emotion'])
        return [result_dict.get("age"), result_dict.get("gender"), result_dict.get('race'), result_dict.get('emotion')]

    except Exception as _ex:
        file = pathlib.Path(photo)
        file.unlink()
        return "На этом фото нет лица человека!"
