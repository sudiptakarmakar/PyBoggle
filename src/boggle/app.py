import itertools
import pathlib
import random

import click

ROWS = 4
COLS = 4

CLASSIC_CONFIG = [
    "AACIOT",
    "ABILTY",
    "ABJMOQ",
    "ACDEMP",
    "ACELRS",
    "ADENVZ",
    "AHMORS",
    "BIFORX",
    "DENOSW",
    "DKNOTU",
    "EEFHIY",
    "EGKLUY",
    "EGINTV",
    "EHINPS",
    "ELPSTU",
    "GILRUW",
]

NEW_CONFIG = [
    "AAEEGN",
    "ABBJOO",
    "ACHOPS",
    "AFFKPS",
    "AOOTTW",
    "CIMOTU",
    "DEILRX",
    "DELRVY",
    "DISTTY",
    "EEGHNW",
    "EEINSU",
    "EHRTVW",
    "EIOSST",
    "ELRTTY",
    "HIMNUQ",
    "HLNNRZ",
]


def get_boggle_board(letters: list[str]) -> str:
    cubes = [f"{i.title():>2}" if i.lower() != "q" else "Qu" for i in letters]
    template = """
┌───────────────────────────────────────────┐
│          │          │          │          │
│    {}    │    {}    │    {}    │    {}    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│    {}    │    {}    │    {}    │    {}    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│    {}    │    {}    │    {}    │    {}    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│    {}    │    {}    │    {}    │    {}    │
│          │          │          │          │
└───────────────────────────────────────────┘
"""
    return template.strip().format(*cubes), "".join(letters[:16])


class Dictionary:
    def __init__(self, word_file=None, words=None, lang="en_US", word_min_length=3):
        self.word_min_length = word_min_length
        self.container = set()
        self.words_file_name = word_file
        self.dictionary = None

        if words is not None and len(words) > 0:
            self.container = set(
                word.strip().lower()
                for word in words
                if len(word.strip()) >= word_min_length
            )
            return

        if word_file is not None and pathlib.Path(word_file).exists():
            with open(word_file, "r") as words:
                self.container = set(
                    word.strip().lower()
                    for word in words
                    if len(word.strip()) >= word_min_length
                )
            return
        # import enchant only if its required
        import enchant

        self.dictionary = enchant.Dict(lang)

    def is_valid(self, word):
        if len(word.strip()) < self.word_min_length:
            return False
        if len(self.container) > 0:
            return word in self.container
        else:
            return self.dictionary.check(word)

    def __repr__(self):
        return f"Dictionary powered by '{self.words_file_name if self.words_file_name is not None else 'PyEnchant'}'"


class GetNeighbors:
    def __init__(self, mixed=False, diag=False):
        self.mixed_direction = mixed
        self.diagonal_only = diag
        self.active_path = set()

    def __call__(self, row, col, current_path):
        used_cells = set(current_path)
        if self.mixed_direction:
            yield from (
                (r, c)
                for r, c in itertools.product(
                    range(row - 1, row + 2), range(col - 1, col + 2)
                )
                if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in used_cells
            )
        else:
            if self.diagonal_only:
                yield from (
                    (r, c)
                    for r, c in itertools.product(
                        (row - 1, row + 1), (col - 1, col + 1)
                    )
                    if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in used_cells
                )
            else:
                yield from (
                    (r, c)
                    for r, c in [
                        (row, col - 1),
                        (row - 1, col),
                        (row + 1, col),
                        (row, col + 1),
                    ]
                    if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in used_cells
                )


class BoggleSolver:
    def __init__(self, letters: list[str], dictionary: Dictionary = None):
        assert len(letters) == ROWS * COLS
        self.letters = letters
        self.cubes = []
        for i in range(0, ROWS * COLS, COLS):
            self.cubes.append(list(letters[i : i + COLS]))
        self.dictionary = dictionary
        self.words = set()

    def __repr__(self):
        return "\n".join(
            " ".join(f"{ch.title():>2}" for ch in row) for row in self.cubes
        )

    def __str__(self):
        return get_boggle_board("".join(l[0] for l in self.letters))[0]

    def details(self):
        return repr(self.dictionary)

    def dfs(self, get_neighbors_fn, row, col, current_path, prefix):
        for nbr_r, nbr_c in get_neighbors_fn(row, col, current_path):
            new_prefix = prefix + self.cubes[nbr_r][nbr_c]
            if self.dictionary.is_valid(new_prefix) and new_prefix not in self.words:
                self.words.add(new_prefix)
                yield new_prefix
            yield from self.dfs(
                get_neighbors_fn,
                nbr_r,
                nbr_c,
                current_path + [(nbr_r, nbr_c)],
                new_prefix,
            )

    def find_words(self, mixed_direction=False):
        get_neighbors_fns = []
        if mixed_direction:
            get_neighbors_fns = [
                GetNeighbors(mixed=True),
            ]
        else:
            get_neighbors_fns = [
                GetNeighbors(mixed=False, diag=False),
                GetNeighbors(mixed=False, diag=True),
            ]

        for row in range(ROWS):
            for col in range(COLS):
                for fn in get_neighbors_fns:
                    yield from self.dfs(
                        fn, row, col, [(row, col)], self.cubes[row][col]
                    )

    def show_results(self, verbose, capitalize, mixed_direction=False, print_width=40):
        def transform(w):
            return w.title() if capitalize else w

        if verbose:
            print(self)
            print(self.details())

        word_count = 0
        line_length = 0
        for word in self.find_words(mixed_direction=mixed_direction):
            word_count += 1

            if print_width <= 0:  # print each word in new line
                print(f"{transform(word)}", flush=True)
                continue

            if line_length + len(word) + 2 > print_width:
                print(flush=True)
                line_length = 0
            line_length += len(word)
            print(f"{transform(word)}, ", end="", flush=True)

        print(f"\n[found: {word_count}]", flush=True)


def get_boggle_cubes(prefix="", ordered=False, generate_random=True, classic=False):
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    required = max(0, ROWS * COLS - len(prefix))
    prefix = list(prefix)
    if generate_random:
        if len(prefix) > 0 and not ordered:
            random.shuffle(prefix)
        if required > 0:
            random.shuffle(alphabet)
            return (prefix + random.choices(alphabet, k=required))[0 : ROWS * COLS]
        return prefix[0 : ROWS * COLS]
    dices = CLASSIC_CONFIG if classic else NEW_CONFIG
    return [random.choice(dice).lower() for dice in dices]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("letters")
@click.option(
    "--dict-file",
    "-d",
    "dfile",
    type=click.Path(exists=True),
    help="Provide file as dictionary",
)
@click.option(
    "--dict-words",
    "-w",
    "dwords",
    multiple=True,
    help="Provide comma separated list of words as dictionary",
)
@click.option(
    "--dict-lang",
    "-l",
    "dlang",
    default="en_US",
    help="Provide dictionary language code for system library",
)
@click.option(
    "--mixed",
    is_flag=True,
    help="Mixed direction, can navigate diagonally as well as sideways, up down",
)
@click.option(
    "--word-min-length",
    default=3,
    help="Minimum length of valid word",
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode, prints details")
@click.option(
    "-C", "--capitalize", is_flag=True, help="Print words in capitalized form"
)
@click.option(
    "--wrap-length", type=int, default=40, help="Word wrap when printing result"
)
def solve(
    letters,
    dfile,
    dwords,
    dlang,
    mixed,
    word_min_length,
    verbose,
    capitalize,
    wrap_length,
):
    dictionary = Dictionary(
        word_file=dfile, words=dwords, lang=dlang, word_min_length=word_min_length
    )
    game = BoggleSolver(letters, dictionary)
    game.show_results(verbose, capitalize, mixed, wrap_length)


@cli.command()
@click.option("--letters", default="", help="Provide letters for the game")
@click.option("--ordered", is_flag=True, help="Preserve order of the letters")
@click.option(
    "--random", "is_random", is_flag=True, help="Generate completely random board"
)
@click.option("--classic", is_flag=True, help="Generate classic board")
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode, no-op")
@click.option("-c", "--print-code", "code", is_flag=True, help="Only prints letters")
def new(letters, ordered, is_random, classic, verbose, code):
    letters = get_boggle_cubes(
        prefix=letters, ordered=ordered, generate_random=is_random, classic=classic
    )
    board, text = get_boggle_board(letters)
    if code:
        click.echo(click.style(f" {text} ", bg="white", fg="red", bold=True))
    else:
        click.echo(board)
        click.echo(text)


if __name__ == "__main__":
    cli()
