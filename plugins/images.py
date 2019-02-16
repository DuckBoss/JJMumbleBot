from templates.plugin_template import PluginBase
import requests
import utils
import os
import urllib.request
from urllib.parse import quote
import urllib
from bs4 import BeautifulSoup
from PIL import Image
from binascii import b2a_base64
import time
import shutil


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Images Plugin Help <font color='red'>#####</font></b><br> \
                        All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!post 'image_url'</b>: Posts the image from the url in the channel chat.<br>\
                        <b>!img 'image_name'</b>: Posts locally hosted images in the channel chat. The image must be a jpg.<br>\
                        <b>!imglist</b>: Lists all locally hosted images."

    def __init__(self):
        print("Images Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "post":
            img_url = message_parse[1]
            # Download image
            img_url = ''.join(BeautifulSoup(img_url, 'html.parser').findAll(text=True))
            self.download_image_urllib(img_url)
            # Format image
            time.sleep(1)
            img_ext = img_url.rsplit('.', 1)[1]
            formatted_string = self.format_image("image", img_ext, utils.get_temporary_img_dir())

            # print(formatted_string)
            # print("%d characters" % len(formatted_string))
            print("Posting to mumble!")
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       '%s' % formatted_string)
            return

        elif command == "img":
            parameter = message_parse[1]
            # Format image
            img_data = parameter.rsplit('.', 1)
            formatted_string = self.format_image(img_data[0], "jpg", utils.get_permanent_media_dir()+"images/")
            print("Posting to mumble!")
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       '%s' % formatted_string)
            return

        elif command == "imglist":
            file_counter = 0
            internal_list = []

            for file in os.listdir(utils.get_permanent_media_dir() + "images/"):
                if file.endswith(".jpg"):
                    internal_list.append(
                        "<br><font color='cyan'>[%d]:</font> <font color='yellow'>%s</font>" % (file_counter, file))
                    file_counter += 1

            cur_text = "<br><font color='red'>Local Image Files</font>"
            for i in range(len(internal_list)):
                cur_text += internal_list[i]
                if i % 50 == 0 and i != 0:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               '%s' % cur_text)
                    cur_text = ""
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       '%s' % cur_text)
            return

    def mid(self, text, begin, length):
        return text[begin:begin+length]

    def format_image_html(self, img_ext, byte_arr):
        if img_ext == "jpg":
            img_ext = "JPEG"
        elif img_ext == "jpeg":
            img_ext = "JPEG"
        elif img_ext == "png":
            img_ext = "PNG"

        raw_base = self.encode_b64(byte_arr)
        encoded = []
        i = 0
        begin = 0
        end = 0

        begin = i * 72
        end = i * 72
        mid_raw_base = self.mid(raw_base, begin, 72)
        encoded.append(quote(mid_raw_base, safe=''))
        i += 1
        while end < len(raw_base):
            begin = i * 72
            end = i * 72
            mid_raw_base = self.mid(raw_base, begin, 72)
            encoded.append(quote(mid_raw_base, safe=''))
            i += 1

        return "<img src='data:image/%s;base64,%s' />" % (img_ext, ''.join(encoded))

    def format_image(self, img_name, img_ext, img_dir):
        # Open image
        img = Image.open("%s%s.%s" % (img_dir, img_name, img_ext))
        img.load()
        img_width = img.size[0]
        img_height = img.size[1]
        # Scale image down with aspect ratio
        if img_width > 480 or img_height > 270:
            img.thumbnail((480, 270), Image.ANTIALIAS)
        # Save and close image
        img.save("%s%s.%s" % (img_dir, img_name, img_ext))
        img.close()
        # Convert image to byte array
        with open("%s%s.%s" % (img_dir, img_name, img_ext), "rb") as img_read:
            img_data = img_read.read()
            img_byte_arr = bytearray(img_data)
        # Keep lowering quality until it fits within the size restrictions.
        img_quality = 100
        while len(img_byte_arr) >= 65536 and img_quality > 0:
            img_byte_arr.clear()
            with open("%s%s.%s" % (img_dir, img_name, img_ext), "rb") as img_file:
                img_data = img_file.read()
                img_byte_arr = bytearray(img_data)
            img = Image.open("%s%s.%s" % (img_dir, img_name, img_ext))
            img.save("%s%s.%s" % (img_dir, img_name, img_ext), quality=img_quality)
            img.close()
            img_quality -= 10
        if len(img_byte_arr) < 65536:
            # return formatted html img string
            return self.format_image_html(img_ext=img_ext, byte_arr=img_byte_arr)
        return ""

    def encode_b64(self, byte_arr):
        encvec = []
        eol = '\n'
        max_unencoded = 76 * 3 // 4
        s = byte_arr
        for i in range(0, len(s), max_unencoded):
            # BAW: should encode() inherit b2a_base64()'s dubious behavior in
            # adding a newline to the encoded string?
            enc = b2a_base64(s[i:i + max_unencoded]).decode("ascii")
            if enc.endswith('\n') and eol != '\n':
                enc = enc[:-1] + eol
            encvec.append(enc)

        b64_img = ''.join(encvec)
        return b64_img

    def download_image_requests(self, img_url):
        utils.clear_directory(utils.get_temporary_img_dir())
        img_ext = img_url.rsplit('.', 1)[1]
        s = requests.Session()
        r = s.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open("image.%s" % img_ext, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print("Downloaded image from: %s" % img_url)
        else:
            print("403 Error!")

    def download_image_urllib(self, img_url):
        utils.clear_directory(utils.get_temporary_img_dir())
        img_ext = img_url.rsplit('.', 1)[1]
        urllib.request.urlretrieve(img_url, "%simage.%s" % (utils.get_temporary_img_dir(), img_ext))
        print("Downloaded image from: %s" % img_url)

    def download_image_stream(self, img_url):
        utils.clear_directory(utils.get_temporary_img_dir())
        img_ext = img_url.rsplit('.', 1)[1]
        with open('%simage.%s' % (utils.get_temporary_img_dir(), img_ext), 'wb') as img_file:
            resp = requests.get(img_url, stream=True)
            for block in resp.iter_content(1024):
                if not block:
                    break
                img_file.write(block)
        print("Downloaded image from: %s" % img_url)

    def plugin_test(self):
        print("Images Plugin self-test callback.")

    def quit(self):
        print("Exiting Images Plugin...")

    def help(self):
        return self.help_data
