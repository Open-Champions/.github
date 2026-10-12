<p align="center">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-of-norrath-logo.png" alt="Champions of Norrath" width="300">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-return-to-arms-logo.png" alt="Champions: Return to Arms" width="300">
</p>

<h1 align="center">Open Champions</h1>
<p align="center"><strong>Both Champions games. Native Mac &amp; Windows PC play.</strong></p>

An independent community project for **Champions of Norrath** and **Champions: Return to Arms**.
We reconstruct source from evidence, investigate online bugs, and develop a shared Godot client
targeting **MacBooks and other Macs (macOS) and Windows PCs** for **both games**,
using each player's original game data. The goal is native play **without a PS2 emulator**.

<!-- dashboard:start -->
### Project progress

[![Progress refresh](https://github.com/Open-Champions/.github/actions/workflows/progress.yml/badge.svg)](https://github.com/Open-Champions/.github/actions/workflows/progress.yml)

Scheduled to refresh every 15 minutes; GitHub can delay runs and image updates.
Last published data update: **2026-10-12 03:07 CDT**. [How these bars work](https://github.com/Open-Champions/.github/blob/main/PROGRESS.md).

[![rta progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/rta-6198e899907ed27a.svg)](https://github.com/Open-Champions/champions-return-to-arms/blob/adb1e7c3a9b1c41e86aed3f9f73cfef95c088c36/targets/SLUS-20973/verification.json)

[![norrath-source progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/norrath-source-78c8dc3935ae3478.svg)](https://github.com/Open-Champions/champions-of-norrath/pull/2)

[![norrath progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/norrath-6b49e4c93f9ab2e0.svg)](https://github.com/Open-Champions/champions-of-norrath/issues/1)

[![native progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/native-27467079eb7e8282.svg)](https://github.com/Open-Champions/open-champions-godot/issues/2)

[![research progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/research-4ecd83ded3ca2069.svg)](https://github.com/Open-Champions/champions-return-to-arms-re/blob/817ccfb77e0bf9ffa82e4c49b113bf67f4a7b4c2/docs/STATUS.md)

<details>
<summary>Research progress by subsystem</summary>

![Research areas](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/research-areas-a5ebb0da0d9bca1d.svg)

</details>

**Our goal: both Champions games running natively on Mac/macOS and Windows PCs, without a PS2 emulator. Each bar tracks its own development measure.**
<!-- dashboard:end -->

### Our repositories

| Repository | What belongs there | Current state |
|---|---|---|
| [champions-of-norrath](https://github.com/Open-Champions/champions-of-norrath) | Norrath's PS2 source reconstruction | Hash-pinned reconstruction in draft PR #2; exact retail pressing unresolved |
| [champions-return-to-arms](https://github.com/Open-Champions/champions-return-to-arms) | Return to Arms' PS2 source reconstruction | Exact-function verifier and recorded byte-matching progress |
| [open-champions-godot](https://github.com/Open-Champions/open-champions-godot) | Godot client for both games on Mac/macOS & Windows PC | RTA archive, texture, model and joint inspection; bounded skinning bridge; gameplay ahead |
| [champions-return-to-arms-re](https://github.com/Open-Champions/champions-return-to-arms-re) | Existing research, symbols, file formats and online-bug evidence | Active subsystem and network research |

Each piece has one active home. The source repositories preserve the original PS2 targets;
the shared Godot client brings both games toward native Mac and Windows play.
Follow the bars above for source reconstruction, research, and native-client milestones.

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
