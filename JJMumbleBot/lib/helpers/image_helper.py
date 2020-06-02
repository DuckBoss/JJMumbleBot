from JJMumbleBot.lib.utils.print_utils import dprint
from urllib.parse import quote
from PIL import Image
from binascii import b2a_base64
import requests
import shutil
import os
from JJMumbleBot.lib.utils import dir_utils


def mid(text, begin, length):
    return text[begin:begin + length]


def format_image_html(img_ext, byte_arr):
    if img_ext == "jpg":
        img_ext = "JPEG"
    elif img_ext == "jpeg":
        img_ext = "JPEG"
    elif img_ext == "png":
        img_ext = "PNG"

    raw_base = encode_b64(byte_arr)
    encoded = []
    i = 0

    begin = i * 72
    end = i * 72
    mid_raw_base = mid(raw_base, begin, 72)
    encoded.append(quote(mid_raw_base, safe=''))
    i += 1
    while end < len(raw_base):
        begin = i * 72
        end = i * 72
        mid_raw_base = mid(raw_base, begin, 72)
        encoded.append(quote(mid_raw_base, safe=''))
        i += 1
    return f"<img src='data:image/{img_ext};base64,{''.join(encoded)}' />"


def format_image(img_name: str, img_ext: str, img_dir: str, size_goal=65536, raw=False, max_width=480, max_height=270):
    # Convert to JPG if it's PNG
    img = Image.open(f"{img_dir}/{img_name}.{img_ext}")
    if img_ext.upper() == 'PNG':
        img.convert('RGB').save(f'{img_dir}/{img_name}.jpg', 'JPEG')
        img_ext = 'jpg'
    # Open images
    img = Image.open(f"{img_dir}/{img_name}.{img_ext}")
    img.load()

    img_width = img.size[0]
    img_height = img.size[1]
    # Scale images down with aspect ratio
    if img_width > max_width or img_height > max_height:
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    # Save and close images
    img.save(f"{img_dir}/{img_name}.{img_ext}")
    img.close()
    # Convert images to byte array
    with open(f"{img_dir}/{img_name}.{img_ext}", "rb") as img_read:
        img_data = img_read.read()
        img_byte_arr = bytearray(img_data)
    # Keep lowering quality until it fits within the size restrictions.
    img_quality = 100
    while len(img_byte_arr) >= size_goal and img_quality > 0:
        img_byte_arr.clear()
        with open(f"{img_dir}/{img_name}.{img_ext}", "rb") as img_file:
            img_data = img_file.read()
            img_byte_arr = bytearray(img_data)
        img = Image.open(f"{img_dir}/{img_name}.{img_ext}")
        img.save(f"{img_dir}/{img_name}.{img_ext}", quality=img_quality)
        img.close()
        img_quality -= 10
    if len(img_byte_arr) < size_goal:
        # delete jpg if generated from png
        if os.path.isfile(f"{img_dir}/{img_name}.png"):
            os.unlink(f"{img_dir}/{img_name}.jpg")
        if raw:
            return img_byte_arr
        # return formatted html img string
        return format_image_html(img_ext=img_ext, byte_arr=img_byte_arr)
    return ""


def encode_b64(byte_arr):
    encvec = []
    eol = '\n'
    max_unencoded = 76 * 3 // 4
    s = byte_arr
    for i in range(0, len(s), max_unencoded):
        enc = b2a_base64(s[i:i + max_unencoded]).decode("ascii")
        if enc.endswith('\n') and eol != '\n':
            enc = enc[:-1] + eol
        encvec.append(enc)

    b64_img = ''.join(encvec)
    return b64_img


def download_image_requests(img_url):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/internal/images')
    img_ext = img_url.rsplit('.', 1)[1]
    s = requests.Session()
    r = s.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        with open(f"{dir_utils.get_temp_med_dir()}/internal/images/_image.{img_ext}", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        dprint(f"Downloaded image from: {img_url}")
    else:
        dprint(f"{r.status_code} Error! - {img_url}")


def download_image_stream(img_url):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/internal/images')
    img_ext = img_url.rsplit('.', 1)[1]
    with open(f"{dir_utils.get_temp_med_dir()}/internal/images/_image.{img_ext}", 'wb') as img_file:
        resp = requests.get(img_url, stream=True)
        for block in resp.iter_content(1024):
            if not block:
                break
            img_file.write(block)
    dprint(f"Downloaded image from: {img_url}")


def download_image_stream_to_dir(img_url, dir_name):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    img_ext = img_url.rsplit('.', 1)[1]
    with open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}", 'wb') as img_file:
        resp = requests.get(img_url, stream=True)
        for block in resp.iter_content(1024):
            if not block:
                break
            img_file.write(block)
    if img_ext == 'png':
        dprint(f"Fixing image to force jpg conversion: {img_url}")
        img_fix = Image.open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}")
        img_fix.convert('RGB').save(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.jpg")
        dir_utils.remove_file("_image.png", f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    dprint(f"Downloaded image from: {img_url}")


def download_image_requests_to_dir(img_url, dir_name):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    img_ext = img_url.rsplit('.', 1)[1]
    s = requests.Session()
    r = s.get(img_url)
    if r.status_code == 200:
        with open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        dprint(f"Downloaded image from: {img_url}")
    else:
        dprint(f"{r.status_code} Error! - {img_url}")
    if img_ext == 'png':
        dprint(f"Fixing image to force jpg conversion: {img_url}")
        img_fix = Image.open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}")
        img_fix.convert('RGB').save(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.jpg")
        dir_utils.remove_file("_image.png", f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    dprint(f"Downloaded image from: {img_url}")
