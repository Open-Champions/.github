#!/usr/bin/env python3
"""Render the org profile from public, pinned source snapshots and milestone issues."""
import argparse
from datetime import datetime
from html import escape
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

ORG = 'Open-Champions'
ROOT = Path(__file__).resolve().parents[1]
REPOS = ['champions-return-to-arms-re', 'champions-return-to-arms', 'champions-of-norrath', 'open-champions-godot']
START, END = '<!-- dashboard:start -->', '<!-- dashboard:end -->'


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True, timeout=90).stdout


def ratio(done, total):
    if not isinstance(done, int) or not isinstance(total, int) or total <= 0 or not 0 <= done <= total:
        raise ValueError('invalid progress counts')
    return 100 * done / total


def checklist(body):
    start, end = '<!-- progress:start -->', '<!-- progress:end -->'
    if body.count(start) != 1 or body.count(end) != 1:
        raise ValueError('milestone issue must contain exactly one progress block')
    text = body.split(start, 1)[1].split(end, 1)[0]
    rows = re.findall(r'^- \[([ xX])\] (.+)$', text, re.M)
    if not rows or len(rows) > 100 or any(line.startswith('- ') and not re.match(r'^- \[([ xX])\] .+$', line) for line in text.splitlines()):
        raise ValueError('invalid milestone checklist')
    if len({label for _, label in rows}) != len(rows):
        raise ValueError('duplicate milestones')
    return sum(mark.lower() == 'x' for mark, _ in rows), len(rows)


def coverage(table):
    rows = []
    for line in table.splitlines():
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) == 6 and cells[2].isdigit() and cells[3].isdigit():
            total, named = int(cells[2]), int(cells[3])
            ratio(named, total)
            rows.append({'area': cells[0].strip('*'), 'total': total, 'named': named})
    totals = [row for row in rows if row['area'] == 'all']
    areas = [row for row in rows if row['area'] != 'all']
    if len(totals) != 1 or not areas or len({r['area'] for r in areas}) != len(areas):
        raise ValueError('unrecognized research coverage table')
    for field in ('total', 'named'):
        if sum(row[field] for row in areas) != totals[0][field]:
            raise ValueError('research area totals disagree')
    return totals[0], areas


def source_stats(sources):
    revisions = {repo: run(['git', 'rev-parse', 'HEAD'], sources / repo).strip() for repo in REPOS}
    research, areas = coverage(run([sys.executable, '-I', 'tools/coverage.py'], sources / REPOS[0]))
    # The source project's own verifier checks ledger, index, source and verifier
    # fingerprints. Never sum an unvalidated saved receipt or expose private bytes.
    rta = json.loads(run([sys.executable, '-I', 'tools/rebuild.py', 'progress', '--json'], sources / REPOS[1]))
    if rta.get('report_supplied') is not True:
        raise ValueError('RTA progress lacks a validated public verification receipt')
    ratio(rta['bytes_matched'], rta['text_bytes_total'])
    issues = {}
    for repo, number, key in [(REPOS[3], 2, 'native'), (REPOS[2], 1, 'norrath')]:
        issue = json.loads(run(['gh', 'api', f'repos/{ORG}/{repo}/issues/{number}']))
        done, total = checklist(issue['body'])
        issues[key] = {'done': done, 'total': total, 'url': issue['html_url'], 'updated_at': issue['updated_at']}
    return {'revisions': revisions, 'research': research, 'areas': areas, 'rta': rta, 'milestones': issues}


def card(title, label, done, total, note, color='#dfbe79', digits=1):
    pct = ratio(done, total)
    # No artificial minimum fill: 24 matched bytes must not look like 1%.
    width = 844 * pct / 100
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="124" viewBox="0 0 900 124" role="img" aria-label="{escape(title)}: {escape(label)} {pct:.{digits}f}%">
<rect width="900" height="124" rx="12" fill="#111d22"/>
<g font-family="Arial, sans-serif" fill="#edf2ee">
<text x="28" y="30" font-size="19" font-weight="bold">{escape(title)}</text>
<text x="872" y="30" text-anchor="end" font-size="18" fill="{color}">{pct:.{digits}f}%</text>
<text x="28" y="55" font-size="15" fill="#bfd0ce">{escape(label)} · {done:,} / {total:,}</text>
<rect x="28" y="68" width="844" height="10" rx="5" fill="#30434b"/>
<rect x="28" y="68" width="{width:.6f}" height="10" rx="5" fill="{color}"/>
<text x="28" y="104" font-size="13" fill="#a8bdbb">{escape(note)}</text>
</g></svg>\n'''


def area_svg(areas):
    height = 78 + 48 * len(areas)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-label="Research function naming by subsystem">', f'<rect width="900" height="{height}" rx="12" fill="#111d22"/>', '<g font-family="Arial, sans-serif" fill="#edf2ee"><text x="28" y="30" font-size="19">Research areas · functions named</text><text x="28" y="52" font-size="13" fill="#a8bdbb">Function identification across the original game engine, grouped by subsystem.</text>']
    for i, row in enumerate(areas):
        y = 83 + i * 48
        pct = ratio(row['named'], row['total'])
        parts += [f'<text x="28" y="{y}" font-size="15">{escape(row["area"])}</text>', f'<text x="872" y="{y}" text-anchor="end" font-size="14">{row["named"]:,} / {row["total"]:,} · {pct:.1f}%</text>', f'<rect x="28" y="{y+9}" width="844" height="7" rx="3" fill="#30434b"/>', f'<rect x="28" y="{y+9}" width="{844*pct/100:.6f}" height="7" rx="3" fill="#79c6b6"/>']
    return ''.join(parts) + '</g></svg>\n'


def render(data, root=ROOT):
    folder = root / 'profile/progress'
    folder.mkdir(parents=True, exist_ok=True)
    snapshot = folder / 'snapshot.json'
    old = json.loads(snapshot.read_text()) if snapshot.exists() else None
    generator_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    if old and old.get('data') == data and old.get('generator_sha256') == generator_hash:
        print('Published inputs unchanged; preserving snapshot and commit history.')
        return
    now = datetime.now(ZoneInfo('America/Chicago')).strftime('%Y-%m-%d %H:%M %Z')
    native, norrath = data['milestones']['native'], data['milestones']['norrath']
    rta, research = data['rta'], data['research']
    cards = {
        'rta': card('Return to Arms · PS2 source rebuild', 'Verified matching code bytes', rta['bytes_matched'], rta['text_bytes_total'], f'{rta["functions_matched"]:,} / {rta["functions_total"]:,} complete functions rebuilt and verified against the original PS2 code.', digits=4),
        'research': card('Return to Arms · research coverage', 'Functions with names', research['named'], research['total'], 'Tracks function identification across the original game engine.', '#79c6b6'),
        'native': card('Godot client · Mac/macOS & Windows PC', 'Delivered roadmap milestones', native['done'], native['total'], 'Both Champions games. Target: native play without a PS2 emulator. Milestones vary in size.'),
        'norrath': card('Champions of Norrath · baseline setup', 'Verified setup milestones', norrath['done'], norrath['total'], 'Establishing the game-specific foundation for Norrath source reconstruction.', '#a6b9d3'),
    }
    cards['research-areas'] = area_svg(data['areas'])
    filenames = {}
    for name, svg in cards.items():
        filenames[name] = f'{name}-{sha256(svg.encode()).hexdigest()[:16]}.svg'
        (folder / filenames[name]).write_text(svg, encoding='utf-8')
        # Content-addressed image paths prevent cached captions surviving an update.
        for previous in folder.glob(f'{name}*.svg'):
            if re.fullmatch(re.escape(name) + r'(?:-[0-9a-f]{16})?\.svg', previous.name) and previous.name != filenames[name]:
                previous.unlink()
    snapshot.write_text(json.dumps({'updated': now, 'generator_sha256': generator_hash, 'data': data}, indent=2) + '\n', encoding='utf-8')
    base = f'https://raw.githubusercontent.com/{ORG}/.github/main/profile/progress'
    links = {'rta': f'https://github.com/{ORG}/{REPOS[1]}/blob/{data["revisions"][REPOS[1]]}/targets/SLUS-20973/verification.json', 'research': f'https://github.com/{ORG}/{REPOS[0]}/blob/{data["revisions"][REPOS[0]]}/docs/STATUS.md', 'native': native['url'], 'norrath': norrath['url']}
    block = f'''{START}
### Project progress

[![Progress refresh](https://github.com/{ORG}/.github/actions/workflows/progress.yml/badge.svg)](https://github.com/{ORG}/.github/actions/workflows/progress.yml)

Automatically checked every 15 minutes; GitHub scheduling and image caching can delay display.
Last published data update: **{now}**. [How these bars work](https://github.com/{ORG}/.github/blob/main/PROGRESS.md).

'''
    for name in ('rta', 'norrath', 'native', 'research'):
        block += f'[![{name} progress]({base}/{filenames[name]})]({links[name]})\n\n'
    block += f'''<details>
<summary>Research progress by subsystem</summary>

![Research areas]({base}/{filenames['research-areas']})

</details>

**Our goal: both Champions games running natively on Mac/macOS and Windows PCs, without a PS2 emulator. Each bar tracks its own development measure.**
{END}'''
    readme = root / 'profile/README.md'
    text = readme.read_text()
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('profile must contain one dashboard block; refusing to replace unrelated text')
    text = text.split(START)[0] + block + text.split(END)[1]
    readme.write_text(text, encoding='utf-8')
    print('Updated four project bars, research-area bars, source snapshot and profile.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=ROOT / '.sources')
    args = parser.parse_args()
    render(source_stats(args.sources.resolve()))


if __name__ == '__main__':
    main()
