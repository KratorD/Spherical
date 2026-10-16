# Spherical (ZX Spectrum 48K, 1989) — documented reverse engineering

[Versión en español: README_es.md](README_es.md)

A complete analysis of the Z80 code of **Spherical** (Rainbow Arts / Electronic Zoo, 1989; a static-screen puzzle-platformer in the style of *Solomon's Key*), written for anyone who wants to understand it, mod it or port it without repeating the work.

> The game's rights belong to their holders (according to our research, currently **Ziggurat Interactive**). This repository **does not contain the game**: no tapes, no snapshots, no disassembly with the original bytes, no graphics and no levels. It only holds our own documentation, a SkoolKit control file and tools. You need **your own legitimate copy**. If the rights holder asks for anything to be removed, it will be removed.

The documentation itself is written in **Spanish**; addresses, register names and tables are language-neutral, so it is usable with basic Spanish and a translator.

## What is here

| Path | Contents |
|---|---|
| [`docs/Spherical_ZX_Spectrum_Analisis_Completo.md`](docs/Spherical_ZX_Spectrum_Analisis_Completo.md) | **The main document** (Spanish): tape and loading, memory map, main loop, data structures, level format, graphics and masks, every mechanic (sphere, blocks, orb, energy, 19 enemy types, 2 players…), a reference of 81 routines, a modding guide with tested recipes, and what is verified and what is not. |
| [`docs/verificacion.md`](docs/verificacion.md), [`docs/cobertura.md`](docs/cobertura.md) | What was tested and how; instruction coverage (4689/4689 instructions executed by at least one test, with the caveats explained). |
| [`control/spherical_anotado.ctl`](control/spherical_anotado.ctl) | A [SkoolKit](https://skoolkit.ca/) control file with the code/data split and **all the analysis comments**. It contains no bytes of the game. |
| [`herramientas/`](herramientas/) | Python scripts built on SkoolKit's Z80 simulator: key injection, coverage, extraction, per-mechanic tests, a TZX tape patcher. |

## How to regenerate the annotated disassembly

1. Take a snapshot (`.sna`/`.z80`) of your own copy of the game running (world 0 loaded).
2. With SkoolKit ≥ 9:
   ```bash
   sna2skool.py -H -c control/spherical_anotado.ctl your_snapshot.sna > spherical_anotado.skool
   ```
3. You get the `.skool` with line-by-line commented code (in our analysis it reassembles byte-identical to RAM `$5B00-$FFFF`). **Do not publish it.**

Some tools contain hard-coded paths (`/home/claude/...`) from our environment; adjust them to your setup.

## What we know, in short

- Code at `$A7CC–$D030`; main loop at `$AAC7` with **no synchronisation to the interrupt** (speed depends on the level contents; a tested speed limiter is in the modding guide).
- 9 worlds of 10 levels loaded from tape (81 real levels; 1P and 2P levels differ); 16×16 sprites with a mask computed from two silhouette tables.
- Energy is a bar shared by both players; at 0 → *Game Over*. The game has **no lives**: there is a retry counter (key R).
- Anything not measured is flagged as an assumption; the only thing left unmeasured is the **speed on real hardware**.

## License

- Scripts in `herramientas/`: MIT (see [`LICENSE`](LICENSE)).
- Documentation and control file: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (proposed; change if you prefer another).
- No license here covers the original game or its data.
