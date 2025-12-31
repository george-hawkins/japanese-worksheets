from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm


def create_kanji_practice_grid(filename="kanji_grid.pdf",
                               columns=10,
                               rows=20,
                               sample_characters=None,
                               font_path=None):
    """
    Create a Japanese kanji practice grid PDF with furigana columns.

    Args:
        filename: Output PDF filename
        columns: Number of kanji columns
        rows: Number of rows per column
        sample_characters: List of kanji to display at the top of each column
        font_path: Path to TTF font file for kanji (optional)
    """
    # Create PDF canvas
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Register custom font if provided
    font_name = "Helvetica"  # Default font
    if font_path:
        try:
            pdfmetrics.registerFont(TTFont('KanjiFont', font_path))
            font_name = 'KanjiFont'
            print(f"Custom font loaded: {font_path}")
        except Exception as e:
            print(f"Warning: Could not load font from {font_path}: {e}")
            print("Falling back to default font")

    # Grid parameters (in millimeters)
    margin_left = 12 * mm
    margin_top = 12 * mm
    kanji_cell_width = 13 * mm  # Square cells
    kanji_cell_height = 13 * mm  # Same as width for squares
    furigana_cell_width = 4 * mm  # Narrow column for furigana
    gap_kanji_furigana = 0.8 * mm  # Small gap between kanji and furigana
    gap_between_columns = 1.5 * mm  # Wider gap between column pairs
    kanji_font_size = 34  # Font size in points for kanji

    # Calculate grid dimensions
    column_unit = kanji_cell_width + gap_kanji_furigana + furigana_cell_width + gap_between_columns
    grid_width = columns * column_unit - gap_between_columns  # Subtract last gap
    grid_height = rows * kanji_cell_height

    # Starting position (top-left)
    start_x = margin_left
    start_y = height - margin_top

    # Add guide lines (center lines only) in kanji cells FIRST so everything draws on top
    c.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray
    c.setLineWidth(0.5)

    for col in range(columns):
        for row in range(rows):
            # Only draw guide lines in kanji cells, not furigana cells
            x1 = start_x + col * column_unit
            y1 = start_y - row * kanji_cell_height
            x2 = x1 + kanji_cell_width
            y2 = y1 - kanji_cell_height

            # Draw center lines only
            center_x = x1 + kanji_cell_width / 2
            center_y = y1 - kanji_cell_height / 2
            c.line(center_x, y1, center_x, y2)  # Vertical center
            c.line(x1, center_y, x2, center_y)  # Horizontal center

    # Draw the grid
    c.setStrokeColorRGB(0, 0, 0)  # Black lines
    c.setLineWidth(1)

    # Draw kanji columns and furigana columns with gaps
    for i in range(columns):
        # Left edge of kanji column
        x = start_x + i * column_unit
        c.line(x, start_y, x, start_y - grid_height)

        # Right edge of kanji column
        x = start_x + i * column_unit + kanji_cell_width
        c.line(x, start_y, x, start_y - grid_height)

        # Furigana column (lighter lines)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)  # Lighter grey lines for furigana

        # Left edge of furigana column
        x = start_x + i * column_unit + kanji_cell_width + gap_kanji_furigana
        c.line(x, start_y, x, start_y - grid_height)

        # Right edge of furigana column
        x = start_x + i * column_unit + kanji_cell_width + gap_kanji_furigana + furigana_cell_width
        c.line(x, start_y, x, start_y - grid_height)

        # Reset to black for next kanji column
        c.setStrokeColorRGB(0, 0, 0)

    # Draw horizontal lines (rows) - need to account for gaps
    c.setStrokeColorRGB(0, 0, 0)  # Black lines
    for i in range(rows + 1):
        y = start_y - i * kanji_cell_height

        # Draw horizontal lines for each column pair
        for col in range(columns):
            # Line across kanji cell
            x1 = start_x + col * column_unit
            x2 = x1 + kanji_cell_width
            c.line(x1, y, x2, y)

            # Line across furigana cell (lighter)
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            x1 = start_x + col * column_unit + kanji_cell_width + gap_kanji_furigana
            x2 = x1 + furigana_cell_width
            c.line(x1, y, x2, y)
            c.setStrokeColorRGB(0, 0, 0)

    # Add sample kanji distributed across rows in light grey
    if sample_characters:
        try:
            c.setFont(font_name, kanji_font_size)
            c.setFillColorRGB(0.6, 0.6, 0.6)  # Slightly darker grey for tracing
            num_kanji = len(sample_characters)

            if num_kanji > 0:
                rows_per_kanji = rows // num_kanji

                for kanji_idx, char in enumerate(sample_characters):
                    # Calculate which rows this kanji should appear in
                    start_row = kanji_idx * rows_per_kanji
                    end_row = (kanji_idx + 1) * rows_per_kanji

                    # Draw the kanji in every second cell (columns 0, 2, 4, 6, 8)
                    for col in range(0, columns, 2):
                        for row in range(start_row, end_row):
                            # Center the character in the kanji cell
                            x = start_x + col * column_unit + kanji_cell_width / 2
                            y = start_y - row * kanji_cell_height - kanji_cell_height / 2
                            char_width = c.stringWidth(char, font_name, kanji_font_size)
                            c.drawString(x - char_width / 2, y - kanji_font_size / 3, char)

            # Reset fill color to black for any subsequent drawing
            c.setFillColorRGB(0, 0, 0)
        except Exception as e:
            print(f"Warning: Could not add characters: {e}")

    # Save the PDF
    c.save()
    print(f"PDF created: {filename}")


# Example usage
if __name__ == "__main__":
    # Sample kanji from the image
    sample_kanji = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

    create_kanji_practice_grid(
        filename="kanji_practice.pdf",
        columns=10,
        rows=20,
        sample_characters=sample_kanji,
        font_path="KanjiStrokeOrders_v4.005.ttf"  # Replace with your TTF file path
    )

    print("Kanji practice grid generated successfully!")
    print("Features:")
    print("  - Main columns for kanji practice with guide lines")
    print("  - Narrow furigana columns to the right of each kanji column")
    print("  - Customizable number of columns and rows")
    print("  - Custom font support for kanji")
    print("\nYou can customize the grid by modifying the parameters:")
    print("  - columns: number of kanji columns (each with its furigana column)")
    print("  - rows: number of rows")
    print("  - sample_characters: list of kanji to display at the top")
    print("  - font_path: path to your TTF font file")