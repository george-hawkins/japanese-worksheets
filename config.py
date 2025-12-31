from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

PAGE_SIZE = A4
MARGIN_LEFT = 12 * mm
MARGIN_RIGHT = MARGIN_LEFT
MARGIN_TOP = 12 * mm
MARGIN_BOTTOM = MARGIN_TOP
KANJI_CELL_SIDE = 13 * mm
KANJI_BORDER = 1 * mm
FURIGANA_CELL_SIDE = 4 * mm
KANJI_FURIGANA_GAP = 0.8 * mm
COLUMN_GAP = 1.5 * mm

GUIDELINE_GRAY = 0.8
GUIDELINE_WIDTH = 0.5

GRID_GRAY = 0
GRID_LINE_WIDTH = 1

FURIGANA_GRAY = 0.7

TRACING_STRENGTH = 0.75
TRACING_FREQ = 4  # How often traceable characters are drawn.

KANJIVG_BASE_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/refs/heads/master/kanji"
KANJIVG_CACHE_DIR = "kanjivg_cache"