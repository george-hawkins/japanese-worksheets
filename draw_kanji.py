import os

import requests
from lxml import etree
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

from reportlab.graphics.shapes import Group, Shape

import config


class KanjiDrawer:
    def __init__(self, c: canvas.Canvas, cache_dir=config.KANJIVG_CACHE_DIR):
        self.c = c
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    @staticmethod
    def _codepoint(char: str):
        return format(ord(char), "05x")

    @classmethod
    def _download(cls, svg_filename: str, char: str):
        if not os.path.exists(svg_filename):
            codepoint = cls._codepoint(char)
            url = f"{config.KANJIVG_BASE_URL}/{codepoint}.svg"
            resp = requests.get(url)
            if resp.status_code != 200:
                raise FileNotFoundError(f"KanjiVG SVG not found for {char} (codepoint U+{codepoint})")
            with open(svg_filename, "w", encoding="utf-8") as f:
                f.write(resp.text)

    @staticmethod
    def _strip_numbers(svg_filename:str, unnumbered_filename: str):
        if not os.path.exists(unnumbered_filename):
            tree = etree.parse(svg_filename)
            root = tree.getroot()
            for elem in root.xpath('//svg:text', namespaces={'svg': 'http://www.w3.org/2000/svg'}):
                elem.getparent().remove(elem)
            tree.write(unnumbered_filename, encoding="utf-8", xml_declaration=True)

    # `strength` must be a value in the range [0.0, 1.0].
    @staticmethod
    def fade(color, strength: float):
        r = color.red * (1 - strength) + 1.0 * strength
        g = color.green * (1 - strength) + 1.0 * strength
        b = color.blue * (1 - strength) + 1.0 * strength
        return Color(r, g, b, alpha=getattr(color, "alpha", 1))

    @classmethod
    def fade_drawing(cls, node: Shape, strength: float):
        if hasattr(node, "strokeColor") and node.strokeColor:
            node.strokeColor = cls.fade(node.strokeColor, strength)

        if hasattr(node, "fillColor") and node.fillColor:
            node.fillColor = cls.fade(node.fillColor, strength)

        if isinstance(node, Group):
            for child in node.contents:
                cls.fade_drawing(child, strength)

    def draw(self, char: str, x: float, y: float, size: int, show_numbers=False, strength=None):
        codepoint = self._codepoint(char)
        svg_filename = f"{self.cache_dir}/{codepoint}.svg"
        unnumbered_filename = f"{self.cache_dir}/{codepoint}_unnumbered.svg"

        self._download(svg_filename, char)

        svg_to_use = svg_filename
        if not show_numbers:
            self._strip_numbers(svg_filename, unnumbered_filename)
            svg_to_use = unnumbered_filename

        drawing = svg2rlg(svg_to_use)
        if strength is not None:
            self.fade_drawing(drawing, strength)

        # Scale proportionally so height ≈ `size`
        if drawing.height > 0:
            scale = size / drawing.height
        else:
            scale = 1.0
        drawing.scale(scale, scale)

        renderPDF.draw(drawing, self.c, x, y)