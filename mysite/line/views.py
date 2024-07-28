from django.shortcuts import render

from django.http import HttpResponse, FileResponse
from django.utils.datastructures import MultiValueDictKeyError

from .models import LineText
from django.utils import timezone
import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw
import os, re
from django.conf import settings


def index(request):
    latest_text_list = LineText.objects.order_by("-pub_date")[:5]
    context = {"latest_text_list": latest_text_list}
    try:
        text_to_video = request.GET["text"]
    except MultiValueDictKeyError:
        return render(request, "line/index.html", context)
    else:
        for f in os.listdir(settings.BASE_DIR):
            if re.search("\d*_video.mp4", f):
                os.remove(os.path.join(settings.BASE_DIR, f))
        if text_to_video:
            line = LineText(line_text=text_to_video, pub_date=timezone.now())
            line.save()

            width, height, fps, time = (100, 100, 24, 3)
            out_video = cv2.VideoWriter(os.path.join(settings.BASE_DIR, f"{str(line.id)}_video.mp4"),
                                        cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            x, y = width, height // 4
            font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "Uni_Sans_Heavy.otf"), height - height // 4)
            for t in range(fps * time):
                img_with_text = Image.new(mode="RGB", size=(width, height), color=(209, 123, 193))
                x -= (font.getlength(text_to_video) + font.getlength(text_to_video[0])) / (fps * time)
                draw = ImageDraw.Draw(img_with_text)
                draw.text((x, y), text_to_video, (255, 255, 255), font=font)
                frame = cv2.cvtColor(np.array(img_with_text), cv2.COLOR_RGB2BGR)
                out_video.write(frame)
            out_video.release()
            response = FileResponse(open(os.path.join(settings.BASE_DIR, f"{str(line.id)}_video.mp4"), 'rb'),
                                    as_attachment=True)
            return response
