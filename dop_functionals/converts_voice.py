import os


async def converts_wav(audio_path, output_name):
    output_name = output_name + '.wav'
    os.system("ffmpeg -i " + audio_path + " -ac 1 -ar 16000" + " " + output_name)
