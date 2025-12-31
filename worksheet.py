from reportlab.pdfgen import canvas
import argparse

import config
import math
from draw_kanji import KanjiDrawer

class PracticeGrid:
    def __init__(self, filename: str):
        self.c = canvas.Canvas(filename, pagesize=config.PAGE_SIZE)
        self.kanji_drawer = KanjiDrawer(self.c)

    def draw(self, chars):
        page_width, page_height = config.PAGE_SIZE

        start_x = config.MARGIN_LEFT
        start_y = page_height - config.MARGIN_TOP
        width = page_width - (config.MARGIN_LEFT + config.MARGIN_RIGHT)

        start_y = self._draw_stroke_order_kanji(chars, start_x, start_y, width)
        start_y -= config.SEPARATOR
        height = start_y - config.MARGIN_BOTTOM
        self._draw_worksheet(chars, start_x, start_y, width, height)

        self.c.save()
        print("Done")

    def _draw_worksheet(self, chars, start_x, start_y, width, height):
        col_width = config.KANJI_CELL_SIDE + config.KANJI_FURIGANA_GAP + config.FURIGANA_CELL_SIDE
        cols = self.divisions(width, col_width, config.COLUMN_GAP)
        rows = self.divisions(height, config.KANJI_CELL_SIDE)
        col_unit = col_width + config.COLUMN_GAP

        self._draw_guidelines(start_x, start_y, cols, rows, col_unit)
        self._draw_grid_verticals(start_x, start_y, height, cols, col_unit)
        self._draw_grid_horizontals(start_x, start_y, cols, rows, col_unit)
        self._draw_kanji(chars, start_x, start_y, cols, rows, col_unit)

    def _draw_guidelines(self, start_x, start_y, cols, rows, col_unit):
        self.set_gray(config.GUIDELINE_GRAY)
        self.c.setLineWidth(config.GUIDELINE_WIDTH)

        for col in range(cols):
            for row in range(rows):
                x1 = start_x + col * col_unit
                y1 = start_y - row * config.KANJI_CELL_SIDE

                x2 = x1 + config.KANJI_CELL_SIDE
                y2 = y1 - config.KANJI_CELL_SIDE
                center_x = x1 + config.KANJI_CELL_SIDE / 2
                center_y = y1 - config.KANJI_CELL_SIDE / 2

                self.c.line(center_x, y1, center_x, y2)  # Vertical guideline.
                self.c.line(x1, center_y, x2, center_y)  # Horizontal guideline.

    def _draw_grid_verticals(self, start_x, start_y, height, cols, col_unit):
        self.c.setLineWidth(config.GRID_LINE_WIDTH)

        for i in range(cols):
            self.set_gray(config.GRID_GRAY)

            # Left edge of kanji column.
            x = start_x + i * col_unit
            self.c.line(x, start_y, x, start_y - height)

            # Right edge of kanji column.
            x += config.KANJI_CELL_SIDE
            self.c.line(x, start_y, x, start_y - height)

            self.set_gray(config.FURIGANA_GRAY)

            # Left edge of furigana column.
            x += config.KANJI_FURIGANA_GAP
            self.c.line(x, start_y, x, start_y - height)

            # Right edge of furigana column.
            x += config.FURIGANA_CELL_SIDE
            self.c.line(x, start_y, x, start_y - height)

    def _draw_grid_horizontals(self, start_x, start_y, cols, rows, col_unit):
        for row in range(rows + 1):
            y = start_y - row * config.KANJI_CELL_SIDE

            for col in range(cols):
                self.set_gray(config.GRID_GRAY)
                x1 = start_x + col * col_unit
                x2 = x1 + config.KANJI_CELL_SIDE
                self.c.line(x1, y, x2, y)

                self.set_gray(config.FURIGANA_GRAY)
                x1 += config.KANJI_CELL_SIDE + config.KANJI_FURIGANA_GAP
                x2 = x1 + config.FURIGANA_CELL_SIDE
                self.c.line(x1, y, x2, y)

    def _draw_kanji(self, chars, start_x, start_y, cols, rows, col_unit):
        start_x += config.KANJI_BORDER
        start_y -= config.KANJI_CELL_SIDE - config.KANJI_BORDER

        side = config.KANJI_CELL_SIDE - 2 * config.KANJI_BORDER

        total_cells = cols * rows
        cells_per_char = total_cells // (config.TRACING_FREQ * len(chars))
        cell_count = 0
        offset = 0
        current_count = 0

        for col in reversed(range(cols)):
            for row in range(rows):
                if cell_count % config.TRACING_FREQ == 0:
                    if offset < len(chars):
                        char = chars[offset]
                        x = start_x + col * col_unit
                        y = start_y - row * config.KANJI_CELL_SIDE
                        self.kanji_drawer.draw(char, x, y, side, strength=config.TRACING_STRENGTH)
                        current_count += 1
                        if current_count == cells_per_char:
                            offset += 1
                            current_count = 0

                cell_count += 1

    def _draw_stroke_order_kanji(self, chars, start_x, start_y, width) -> int:
        cols = self.divisions(width, config.LARGE_KANJI_CELL_SIDE)
        rows = math.ceil(len(chars) / cols)
        # Recalculating `cols` means that instead of e.g. splitting 10 characters
        # into one row of 6 and one of 4, it's split into two rows of 5.
        cols = math.ceil(len(chars) / rows)

        start_y -= config.LARGE_KANJI_CELL_SIDE
        start_x += (width - cols * config.LARGE_KANJI_CELL_SIDE) / 2

        side = config.LARGE_KANJI_CELL_SIDE - 2 * config.LARGE_KANJI_BORDER

        offset = 0

        for row in range(rows):
            for col in range(cols):
                    char = chars[offset]
                    x = start_x + col * config.LARGE_KANJI_CELL_SIDE
                    y = start_y - row * config.LARGE_KANJI_CELL_SIDE
                    self.kanji_drawer.draw(char, x, y, side, show_numbers=True)
                    offset += 1
                    if offset == len(chars):
                        break

        return start_y - (rows - 1) * config.LARGE_KANJI_CELL_SIDE

    def set_gray(self, gray):
        self.c.setStrokeColorRGB(gray, gray, gray)

    @staticmethod
    def divisions(page_width, col_width, gap_width=0):
        n = (page_width + gap_width) / (col_width + gap_width)
        return math.floor(n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a kanji PDF worksheet.")
    parser.add_argument("--filename", type=str, required=True, help="Output PDF filename")
    parser.add_argument("--characters", type=str, required=True, help="Kanji to include")

    args = parser.parse_args()

    grid = PracticeGrid(args.filename)

    grid.draw(args.characters)
