import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

# ТВОЙ ТЕКСТ - МЕНЯЙ ТЕКСТ ТУТ
# start = секунда когда фраза должна начаться
SUBS = [
    {"start": 0.5, "text": "Почти три часа ночи. Тихая ночь."},
    {"start": 7.0, "text": "Ты слышишь как летит Герань."},
    {"start": 15.0, "text": "Это не просто звук. Это предупреждение."},
]

async def make_tts(text, out):
    com = edge_tts.Communicate(text, "ru-RU-DmitryNeural")
    await com.save(out)

async def main():
    print("Генерирую голос Дмитрия...")
    voice_clips = []
    for i, s in enumerate(SUBS):
        f = f"v{i}.mp3"
        await make_tts(s["text"], f)
        clip = AudioFileClip(f).set_start(s["start"])
        voice_clips.append(clip)

    video = VideoFileClip("shahed_video_v3.mp4")
    
    # ВАЖНО: Оставляем оригинальный звук видео + голос
    if video.audio:
        all_audio = CompositeAudioClip([video.audio] + voice_clips)
    else:
        all_audio = CompositeAudioClip(voice_clips)
        
    final = video.set_audio(all_audio)
    final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
    print("ГОТОВО! Файл output.mp4 создан с полным звуком")

asyncio.run(main())
