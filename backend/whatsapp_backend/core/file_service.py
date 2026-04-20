import os
import uuid
from django.conf import settings

def save_file(file):

    ext = file.name.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{ext}"

    file_path = os.path.join(settings.MEDIA_ROOT, "profile_pics", file_name)

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return f"{settings.MEDIA_URL}profile_pics/{file_name}"