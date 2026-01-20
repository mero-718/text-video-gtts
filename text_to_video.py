from PIL import ImageFont, ImageDraw, Image
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
import argparse
from pydub import AudioSegment
import colorsys
import numpy as np
import os

# Variables for customization
TEXT_SPEED = 24  # frames per second
TEXT_COLOR = (255, 255, 255)
FONT_PATH = "DMSerifDisplay-Regular.ttf" # Path to .ttf font file (change this to your font file)
FONT_SIZE = 180
BACKGROUND_SPEED = 0.8  # Background color change speed (lower value means slower)
TIMING_ADJUSTMENT = -0.3  # Adjusts the duration of each word in the video
START_BG_COLOR = "#000000"  # Start color in HEX
END_BG_COLOR = "#6638f3"  # End color in HEX


# Function to convert HEX color to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# interpolate color
def interpolate_color(start_color, end_color, progress):
    start_color = hex_to_rgb(start_color)
    end_color = hex_to_rgb(end_color)

    start_h, start_s, start_v = colorsys.rgb_to_hsv(
        start_color[0] / 255, start_color[1] / 255, start_color[2] / 255
    )
    end_h, end_s, end_v = colorsys.rgb_to_hsv(
        end_color[0] / 255, end_color[1] / 255, end_color[2] / 255
    )

    interpolated_h = start_h + (end_h - start_h) * progress
    interpolated_s = start_s + (end_s - start_s) * progress
    interpolated_v = start_v + (end_v - start_v) * progress

    r, g, b = colorsys.hsv_to_rgb(interpolated_h, interpolated_s, interpolated_v)

    return int(r * 255), int(g * 255), int(b * 255)


def text_to_video(textfile, outputfile):
    with open(textfile, "r") as f:
        lines = f.read()

    words = lines.split()
    images = []
    durations = []

    fnt = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Generate speech for the whole text and save as a temporary file
    tts = gTTS(text=lines, lang="en")
    tts.save("temp.mp3")

    # Measure the speech duration using pydub
    full_audio = AudioSegment.from_file("temp.mp3")
    full_audio_duration = len(full_audio) / 1000  # duration in seconds
    avg_word_duration = full_audio_duration / len(words)  # average duration per word
    # Inside your text_to_video function, when setting frame duration:
    durations.append(
        avg_word_duration + TIMING_ADJUSTMENT
    )  # Adjust frame duration based on average word duration and timing adjustment

    for i, word in enumerate(words):
        # Calculate text size and position only once per word
        text_width, text_height = fnt.getsize(word)
        position = ((VIDEO_SIZE[0] - text_width) / 2, (VIDEO_SIZE[1] - text_height) / 2)

        # Calculate background color based on word index and total number of words
        background_progress = i / len(words)
        background_color = interpolate_color(
            START_BG_COLOR, END_BG_COLOR, background_progress
        )

        img = Image.new(
            "RGB", VIDEO_SIZE, color=background_color
        )  # Set background color
        d = ImageDraw.Draw(img)
        d.text(position, word, font=fnt, fill=TEXT_COLOR)

        images.append(np.array(img))
        durations.append(
            avg_word_duration
        )  # Set frame duration based on average word duration

    audioclip = AudioFileClip("temp.mp3")
    clip = ImageSequenceClip(images, durations=durations)
    clip = clip.set_audio(audioclip)

    clip.fps = TEXT_SPEED
    clip.write_videofile(outputfile, codec="libx264")

    # Remove the temporary file
    os.remove("temp.mp3")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text file to video")
    parser.add_argument("textfile", help="The name of the text file to convert")
    parser.add_argument("outputfile", help="The name of the output mp4 file")
    parser.add_argument(
        "--format-short",
        action="store_true",
        help="Set this flag if you want a short video",
    )
    args = parser.parse_args()

    VIDEO_SHORT = args.format_short
    VIDEO_SIZE = (1080, 1920) if VIDEO_SHORT else (1920, 1080)  # width, height

    text_to_video(args.textfile, args.outputfile)