from io import BytesIO

import aiohttp
from cal_values import calculate_values
from PIL import Image, ImageDraw, ImageFilter, ImageFont

font_path = "./fonts/namecat/Namecat.ttf"


class Utils:
    @staticmethod
    async def open_image_from_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    image = Image.open(BytesIO(image_bytes))
                    if image.mode == "P" and "transparency" in image.info:
                        image = image.convert("RGBA")
                    return image
                else:
                    return None

    @staticmethod
    def add_text(
        draw,
        text,
        font,
        pos_y,
        offset,
        text_color="white",
        make_shadow=True,
        shadow_color="black",
    ):
        _, _, text_width, _ = draw.textbbox((0, 0), text, font=font)
        if make_shadow:
            draw.text(
                (((draw._image.width - text_width) // 2) - offset, pos_y),
                text,
                fill=shadow_color,
                font=font,
            )

        draw.text(
            ((draw._image.width - text_width) // 2, pos_y),
            text,
            fill=text_color,
            font=font,
        )

    def circle_mask(size):
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        circle_radius = size[0] // 2
        center = (size[0] // 2, size[1] // 2)
        draw.ellipse(
            (
                center[0] - circle_radius,
                center[1] - circle_radius,
                center[0] + circle_radius,
                center[1] + circle_radius,
            ),
            fill=255,
        )
        return mask.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.SMOOTH_MORE)


class BackgroundImage:
    def __init__(self, image_path, blur=True):
        self.background = Image.open(image_path)
        self.values = calculate_values(self.background.size)
        if blur:
            self.background = self.background.filter(
                ImageFilter.GaussianBlur(self.values.blur)
            )
        self.font = ImageFont.truetype(font_path, self.values.font_size)
        self.font_small = ImageFont.truetype(
            font_path,
            self.values.font_size - self.values.text2_font_size_subtraction_value,
        )


class DiscordBannerMaker:
    def __init__(self, background_image):
        self.background_image = background_image

    async def make_banner(self, overlay_url, text, text2):
        background = self.background_image.background.copy()

        overlay = await Utils.open_image_from_url(overlay_url)
        overlay = overlay.resize(self.background_image.values.overlay_size)
        overlay_mask = Utils.circle_mask(overlay.size)

        x_position = (background.width - overlay.width) // 2
        y_position = (
            background.height
            - overlay.height
            - self.background_image.values.cicle_y_pos_subtraction_value
        ) // 2

        background.paste(overlay, (int(x_position), int(y_position)), overlay_mask)

        # for text
        draw = ImageDraw.Draw(background)
        font = self.background_image.font
        font_small = self.background_image.font_small
        font_ver_pos = self.background_image.values.font_ver_pos
        offset = self.background_image.values.offset
        text2_font_ver_pos_addition_value = (
            self.background_image.values.text2_font_ver_pos_addition_value
        )
        text2_offset = self.background_image.values.text2_offset

        Utils.add_text(draw, text, font, font_ver_pos, offset)
        Utils.add_text(
            draw,
            text2,
            font_small,
            font_ver_pos + text2_font_ver_pos_addition_value,
            text2_offset,
        )

        return background

        # circle_radius = (
        #     self.background_image.values.overlay_size[0] // 2
        # ) + self.background_image.values.circle_radius_addition_value
        # image_width, image_height = background.size
        # circle_center = (
        #     (image_width - self.background_image.values.offset) // 2,
        #     (image_height - self.background_image.values.cicle_y_pos_subtraction_value)
        #     // 2,
        # )
        # draw.ellipse(
        #     (
        #         circle_center[0] - circle_radius,
        #         circle_center[1] - circle_radius,
        #         circle_center[0] + circle_radius,
        #         circle_center[1] + circle_radius,
        #     ),
        #     fill=(0, 0, 0, 90),
        # )

        # shadow = Image.new("RGBA", background.size, (0, 0, 0, 0))
        # draw = ImageDraw.Draw(shadow)
        # draw.rounded_rectangle(
        #     (300, 300, background.size[0] - 300, background.size[1] - 300),
        #     fill=(0, 0, 0, 60),
        #     radius=200,
        # )

        # background = Image.alpha_composite(
        #     background.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(50))
        # )
