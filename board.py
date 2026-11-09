"""Board representation. Assigned module owner: Jiakai Chen."""

class BFFError(ValueError):
    """Raised when a .bff file is malformed."""

class Board:
    """
    A Lazor board as described by a .bff file.

    **Attributes**

        width, height: *int*
            Board size in blocks.
        cells: *list of Block or None*
            Row-major list of length ``width * height``.  ``None`` marks a
            cell where the solver may place a block ('o' in the file).
        blocks: *dict*
            Number of movable blocks of each type, e.g. ``{'A': 2, 'C': 1}``.
        lasers: *list of (x, y, vx, vy)*
        targets: *set of (x, y)*
        name: *str*
    """

    def __init__(self, width, height, cells, blocks, lasers, targets, name='board'):
        self.width = width
        self.height = height
        self.cells = cells
        self.blocks = blocks
        self.lasers = lasers
        self.targets = targets
        self.name = name

    @classmethod
    def from_file(cls, path):
        """Read a file through the parser module."""
        from parser import read_bff
        return read_bff(path)

    @classmethod
    def from_string(cls, text, name='board'):
        """Parse text through the parser module."""
        from parser import parse_bff
        return parse_bff(text, name=name)
