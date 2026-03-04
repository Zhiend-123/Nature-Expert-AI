import pickle
import os
from exif import Image as ExifImage

HISTORY_FILE = "data_history.pkl"


def get_exif_coords(image_file):
    """Извлекает GPS-координаты из EXIF данных фото"""
    try:
        image_file.seek(0)
        img = ExifImage(image_file)
        if img.has_exif and hasattr(img, 'gps_latitude') and hasattr(img, 'gps_longitude'):
            # Конвертация из градусов/минут/секунд в десятичный формат
            def to_decimal(coords, ref):
                decimal = coords[0] + coords[1] / 60 + coords[2] / 3600
                if ref in ['S', 'W']: decimal = -decimal
                return decimal

            lat = to_decimal(img.gps_latitude, img.gps_latitude_ref)
            lon = to_decimal(img.gps_longitude, img.gps_longitude_ref)
            return lat, lon
    except Exception:
        return None
    return None
def save_history(history_list):
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(history_list, f)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            return []
    return []

def clear_history_file():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def delete_entry_from_file(index):
    """Удаляет запись по индексу и перезаписывает файл"""
    history = load_history()
    if 0 <= index < len(history):
        history.pop(index)
        save_history(history)
        return history
    return history