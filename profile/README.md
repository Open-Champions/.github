<p align="center">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-of-norrath-logo.png" alt="Champions of Norrath" width="300">
  <img src="https://raw.githubusercontent.com/Open-Champions/.github/main/profile/assets/champions-return-to-arms-logo.png" alt="Champions: Return to Arms" width="300">
</p>

<h1 align="center">Open Champions</h1>
<p align="center"><strong>Preserve both games. Understand their engines. Build native play.</strong></p>

An independent community project for **Champions of Norrath** and **Champions: Return to Arms**.
We reconstruct source from evidence, investigate online bugs, and develop a shared Godot client
for native Mac and Windows play using each player's original game data.

<!-- dashboard:start -->
### Project progress

[![Progress refresh](https://github.com/Open-Champions/.github/actions/workflows/progress.yml/badge.svg)](https://github.com/Open-Champions/.github/actions/workflows/progress.yml)

Automatically checked every 15 minutes; GitHub scheduling and image caching can delay display.
Last published data update: **2026-10-10 02:44 CDT**. [How these bars work](https://github.com/Open-Champions/.github/blob/main/PROGRESS.md).

[![rta progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/rta-579923a6e33eb08a.svg)](https://github.com/Open-Champions/champions-return-to-arms/blob/23e2246c457a2e4b6f57e52cefa337caeae0f7f3/targets/SLUS-20973/verification.json)

[![norrath progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/norrath-c5116c78228c08ae.svg)](https://github.com/Open-Champions/champions-of-norrath/issues/1)

[![native progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/native-ce047bf14fcdc2f7.svg)](https://github.com/Open-Champions/open-champions-godot/issues/2)

[![research progress](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/research-7a57100dee4bdfa5.svg)](https://github.com/Open-Champions/champions-return-to-arms-re/blob/7bb716d6fa471e2405d37153f3d60ad0b2e4e1a8/docs/STATUS.md)

<details>
<summary>Research progress by subsystem</summary>

![Research areas](https://raw.githubusercontent.com/Open-Champions/.github/main/profile/progress/research-areas-5239fb328f25f21a.svg)

</details>

**Our goal: both Champions games running natively on Mac and Windows. Each bar tracks its own development measure.**
<!-- dashboard:end -->

### Our repositories

| Repository | What belongs there | Current state |
|---|---|---|
| [champions-of-norrath](https://github.com/Open-Champions/champions-of-norrath) | Norrath's PS2 source reconstruction | Baseline intake and research setup |
| [champions-return-to-arms](https://github.com/Open-Champions/champions-return-to-arms) | Return to Arms' PS2 source reconstruction | Exact-function verifier and recorded byte-matching progress |
| [open-champions-godot](https://github.com/Open-Champions/open-champions-godot) | Shared native client for both games | Native Godot archive browser and C++ inspector; asset decoding and gameplay ahead |
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
