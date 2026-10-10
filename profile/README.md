<p align="center">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-return-to-arms-logo.png" alt="Champions: Return to Arms" width="512">
</p>

<h1 align="center">Open Champions</h1>
<p align="center"><strong>Understand the game. Restore dependable online play. Build in the open.</strong></p>

We are a community preservation and reverse-engineering project for **Champions: Return to Arms**, the Snowblind Studios action RPG for PlayStation 2.

Our first target is the US v2.00 release, **SLUS-20973**. We are tracing the causes of online desync and lag, documenting the Snowblind engine, and building tools that let anyone with their own disc help.

### Start here

| | |
|---|---|
| **Source, tools & research** | [champions-return-to-arms-re](https://github.com/Open-Champions/champions-return-to-arms-re) |
| **Progress by area** | [Current coverage and subsystem notes](https://github.com/Open-Champions/champions-return-to-arms-re/blob/main/docs/STATUS.md) |
| **What we know about online bugs** | [Evidence ledger](https://github.com/Open-Champions/champions-return-to-arms-re/blob/main/FINDINGS.md) |
| **Help build it** | [Contributor guide](https://github.com/Open-Champions/champions-return-to-arms-re/blob/main/CONTRIBUTING.md) · [Open issues](https://github.com/Open-Champions/champions-return-to-arms-re/issues) |

### Where we are

- **7,732 indexed functions** and **403 recovered class names** provide a map of the executable.
- **120 level scripts** can be decoded with the project tools.
- The online lockstep model, input encoding and local-player prediction are mapped.
- Reverse engineering is underway across the game. Function names measure mapping coverage, not a percentage of a completed port.
- **The arena desync remains unresolved. Proposed game patches have not been validated in two running clients.**

### Join the work

We welcome reverse engineers, Python tool contributors, documentation writers, and players who can reproduce network bugs with two PCSX2 clients. Pick a small task, coordinate in an issue, and include evidence with your contribution.

Tools and research are open source. Use your own game disc to generate local analysis files. Game executables, BIOS files, disc images, extracted assets, and raw decompiler output are not distributed by the research repository.

### Related projects

[Champions Reborn](https://github.com/HikikoMarmy/Champions-Reborn-Server) supplies the community lobby server. Open Champions focuses on understanding and improving the game client. [Open-BFME](https://github.com/Open-BFME) helped inspire the open community approach.

---

Independent community project; not affiliated with or endorsed by the game's rights holders. The Champions: Return to Arms name and logo belong to their respective owners. [Artwork credits](https://github.com/Open-Champions/.github/blob/main/ARTWORK.md).
