import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

GENERATED_FOLDER = os.path.join(os.getcwd(), "generated")
os.makedirs(GENERATED_FOLDER, exist_ok=True)

app.config["GENERATED_FOLDER"] = GENERATED_FOLDER


def draw_text_with_outline(draw, text, position, font, fill="white", outline="black", outline_width=2):
    
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def create_meme(image_path, top_text, bottom_text, output_path):
   
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    draw = ImageDraw.Draw(img)

    font_size = int(height / 10)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    if top_text:
        top_text = top_text.upper()
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        top_x = (width - text_width) / 2
        top_y = 10
        draw_text_with_outline(draw, top_text, (top_x, top_y), font)

    if bottom_text:
        bottom_text = bottom_text.upper()
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        bottom_x = (width - text_width) / 2
        bottom_y = height - text_height - 10
        draw_text_with_outline(draw, bottom_text, (bottom_x, bottom_y), font)

    img.save(output_path, format="JPEG")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        top_text = request.form.get("top_text", "")
        bottom_text = request.form.get("bottom_text", "")

        if not file or file.filename == "":
            return render_template("index.html", error="Prosimo, naloži sliko.")

        original_filename = f"upload_{uuid.uuid4().hex}.jpg"
        original_path = os.path.join(app.config["GENERATED_FOLDER"], original_filename)
        file.save(original_path)

        meme_filename = f"meme_{uuid.uuid4().hex}.jpg"
        meme_path = os.path.join(app.config["GENERATED_FOLDER"], meme_filename)

        create_meme(original_path, top_text, bottom_text, meme_path)

        return redirect(url_for("show_meme", filename=meme_filename))

    return render_template("index.html")


@app.route("/meme/<filename>")
def show_meme(filename):
    meme_url = url_for("generated_file", filename=filename)
    return render_template("index.html", meme_url=meme_url)


@app.route("/generated/<filename>")
def generated_file(filename):
    return send_from_directory(app.config["GENERATED_FOLDER"], filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)