#!/usr/bin/env python3
"""Generate featured project cover images from real source snippets."""

import importlib
import subprocess
import sys
import textwrap
from pathlib import Path


def ensure(package, import_name=None):
    name = import_name or package
    try:
        return importlib.import_module(name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return importlib.import_module(name)


ensure("Pillow", "PIL")
ensure("Pygments", "pygments")

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token


WIDTH = 1200
HEIGHT = 630
PADDING = 48
NAVY = "#0a192f"
GREEN = "#64ffda"
SLATE = "#8892b0"
TEXT = "#ccd6f6"
CODE_BG = "#112240"


PROJECTS = [
    {
        "title": "SmartClean AI",
        "subtitle": "Hybrid ML data cleaner",
        "output": "smartclean.png",
        "source": "/Users/likithatadakala/Documents/Academic/Independent_Study/SmartClean_AI_Code/Project/run_smartclean_benchmark.py:163",
        "code": """def clean_price_with_shein_patterns(series, price_patterns):
    cleaned = series.copy()
    if 'price_ranges' in price_patterns:
        ranges = price_patterns['price_ranges']
        for idx in cleaned[cleaned.isnull()].index:
            price_range = random.choice(['budget', 'mid', 'premium'])
            mn, mx = ranges[price_range]
            new_price = np.random.uniform(mn, mx)
            if 'common_endings' in price_patterns and price_patterns['common_endings']:
                ending = random.choice(price_patterns['common_endings'])
                new_price = int(new_price) + float(ending)
            cleaned.iloc[idx] = f"${new_price:.2f}"
    return cleaned


def clean_title_with_shein_patterns(series, title_patterns):
    cleaned = series.copy()
    adjectives = title_patterns.get('common_adjectives', ['Quality', 'Premium', 'Professional'])
    descriptors = title_patterns.get('common_descriptors', ['Product', 'Item', 'Design'])
    for idx in cleaned[cleaned.isnull()].index:
        cleaned.iloc[idx] = f"{random.choice(adjectives)} {random.choice(descriptors)} - High Quality Product"
    return cleaned""",
    },
    {
        "title": "YouTube Learning Chatbot",
        "subtitle": "Offline RAG for YouTube transcripts",
        "output": "youtube-rag.png",
        "source": "/tmp/portfolio-sources/AI_Chatbot/Code/src/handlers/yt_handler.py:17",
        "code": """def get_transcript(self):
    \"\"\"Fetches the transcript of the YouTube video.\"\"\"
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(self.video_id)
        return transcript_list
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return str(e)

def get_transcript_string(self) -> str:
    \"\"\"Fetches and returns the transcript as a formatted string.\"\"\"
    transcript_list = self.get_transcript()
    if isinstance(transcript_list, str):
        return transcript_list  # Error message

    return ' '.join([t['text'] for t in transcript_list])

def get_formatted_transcript(self) -> str:
    \"\"\"Returns transcript formatted with timestamps for easy processing.\"\"\"""",
    },
    {
        "title": "Vision For The Blind",
        "subtitle": "Edge AI assistive device",
        "output": "vision.png",
        "source": "/tmp/portfolio-sources/VISION/Visual_Insight_Solution_Interface_Outreach_Navigator_VISION.py:205",
        "code": """save_frames = True
print("Capturing image...")
if save_frames:
    frame_count += 1
    image_path = f"frame_{frame_count}.jpg"
    cv2.imwrite(image_path, frame)
    # Perform prediction on the captured frame
    predicted_class_name = predict_image(frame, model)
    print("Predicted class:", predicted_class_name)
    # Speak the predicted class name
    engine.say(predicted_class_name)
    engine.runAndWait()
    os.remove(image_path)
    # Display the predicted class on the frame
    cv2.putText(
        frame,
        predicted_class_name,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )""",
    },
]


def load_font(size):
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def token_color(style, token_type):
    while token_type not in style and token_type is not Token:
        token_type = token_type.parent
    color = style.style_for_token(token_type).get("color")
    return f"#{color}" if color else TEXT


def wrap_code(code, max_chars=88):
    wrapped = []
    for line in code.splitlines():
        if len(line) <= max_chars:
            wrapped.append(line)
            continue
        indent = len(line) - len(line.lstrip(" "))
        chunks = textwrap.wrap(
            line,
            width=max_chars,
            subsequent_indent=" " * (indent + 4),
            break_long_words=False,
            break_on_hyphens=False,
        )
        wrapped.extend(chunks or [line])
    return "\n".join(wrapped)


def draw_code(draw, code, xy, font, line_height):
    style = get_style_by_name("monokai")
    x, y = xy
    cursor_x = x
    cursor_y = y
    space_width = draw.textlength(" ", font=font)

    for token_type, value in lex(code, PythonLexer()):
        color = token_color(style, token_type)
        parts = value.split("\n")
        for index, part in enumerate(parts):
            if index:
                cursor_x = x
                cursor_y += line_height
            if part:
                draw.text((cursor_x, cursor_y), part, fill=color, font=font)
                cursor_x += draw.textlength(part, font=font)
        if value.endswith(" "):
            cursor_x += space_width


def render(project):
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)

    title_font = load_font(28)
    subtitle_font = load_font(16)
    code_font = load_font(20)
    source_font = load_font(13)

    draw.text((PADDING, PADDING), project["title"], fill=GREEN, font=title_font)
    draw.text((PADDING, PADDING + 42), project["subtitle"], fill=SLATE, font=subtitle_font)

    code_top = PADDING + 86
    code_left = PADDING
    code_right = WIDTH - PADDING
    code_bottom = HEIGHT - PADDING - 28
    draw.rounded_rectangle(
        (code_left, code_top, code_right, code_bottom),
        radius=8,
        fill=CODE_BG,
        outline="#233554",
        width=1,
    )

    wrapped = wrap_code(project["code"])
    draw_code(draw, wrapped, (code_left + 24, code_top + 24), code_font, 28)
    draw.text((PADDING, HEIGHT - PADDING - 12), project["source"], fill="#526175", font=source_font)

    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    image.save(out_dir / project["output"])


def main():
    for project in PROJECTS:
        render(project)


if __name__ == "__main__":
    main()
