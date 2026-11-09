"""Input parsing. Assigned module owner: Jiakai Chen."""
import os
from blocks import BLOCK_TYPES, FIXED, NO_BLOCK
from board import Board, BFFError

def parse_bff(text, name='board'):
    """
        Parse the contents of a .bff file.

        Raises :class:`BFFError` with a line number on any problem.
        """
    cls = Board
    rows = []
    blocks = {}
    lasers = []
    targets = set()
    in_grid = False
    grid_seen = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        if line.upper() == 'GRID START':
            if grid_seen:
                raise BFFError('line %d: second GRID START' % lineno)
            in_grid = grid_seen = True
            continue
        if line.upper() == 'GRID STOP':
            if not in_grid:
                raise BFFError('line %d: GRID STOP without START' % lineno)
            in_grid = False
            continue
        if in_grid:
            tokens = line.split()
            if len(tokens) == 1 and len(tokens[0]) > 1:
                tokens = list(tokens[0])
            for t in tokens:
                if t not in ('x', 'o', 'A', 'B', 'C'):
                    raise BFFError('line %d: unknown grid symbol %r' % (lineno, t))
            rows.append((lineno, tokens))
            continue
        tokens = line.split()
        key = tokens[0]
        try:
            values = [int(v) for v in tokens[1:]]
        except ValueError:
            raise BFFError('line %d: expected integers in %r' % (lineno, raw.strip()))
        if key in BLOCK_TYPES:
            if len(values) != 1 or values[0] < 0:
                raise BFFError('line %d: use "%s <count>"' % (lineno, key))
            blocks[key] = blocks.get(key, 0) + values[0]
        elif key == 'L':
            if len(values) != 4:
                raise BFFError('line %d: use "L x y vx vy"' % lineno)
            x, y, vx, vy = values
            if abs(vx) != 1 or abs(vy) != 1:
                raise BFFError('line %d: laser direction must be +/-1 in both axes' % lineno)
            lasers.append((x, y, vx, vy))
        elif key == 'P':
            if len(values) != 2:
                raise BFFError('line %d: use "P x y"' % lineno)
            targets.add(tuple(values))
        else:
            raise BFFError('line %d: unknown line %r' % (lineno, raw.strip()))
    if in_grid:
        raise BFFError('GRID START without GRID STOP')
    if not rows:
        raise BFFError('no grid found')
    width = len(rows[0][1])
    for lineno, r in rows:
        if len(r) != width:
            raise BFFError('line %d: grid row has %d cells, expected %d' % (lineno, len(r), width))
    height = len(rows)
    if not lasers:
        raise BFFError('no lasers (L lines) given')
    if not targets:
        raise BFFError('no target points (P lines) given')
    cells = []
    for _, r in rows:
        for t in r:
            if t == 'o':
                cells.append(None)
            elif t == 'x':
                cells.append(NO_BLOCK)
            else:
                cells.append(FIXED[t])
    for x, y, _, _ in lasers:
        if not (0 <= x <= 2 * width and 0 <= y <= 2 * height):
            raise BFFError('laser start (%d, %d) is off the board' % (x, y))
    for x, y in targets:
        if not (0 <= x <= 2 * width and 0 <= y <= 2 * height):
            raise BFFError('target (%d, %d) is off the board' % (x, y))
    free = cells.count(None)
    if sum(blocks.values()) > free:
        raise BFFError('%d blocks given but only %d open cells' % (sum(blocks.values()), free))
    return cls(width, height, cells, blocks, lasers, targets, name)

def read_bff(path):
    """Read a board from a .bff file path."""
    cls = Board
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    name = os.path.splitext(os.path.basename(path))[0]
    return cls.from_string(text, name=name)
