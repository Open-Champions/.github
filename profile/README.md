<p align="center">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-of-norrath-logo.png" alt="Champions of Norrath" width="300">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-return-to-arms-logo.png" alt="Champions: Return to Arms" width="300">
</p>

<h1 align="center">Open Champions</h1>
<p align="center"><strong>Preserve both games. Understand their engines. Build native play.</strong></p>

An independent community project for **Champions of Norrath** and **Champions: Return to Arms**.
We reconstruct source from evidence, investigate online bugs, and develop a shared Godot client
for native Mac and Windows play using each player's original game data.

### Our repositories

| Repository | What belongs there | Current state |
|---|---|---|
| [champions-of-norrath](https://github.com/Open-Champions/champions-of-norrath) | Norrath's PS2 source reconstruction | Baseline intake and research setup; no reconstructed functions yet |
| [champions-return-to-arms](https://github.com/Open-Champions/champions-return-to-arms) | Return to Arms' PS2 source reconstruction | Exact-function verifier, recorded progress and the first verified C++ leaf |
| [open-champions-godot](https://github.com/Open-Champions/open-champions-godot) | Shared native client for both games | Tested C++ archive-inspection foundation; Godot integration and gameplay ahead |
| [champions-return-to-arms-re](https://github.com/Open-Champions/champions-return-to-arms-re) | Existing research, symbols, file formats and online-bug evidence | Active subsystem and network research |

Each piece has one active home. The source repositories preserve the original PS2 targets;
the Godot repository develops native behavior. A function match, a named symbol, and a
working archive inspector measure different things. **Neither game is playable natively yet.**

### Start here

- [Return to Arms reconstruction progress](https://github.com/Open-Champions/champions-return-to-arms#readme)
- [Norrath baseline checklist](https://github.com/Open-Champions/champions-of-norrath/blob/main/targets/README.md)
- [Shared native-client roadmap](https://github.com/Open-Champions/open-champions-godot/blob/main/docs/ROADMAP.md)
- [Research coverage](https://github.com/Open-Champions/champions-return-to-arms-re/blob/main/docs/STATUS.md)
- [Online bug evidence](https://github.com/Open-Champions/champions-return-to-arms-re/blob/main/FINDINGS.md)

### Join the work

Choose a repository, read its contributor and agent instructions, and claim a small task.
We welcome reverse engineers, C++ and Godot contributors, tool developers, and players who
can reproduce network bugs. Publish evidence with each contribution. Original executables,
disc/BIOS files, extracted game assets and raw decompiler output stay private.

[Champions Reborn](https://github.com/HikikoMarmy/Champions-Reborn-Server) supplies the existing
community lobby-server work; we are not creating a duplicate server repository.
[Open-BFME](https://github.com/Open-BFME) helped inspire this project's organization and measured reconstruction approach.

---

Independent community project; not affiliated with or endorsed by the games' rights holders.
Game names and wordmarks belong to their respective owners and are excluded from the software
license. [Artwork credits](https://github.com/Open-Champions/.github/blob/main/ARTWORK.md).
