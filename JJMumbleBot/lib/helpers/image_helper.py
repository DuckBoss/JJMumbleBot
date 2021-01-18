from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import INFO, ERROR, WARNING, L_GENERAL, WARN_INVALID_IMG_FORMAT,\
    WARN_FIXED_IMG_FORMAT, GEN_PROCESS_ERR
from JJMumbleBot.lib.resources.log_strings import INFO_IMG_DOWNLOADED, INFO_IMG_HTML_FORMATTED, \
    WARN_IMG_INCORRECT_FORMAT, WARN_IMG_CONVERTED, INFO_IMG_RAW_FORMATTED
from urllib.parse import quote
from PIL import Image
from binascii import b2a_base64
import requests
import shutil
import os
from JJMumbleBot.lib.utils import dir_utils


def mid(text, begin, length):
    return text[begin:begin + length]


def format_image_html(img_ext, byte_arr, quiet=False):
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
    if not quiet:
        log(INFO, INFO_IMG_HTML_FORMATTED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
    return f"<img src='data:image/{img_ext};base64,{''.join(encoded)}' />"


def format_image(img_name: str, img_ext: str, img_dir: str, size_goal=65536, raw=False, max_width=480, max_height=270, quiet=False):
    # Convert to JPG if it's PNG
    img = Image.open(f"{img_dir}/{img_name}.{img_ext}")
    if img_ext.upper() == 'PNG':
        img.convert('RGB').save(f'{img_dir}/{img_name}.jpg', 'JPEG')
        img_ext = 'jpg'
        if not quiet:
            log(WARNING, WARN_IMG_INCORRECT_FORMAT, origin=L_GENERAL,
                error_type=WARN_INVALID_IMG_FORMAT, print_mode=PrintMode.VERBOSE_PRINT.value)
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
    # delete jpg if generated from png
    if os.path.isfile(f"{img_dir}/{img_name}.png"):
        os.unlink(f"{img_dir}/{img_name}.jpg")
        if not quiet:
            log(WARNING, WARN_IMG_CONVERTED, origin=L_GENERAL,
                error_type=WARN_FIXED_IMG_FORMAT, print_mode=PrintMode.VERBOSE_PRINT.value)
    if raw:
        if not quiet:
            log(INFO, INFO_IMG_RAW_FORMATTED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
        return img_byte_arr
    # return formatted html img string
    return format_image_html(img_ext=img_ext, byte_arr=img_byte_arr, quiet=quiet)


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
        log(INFO, INFO_IMG_DOWNLOADED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
    else:
        log(
            ERROR,
            f"ERROR: Encountered a Requests Module error while trying to download an image - {r.status_code} - {img_url}",
            origin=L_GENERAL,
            error_type=GEN_PROCESS_ERR,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )


def download_image_stream(img_url):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/internal/images')
    img_ext = img_url.rsplit('.', 1)[1]
    with open(f"{dir_utils.get_temp_med_dir()}/internal/images/_image.{img_ext}", 'wb') as img_file:
        resp = requests.get(img_url, stream=True)
        for block in resp.iter_content(1024):
            if not block:
                break
            img_file.write(block)
    log(INFO, INFO_IMG_DOWNLOADED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)


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
        log(WARNING, WARN_IMG_INCORRECT_FORMAT, origin=L_GENERAL,
            error_type=WARN_FIXED_IMG_FORMAT, print_mode=PrintMode.VERBOSE_PRINT.value)
        img_fix = Image.open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}")
        img_fix.convert('RGB').save(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.jpg")
        dir_utils.remove_file("_image.png", f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    log(INFO, INFO_IMG_DOWNLOADED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)


def download_image_requests_to_dir(img_url, dir_name):
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{dir_name}')
    img_ext = img_url.rsplit('.', 1)[1]
    s = requests.Session()
    r = s.get(img_url)
    if r.status_code == 200:
        with open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        log(INFO, INFO_IMG_DOWNLOADED, origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
    else:
        log(
            ERROR,
            f"ERROR: Encountered a Requests Module error while trying to download an image - {r.status_code} - {img_url}",
            origin=L_GENERAL,
            error_type=GEN_PROCESS_ERR,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
    if img_ext == 'png':
        log(WARNING, WARN_IMG_INCORRECT_FORMAT, origin=L_GENERAL,
            error_type=WARN_FIXED_IMG_FORMAT, print_mode=PrintMode.VERBOSE_PRINT.value)
        img_fix = Image.open(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.{img_ext}")
        img_fix.convert('RGB').save(f"{dir_utils.get_temp_med_dir()}/{dir_name}/_image.jpg")
        dir_utils.remove_file("_image.png", f'{dir_utils.get_temp_med_dir()}/{dir_name}')
