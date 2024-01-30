from PIL import Image  # , ImageDraw, ImageFont

overlay_size = 0.23  # (0.23 * (bg_width + bg_hight)) / 2

font_ver_pos = 0.57  # 0.57 * bg_hight
font_size = 0.05  # 0.05 * (bg_width + bg_hight)
offset = 0.09  # 0.09 * font_size

circle_radius_addition_value = 0.0025  # 0.0025 * (bg_width + bg_hight)
cicle_y_pos_subtraction_value = 0.116  # 0.116 * (bg_width + bg_hight)

text2_font_size_subtraction_value = 0.4  # 0.4 * font_size
text2_font_ver_pos_addition_value = 0.24  # 0.24 * font_ver_pos
text2_offset = offset  # offset * (font_size-text2_font_size_subtraction_value)

blur = 0.0033  # 0.0033 * (bg_width + bg_hight)


class Values:
    def __init__(
        self,
        _overlay_size,
        _font_ver_pos,
        _font_size,
        _offset,
        _circle_radius_addition_value,
        _cicle_y_pos_subtraction_value,
        _text2_font_size_subtraction_value,
        _text2_font_ver_pos_addition_value,
        _blur,
        _text2_offset,
    ):
        self.overlay_size = (round(_overlay_size), round(_overlay_size))
        self.font_ver_pos = _font_ver_pos
        self.font_size = _font_size
        self.offset = _offset
        self.circle_radius_addition_value = _circle_radius_addition_value
        self.cicle_y_pos_subtraction_value = _cicle_y_pos_subtraction_value
        self.text2_font_size_subtraction_value = _text2_font_size_subtraction_value
        self.text2_font_ver_pos_addition_value = _text2_font_ver_pos_addition_value
        self.blur = _blur
        self.text2_offset = _text2_offset


def calculate_values(img_size):
    img_size_total = img_size[0] + img_size[1]

    _overlay_size = (overlay_size * img_size_total) / 2

    _font_ver_pos = font_ver_pos * img_size[1]
    _font_size = font_size * img_size_total

    _offset = offset * _font_size
    _circle_radius_addition_value = circle_radius_addition_value * img_size_total
    _cicle_y_pos_subtraction_value = cicle_y_pos_subtraction_value * img_size_total

    _text2_font_size_subtraction_value = text2_font_size_subtraction_value * _font_size
    _text2_font_ver_pos_addition_value = (
        text2_font_ver_pos_addition_value * _font_ver_pos
    )

    _blur = blur * img_size_total
    _text2_offset = text2_offset * (_font_size - _text2_font_size_subtraction_value)

    return Values(
        _overlay_size,
        _font_ver_pos,
        _font_size,
        _offset,
        _circle_radius_addition_value,
        _cicle_y_pos_subtraction_value,
        _text2_font_size_subtraction_value,
        _text2_font_ver_pos_addition_value,
        _blur,
        _text2_offset,
    )
