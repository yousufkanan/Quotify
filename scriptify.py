from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

def make_just_girly_things_image(
    quote,
    output_path='output.jpg'
):
    if quote[0] in ['"', ">"]:
        quote = quote[1:]
    if quote[-1] in ['"', "<"]:
        quote = quote[:-1]
    # Randomly select an image ID
    image_id = random.randint(0, 9999)
    print(f"Image ID: {image_id}")

    # Set the correct background image path (no trailing comma)
    background_path = f'backgrounds/gradient_{image_id}.png'
    font_path = 'Dancing_Script/static/DancingScript-Regular.ttf'

    # Load image and force it to 768x768 (assumes background image is high-enough resolution)
    image = Image.open(background_path).convert("RGBA")
    image = image.resize((768, 768))
    draw = ImageDraw.Draw(image)

    # Increase the font size for better visibility
    font_size = 72
    font = ImageFont.truetype(font_path, font_size)

    # Process the quote: if there are line breaks, wrap each line separately.
    lines = quote.splitlines()  # Preserve manual line breaks
    wrapped_lines = []
    for line in lines:
        # Wrap lines longer than 30 characters
        if len(line) > 30:
            wrapped_lines.append(textwrap.fill(line, width=30))
        else:
            wrapped_lines.append(line)
    wrapped_text = "\n".join(wrapped_lines)

    # Get image dimensions (should be 768x768 now)
    width, height = image.size

    # Measure text size (supporting multiple lines)
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Center the text both horizontally and vertically
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Draw a subtle shadow for readability (offset by a few pixels)
    shadow_offset = 3
    shadow_color = (0, 0, 0, 100)  # semi-transparent black
    draw.multiline_text((x + shadow_offset, y + shadow_offset), wrapped_text, font=font, fill=shadow_color, align="center")

    # Draw the main text with partial transparency
    main_text_color = (255, 255, 255, 220)  # almost opaque white
    draw.multiline_text((x, y), wrapped_text, font=font, fill=main_text_color, align="center")

    # Draw a larger "#justgirlythings" tag in the bottom-right corner
    tag_font = ImageFont.truetype(font_path, int(font_size * 0.6))
    tag_text = "#justgirlythings"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_width = tag_bbox[2] - tag_bbox[0]
    tag_height = tag_bbox[3] - tag_bbox[1]
    tag_x = width - tag_width - 30
    tag_y = height - tag_height - 30

    # Shadow for tag
    draw.text((tag_x + 2, tag_y + 2), tag_text, font=tag_font, fill=shadow_color)
    # Main tag text
    draw.text((tag_x, tag_y), tag_text, font=tag_font, fill=main_text_color)

    # Convert to RGB if saving as a JPEG (since JPEG doesn't support transparency)
    if output_path.lower().endswith(('.jpg', '.jpeg')):
        image = image.convert("RGB")

    image.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    make_just_girly_things_image("Next time you choose your dating partner .... don't let copilot choose\n-Jeff")
