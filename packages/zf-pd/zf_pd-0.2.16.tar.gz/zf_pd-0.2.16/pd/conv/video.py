from collections import namedtuple
from os import path as os_path

from loguru import logger
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment

Metadata = namedtuple("Metadata", ["fps", "width", "height"])


def webm(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == "mp3":
        try:
            webm_video_to_mp3(src, dst)
        except Exception as e:
            logger.debug(f"Failed to convert {src} to {dst} as video, retrying as audio")
            webm_audio_to_mp3(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def webm_video_to_mp3(src: str, dst: str) -> None:
    video = VideoFileClip(src)
    audio = video.audio
    audio.write_audiofile(dst)
    return


def webm_audio_to_mp3(src: str, dst: str) -> None:
    audio = AudioFileClip(src)
    audio.write_audiofile(dst)
    return


def mov(src: str, dst: str, quality: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == "mp3":
        try:
            mov_video_to_mp3(src, dst)
        except Exception as _:
            logger.debug(f"Failed to convert {src} to {dst} as video, retrying as audio")
            mov_audio_to_mp3(src, dst)
    elif dst_format == "gif":
        mov_to_gif(src, dst, quality)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def mov_video_to_mp3(src: str, dst: str) -> None:
    video = VideoFileClip(src)
    audio = video.audio
    audio.write_audiofile(dst)
    return


def mov_audio_to_mp3(src: str, dst: str) -> None:
    audio = AudioFileClip(src)
    audio.write_audiofile(dst)
    return

def mov_to_gif(src: str, dst: str, quality: str) -> None:
    metadata = get_metadata(src)
    logger.info(f"{src} has {metadata.width}x{metadata.height} resolution at {metadata.fps} fps")

    target_fps = get_target_fps(quality)
    target_width, target_height = get_target_res(metadata, quality)

    logger.info(f"Converting {src} to {dst} at {target_width}x{target_height} with {target_fps} fps")

    clip = VideoFileClip(filename=src, target_resolution=(target_height, target_width))
    clip.write_gif(dst, fps=target_fps)
    return


def mp4(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == "mp3":
        mp4_to_mp3(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def mp4_to_mp3(src: str, dst: str) -> None:
    video = VideoFileClip(src)
    audio = video.audio
    audio.write_audiofile(dst)
    return

def get_metadata(src: str) -> Metadata:
    with VideoFileClip(src) as clip:
        return Metadata(clip.fps, clip.size[0], clip.size[1])

def get_target_fps(quality: str) -> float:
    match quality:
        case "low":
            return 1
        case "medium":
            return 3
        case "high":
            return 5
        case _:
            return 3

def get_target_res(md: Metadata, quality: str) -> tuple[float, float]:
    scale = 1.0
    match quality:
        case "low":
            scale = 0.2
        case "medium":
            scale = 0.5
        case "high":
            scale = 0.75
        case _:
            scale = 0.5

    return int(md.width * scale), int(md.height * scale)
