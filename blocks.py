"""Block classes. Assigned module owner: Jiakai Chen; physics reviewed with Tingting Li."""

class Block:
    """
    Base class for anything that can occupy a grid cell.

    Subclasses override :meth:`interact`, which tells the tracer what
    happens to a laser that touches this block.

    **Parameters**

        fixed: *bool*
            True if the block was given in the board file and may not
            be moved by the solver.
    """

    symbol = 'o'

    def __init__(self, fixed=False):
        self.fixed = fixed

    def interact(self, x, vx, vy):
        """
        Return the new direction(s) of a laser touching this block.

        **Parameters**

            x: *int*
                x coordinate of the laser at the contact point.  Only its
                parity matters: odd means the laser hit a top/bottom edge,
                even means it hit a left/right edge.
            vx, vy: *int*
                Current laser direction (each is +1 or -1).

        **Returns**

            directions: *tuple of (int, int)*
                Zero, one or two outgoing directions.  The laser leaves
                the contact point in each of these directions.
        """
        return ((vx, vy),)

    def __repr__(self):
        tag = 'fixed ' if self.fixed else ''
        return '<%s%s>' % (tag, type(self).__name__)

class EmptyCell(Block):
    """A cell with no block in it; lasers pass straight through."""

    symbol = 'o'

class NoBlockCell(Block):
    """A cell where blocks are not allowed ('x'); lasers pass through."""

    symbol = 'x'

class ReflectBlock(Block):
    """Reflect block ('A'): mirrors the laser off the face it hits."""

    symbol = 'A'

    def interact(self, x, vx, vy):
        if x & 1:                    # hit top or bottom face
            return ((vx, -vy),)
        return ((-vx, vy),)          # hit left or right face

class OpaqueBlock(Block):
    """Opaque block ('B'): absorbs the laser."""

    symbol = 'B'

    def interact(self, x, vx, vy):
        return ()

class RefractBlock(Block):
    """Refract block ('C'): lets the laser through *and* reflects a copy."""

    symbol = 'C'

    def interact(self, x, vx, vy):
        if x & 1:
            return ((vx, vy), (vx, -vy))
        return ((vx, vy), (-vx, vy))

# Shared instances.  Blocks are stateless apart from ``fixed``, so the
# solver can reuse one object per kind instead of creating thousands.
EMPTY = EmptyCell()
NO_BLOCK = NoBlockCell()
MOVABLE = {
    'A': ReflectBlock(),
    'B': OpaqueBlock(),
    'C': RefractBlock(),
}
FIXED = {
    'A': ReflectBlock(fixed=True),
    'B': OpaqueBlock(fixed=True),
    'C': RefractBlock(fixed=True),
}
BLOCK_TYPES = ('A', 'B', 'C')


