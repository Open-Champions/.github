# Organization progress bars

The organization profile is scheduled to check published project state every 15 minutes through
[Refresh project progress](https://github.com/Open-Champions/.github/actions/workflows/progress.yml).
It also refreshes when this generator changes and supports **Run workflow** for
an immediate refresh. GitHub scheduling and image caches can delay display.
Unchanged input produces no new commit. The profile's date means the last data
update; the workflow badge links to the latest refresh runs.

## What each bar measures

| Part | Source | Meaning |
|---|---|---|
| RTA source rebuild | Source repo `tools/rebuild.py progress --json` | Matching bytes divided by original `.text` bytes; complete function count shown separately. Its own validator rejects stale source, flags, ledger, index or verifier fingerprints. This job does not compile against a private original. |
| Norrath source rebuild | Same-repository [PR #2](https://github.com/Open-Champions/champions-of-norrath/pull/2), at its exact published head commit; default branch after merge | Its unchanged `rebuild.py check --report targets/SLUS-20565/verification.json --require-matches` must validate every source and receipt fingerprint first. The bar labels draft/unmerged status and counts only matching main `.text` bytes, with main `.text` functions and matched data owners/bytes listed separately. No whole-game or runtime proof. |
| RTA research | Research repo `tools/coverage.py` | Named functions divided by indexed functions, overall and by subsystem. It does not count code-size percentage, understanding, or decompilation as source reconstruction. |
| Native Godot client | [Native milestones](https://github.com/Open-Champions/open-champions-godot/issues/2) | Checked, evidenced milestones divided by planned milestones. Milestones vary in size and track the roadmap toward native Mac and Windows play for both games. |
| Norrath baseline setup | [Independent baseline checklist](https://github.com/Open-Champions/champions-of-norrath/issues/1) | Verified setup milestones. Separate from the source rebuild bar; completed setup does not establish a linked or playable game. |

Each bar uses the specific measure listed above. The project goal is native Mac
and Windows play for both Champions games. Matching bytes are drawn at their
true proportion of the original code section.

## Keeping it current

RTA reconstruction and research update automatically from the published default
branches. Norrath source progress currently follows only the explicitly selected,
first-party PR #2. The generator verifies its repository identity, fetches its exact
head SHA into a separate checkout, checks the checkout remains clean, and runs
its validator without job tokens in the environment. Fork code is refused. After
merge it follows the default branch; closure without merging withdraws the draft
counts and renders unavailable. For native or Norrath milestones, update the corresponding issue's
checkbox only after the stated evidence exists, and link it in that item.
The dashboard reads only the checklist between `progress:start` and
`progress:end`; work outside that block does not affect the count. New milestones
can be added there, making the changed denominator explicit.

`profile/progress/snapshot.json` records the exact source commits and checklist
update times. The generated files are owned by this workflow. Change the source
metrics or tracker issues rather than manually painting a bar or editing a
percentage. A failed fetch, stale receipt, or malformed checklist fails the job
and preserves the previous dated snapshot; a failure is visible through its
workflow badge. Original executables, assets and private working files are never
read or uploaded by this workflow.

## Local verification

Clone the four public repositories into `.sources/<repository-name>`, then run:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/update_progress.py
```

GitHub CLI must have permission to read the two public tracking issues and Norrath PR #2. The generator fetches the separate PR snapshot automatically. Publication
uses only this repository's standard workflow token; no new cross-repository
write credential is required. The generator updates only its bounded README
section and `profile/progress/`, preserving branding and unrelated profile text.
