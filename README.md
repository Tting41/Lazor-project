# Lazor Solver

EN.540.635 Software Carpentry, Lazor group project.

This program reads `.bff` board files and searches for block arrangements that
allow the lasers to reach every target point.

## Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/) for PNG output; optional for text-only use

No other dependencies are required.

## Usage

Run the program from the project root, where `lazor.py` and the other Python
modules are located:

```bash
python lazor.py <board_file.bff> --outdir <output_directory>
```

Multiple board files can be supplied in one command. Add `--no-png` for text-only
output. `main.py` can also be used as the entry point.

## How it works

The program is organized into three functional parts: file parsing and board
setup, laser simulation, and the solver algorithm and output. The modules share
a common board representation and remain together in the project root.

| Part | Files | Purpose |
|---|---|---|
| File parsing and board setup | `board.py`, `parser.py`, `blocks.py` | Read `.bff` files and represent the board, available blocks, fixed blocks, laser starts, and targets |
| Laser simulation | `laser.py`, `simulation.py` | Determine block collisions, trace laser paths, and estimate reachable points |
| Solver algorithm and output | `solver.py`, `output.py`, `main.py`, `lazor.py` | Search block arrangements, evaluate target coverage, and coordinate execution and output |

`parser.py` reads the input and creates a `Board`. The solver uses this board to
explore arrangements and calls the simulation functions to evaluate the laser
paths. `main.py` coordinates input, solving, and output, while `lazor.py`
provides a single command-line entry point.

The block classes in `blocks.py` describe empty cells, cells where blocks are
not allowed, and reflecting, opaque, and refracting blocks. Their `interact()`
methods define the outgoing laser directions. Fixed blocks remain in their
specified positions throughout the search.

Coordinates use half-block steps, as specified by the `.bff` format, with the
origin at the top-left corner. A laser at a block-edge midpoint has exactly one
odd coordinate. This parity identifies the face being approached and whether
reflection reverses `vx` or `vy`.

Laser tracing records complete `(x, y, vx, vy)` states so that repeated paths
and loops do not require indefinite tracing. Paths from multiple lasers and
refracted branches are considered together when checking target coverage.

### Speed and Optional Challenge

Enumerating all complete block arrangements would require
`C(n, a) · C(n−a, b) · C(n−a−b, c)` candidate boards, with laser tracing for each
candidate. Our approach focuses on the cells that influence laser propagation
and uses an optimistic reachability bound to reject impossible branches.

The solver advances the lasers through a partially determined board. When a
laser reaches the first undecided cell, the search branches over leaving that
cell empty or placing an A, B, or C block, subject to the remaining inventory.
Once all laser paths are determined and every target is reached, remaining
blocks can be placed in untouched undecided cells without changing those paths.
This avoids separately exploring arrangements that differ only at locations
that cannot affect the established laser paths.

At applicable search steps, the solver estimates the points that the lasers
could still reach. Undecided cells may transmit light and, while an A or C block
remains available, may also reflect it. This relaxed model provides an upper
bound on reachability. If any target is outside that bound, no completion of
the current arrangement can reach every target, so the branch is abandoned.
These two strategies address the optional challenge by reducing unnecessary
arrangement generation and evaluation.

## Output

`output.py` writes a text file containing the final grid in `.bff` grid notation:
`o` for empty cells, `x` for cells where blocks are not allowed, `A` for reflecting
blocks, `B` for opaque blocks, and `C` for refracting blocks.

When PNG output is enabled and Pillow is installed, it also draws the board
with red laser paths, white target circles, and yellow outlines for fixed blocks.

## Tests

Run the test suite from the project root:

```bash
python -m unittest discover -v
```

The tests are grouped by responsibility:

| File | Scope |
|---|---|
| `tests/test_jiakai_chen.py` | File parsing, board setup, and block classes |
| `tests/test_tingting_li.py` | Laser propagation, block interactions, and loops |
| `tests/test_junying_yu.py` | Search, output, and integration |

`tests/support.py` provides shared random-board generation and a brute-force
reference search. These support comparisons between search strategies on small
boards. The suite also includes malformed-input and output-file checks.

## Authors and Contributions

Jiakai Chen is responsible for file parsing and board setup, including reading
and interpreting `.bff` files and developing class-based representations of
the board and blocks, including fixed blocks.

Tingting Li is responsible for laser simulation, including laser movement,
reflection, absorption, refraction, path tracking, and determining whether all
target points are reached.

Junying Yu is responsible for the solver algorithm and output, including
generating and evaluating block arrangements, identifying valid solutions,
and producing the solution files.
