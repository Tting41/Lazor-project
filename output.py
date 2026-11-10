"""Text and PNG output. Assigned module owner: Junying Yu."""
from simulation import trace

def solution_text(board, cells):
    """Return the solved grid in .bff grid notation."""
    lines = []
    for j in range(board.height):
        row = cells[j * board.width:(j + 1) * board.width]
        lines.append(' '.join(c.symbol for c in row))
    return '\n'.join(lines)

def write_text(board, cells, path, elapsed=None):
    """Write a human-readable solution file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# Solution for %s\n' % board.name)
        f.write('#   o = empty, x = no block allowed\n')
        f.write('#   A = reflect, B = opaque, C = refract\n')
        if elapsed is not None:
            f.write('# Solved in %.4f s\n' % elapsed)
        f.write('GRID START\n')
        f.write(solution_text(board, cells) + '\n')
        f.write('GRID STOP\n')

def write_png(board, cells, path, scale=60):
    """
    Draw the solution with Pillow.  Returns False if Pillow is missing.
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    half = scale // 2
    pad = half
    size = (board.width * scale + 2 * pad, board.height * scale + 2 * pad)
    img = Image.new('RGB', size, (40, 40, 40))
    draw = ImageDraw.Draw(img)
    colours = {
        'o': (120, 120, 120),
        'x': (40, 40, 40),
        'A': (235, 235, 235),
        'B': (15, 15, 15),
        'C': (150, 200, 255),
    }

    def px(x, y):
        return pad + x * half, pad + y * half

    for j in range(board.height):
        for i in range(board.width):
            c = cells[j * board.width + i]
            x0, y0 = px(2 * i, 2 * j)
            box = [x0 + 2, y0 + 2, x0 + scale - 2, y0 + scale - 2]
            draw.rectangle(box, fill=colours[c.symbol])
            if c.fixed:
                draw.rectangle(box, outline=(255, 200, 0), width=3)

    _, _, segments = trace(board, cells, record_path=True)
    for x0, y0, x1, y1 in segments:
        draw.line([px(x0, y0), px(x1, y1)], fill=(255, 40, 40), width=3)
    for x, y, _, _ in board.lasers:
        cx, cy = px(x, y)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 40, 40))
    for x, y in board.targets:
        cx, cy = px(x, y)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7],
                     outline=(255, 255, 255), width=3)

    img.save(path)
    return True
