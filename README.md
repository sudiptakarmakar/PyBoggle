# PyBoggle
A 4x4 boggle generator and solver

Generate a new boggle layout from modern boggle configuration:

```bash
$ python3 src/boggle/app.py new
┌───────────────────────────────────────────┐
│          │          │          │          │
│     G    │     B    │     S    │     F    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     T    │     M    │     I    │     L    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     I    │     E    │     E    │     T    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     S    │     Y    │     H    │     N    │
│          │          │          │          │
└───────────────────────────────────────────┘
gbsftmilieetsyhn
```


Generate a new boggle layout from classic boggle configuration:

```bash
$ python3 src/boggle/app.py new --classic
┌───────────────────────────────────────────┐
│          │          │          │          │
│     O    │     L    │    Qu    │     P    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     R    │     Z    │     M    │     X    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     S    │     D    │     E    │     K    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     G    │     N    │     U    │     W    │
│          │          │          │          │
└───────────────────────────────────────────┘
olqprzmxsdekgnuw
```

You can generate a boggle game layout by passing your own letters as well as a prefix. In case the number of letters is less than 16, it will generate the remaining letters. To use your own prefix you must supply `--random` flag as well to let the program know that it can generate random characters for any missing slot. If you want to preserve the order of your letters, pass in `--ordered` flag along with it. If any of the letters supplied is `Q/q`, the system wull replace it as `Qu` for internal processing.

```bash
$ python3 src/boggle/app.py new --letters DontQuit --random --ordered
┌───────────────────────────────────────────┐
│          │          │          │          │
│     D    │     O    │     N    │     T    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│    Qu    │     U    │     I    │     T    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     B    │     P    │     Y    │     L    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     G    │     F    │     H    │     A    │
│          │          │          │          │
└───────────────────────────────────────────┘
dontquitbpylgfha
```

Solve a boggle game by passing the letters row by row (if there is 'Qu' on any face up dice, write only q):

```bash
$ python3 src/boggle/app.py solve olqprzmxsdekgnuw
zen, zens, med, eds, ens, gnu, new, wen, wens,
[found: 9]
```

If you want to see more details, for example, the game board layout, the dictionary being used to validate words etc, add `--verbose`/`-v` flag:

```bash
$ python3 src/boggle/app.py solve olqprzmxsdekgnuw -v
┌───────────────────────────────────────────┐
│          │          │          │          │
│     O    │     L    │    Qu    │     P    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     R    │     Z    │     M    │     X    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     S    │     D    │     E    │     K    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     G    │     N    │     U    │     W    │
│          │          │          │          │
└───────────────────────────────────────────┘
Dictionary powered by 'PyEnchant'
zen, zens, med, eds, ens, gnu, new, wen, wens,
[found: 9]
```

You can pass your own list of words in a file (each word in its own line) as a dictionary as well. Just pass the filename with flag `--dict-file`/`-d`:

```bash
$ python3 src/boggle/app.py solve olqprzmxsdekgnuw -v -d data/dictionary/unix-words.txt
┌───────────────────────────────────────────┐
│          │          │          │          │
│     O    │     L    │    Qu    │     P    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     R    │     Z    │     M    │     X    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     S    │     D    │     E    │     K    │
│          │          │          │          │
│──────────┼──────────┼──────────┼──────────│
│          │          │          │          │
│     G    │     N    │     U    │     W    │
│          │          │          │          │
└───────────────────────────────────────────┘
Dictionary powered by 'data/dictionary/unix-words.txt'
lors, zen, snew, ens, ked, gnu, new, unde, wun, wen,
[found: 10]
```
