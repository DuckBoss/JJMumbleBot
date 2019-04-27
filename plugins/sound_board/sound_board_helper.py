import utils
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print
import wave
import youtube_dl
import time
import audioop
import subprocess as sp


class SoundBoardHelper:
    exit_flag = False
    current_song = None
    audio_thread = None
    # default volume
    volume = 0.5


def stop_audio():
    if SoundBoardHelper.audio_thread is not None:
        debug_print("Stopping sound_board audio thread...")
        SoundBoardHelper.audio_thread.terminate()
        SoundBoardHelper.audio_thread.kill()
        SoundBoardHelper.audio_thread = None
        SoundBoardHelper.current_song = None
        return True
    return False


def get_cur_audio_length():
    wav_file = wave.open(f"{utils.get_permanent_media_dir()}/sound_board/{SoundBoardHelper.current_song}.wav", 'r')
    frames = wav_file.getnframes()
    rate = wav_file.getframerate()
    duration = frames / float(rate)
    wav_file.close()
    return duration


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': utils.get_permanent_media_dir() + f'sound_board/{name}.wav',
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return True
    except Exception:
        return False


def play_audio():
    GM.mumble.sound_output.clear_buffer()

    uri = f"file:///{utils.get_permanent_media_dir()}/sound_board/{SoundBoardHelper.current_song}.wav"
    command = utils.get_vlc_dir()

    GM.mumble.sound_output.clear_buffer()

    if SoundBoardHelper.audio_thread is not None:
        SoundBoardHelper.audio_thread.terminate()
        SoundBoardHelper.audio_thread.kill()
        SoundBoardHelper.audio_thread = None

    if SoundBoardHelper.audio_thread is None:
        SoundBoardHelper.audio_thread = sp.Popen(
            [command, uri] + ['-I', 'dummy', '--quiet', '--one-instance', '--no-repeat', '--sout',
                              '#transcode{acodec=s16le, channels=2, samplerate=24000, '
                              'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                              'vlc://quit'],
            stdout=sp.PIPE, bufsize=480)

    utils.unmute()
    while not SoundBoardHelper.exit_flag and SoundBoardHelper.audio_thread:
        while GM.mumble.sound_output.get_buffer_size() > 0.5 and not SoundBoardHelper.exit_flag:
            time.sleep(0.01)
        if SoundBoardHelper.audio_thread:
            raw_music = SoundBoardHelper.audio_thread.stdout.read(480)
            if raw_music and SoundBoardHelper.audio_thread:
                GM.mumble.sound_output.add_sound(audioop.mul(raw_music, 2, SoundBoardHelper.volume))
            else:
                return
        else:
            return
    return
