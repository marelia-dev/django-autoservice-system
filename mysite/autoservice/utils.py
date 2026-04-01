from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO


def resize_and_crop_photo(image_field, size=300):
    """
    Apkerpa iki kvadrato
    """
    if not image_field:
        return image_field

    img = Image.open(image_field)

    # konvertuoja i RGB
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Оapkerpam i kvadrata ir centruojama
    width, height = img.size
    min_side = min(width, height)

    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side

    img = img.crop((left, top, right, bottom))

    # Sumazinam
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # saugom i atminti
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)

    # sukuriam nauja failo pavadinima
    new_name = os.path.splitext(image_field.name)[0] + '.jpg'

    # keiciame lauke
    image_field.save(new_name, ContentFile(output.read()), save=False)

    return image_field