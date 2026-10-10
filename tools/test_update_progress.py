import tempfile
import json
import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import update_progress as progress


class ProgressTests(unittest.TestCase):
    def test_checklist_counts_only_marked_scope(self):
        text = '- [x] unrelated\n<!-- progress:start -->\n- [x] core\n- [ ] scene\n<!-- progress:end -->'
        self.assertEqual(progress.checklist(text), (1, 2))
        for malformed in ('- [x] no block', '<!-- progress:start -->\n- [yes] bad\n<!-- progress:end -->', '<!-- progress:start -->\n- [ ] same\n- [x] same\n<!-- progress:end -->'):
            with self.assertRaises(ValueError):
                progress.checklist(malformed)

    def test_research_uses_function_counts_not_code_size_percent(self):
        table = '| engine | range | 20 | 5 | 90% | info |\n| **all** | | 20 | 5 | 90% | |'
        total, areas = progress.coverage(table)
        self.assertEqual(progress.ratio(total['named'], total['total']), 25)
        self.assertEqual(len(areas), 1)
        with self.assertRaises(ValueError):
            progress.coverage(table.replace('| | 20 | 5', '| | 21 | 5'))

    def test_card_escapes_text_and_preserves_tiny_real_fill(self):
        svg = progress.card('a < b', 'bytes & count', 24, 3038272, 'No "game" proof', digits=4)
        root = ET.fromstring(svg)
        fills = root.findall('.//{http://www.w3.org/2000/svg}rect')
        self.assertAlmostEqual(float(fills[-1].attrib['width']), 844 * 24 / 3038272, places=6)
        self.assertIn('0.0008%', svg)
        self.assertIn('a &lt; b', svg)
        self.assertIn('bytes &amp; count', svg)
        with self.assertRaises(ValueError):
            progress.card('bad', 'counts', 2, 1, '')

    def test_stale_source_verification_stops_collection(self):
        calls = ['a'*40]*4 + ['| engine | range | 1 | 1 | 100% | info |\n| **all** | | 1 | 1 | 100% | |', RuntimeError('stale report')]
        with patch.object(progress, 'run', side_effect=calls), self.assertRaisesRegex(RuntimeError, 'stale report'):
            progress.source_stats(Path('/unused'))

    def pr(self, **updates):
        result = {'merged': False, 'state': 'open', 'draft': True,
                  'head': {'sha': 'a'*40, 'repo': {'full_name': progress.NORRATH, 'fork': False}},
                  'base': {'repo': {'full_name': progress.NORRATH, 'fork': False}}}
        result.update(updates)
        return result

    def test_draft_uses_separate_exact_snapshot_and_label(self):
        with tempfile.TemporaryDirectory() as folder:
            sources = Path(folder)
            with patch.object(progress, 'run', side_effect=[json.dumps(self.pr()), '', '', '', 'a'*40, '']) as run:
                snapshot, info = progress.norrath_snapshot(sources)
            self.assertNotEqual(snapshot, sources / progress.REPOS[2])
            self.assertEqual(info['label'], 'Draft PR #2 / unmerged')
            self.assertEqual(info['revision'], 'a'*40)
            fetch = run.call_args_list[2].args[0]
            self.assertEqual(fetch[-1], 'a'*40)
            self.assertEqual(fetch[-2], f'https://github.com/{progress.NORRATH}.git')

    def test_fork_closed_and_merged_pr_states(self):
        fork = self.pr()
        fork['head']['repo']['full_name'] = 'someone/champions-of-norrath'
        with patch.object(progress, 'run', return_value=json.dumps(fork)), self.assertRaisesRegex(ValueError, 'fork'):
            progress.norrath_snapshot(Path('/unused'))
        with patch.object(progress, 'run', return_value=json.dumps(self.pr(state='closed'))):
            folder, info = progress.norrath_snapshot(Path('/unused'))
        self.assertIsNone(folder)
        self.assertFalse(info['available'])
        self.assertNotIn('bytes_matched', info)
        with patch.object(progress, 'run', side_effect=[json.dumps(self.pr(merged=True, state='closed')), 'b'*40, 'b'*40, '']):
            folder, info = progress.norrath_snapshot(Path('/unused'))
        self.assertEqual(folder, Path('/unused') / progress.REPOS[2])
        self.assertEqual(info['label'], 'Main branch')
        self.assertEqual(info['revision'], 'b'*40)

    def test_snapshot_consistency_rejects_wrong_revision_or_dirty_files(self):
        for responses in [('b'*40,), ('a'*40, ' M reconstructed/source.cpp')]:
            with patch.object(progress, 'run', side_effect=responses), self.assertRaisesRegex(ValueError, 'snapshot changed'):
                progress.clean_snapshot(Path('/unused'), 'a'*40)

    def test_stale_receipt_or_missing_source_stops_norrath_counts(self):
        for message in ('stale report: source changed', 'missing reconstructed/source.cpp'):
            failure = subprocess.CalledProcessError(1, ['validator'], stderr=message)
            with patch.object(progress, 'norrath_snapshot', return_value=(Path('/unused'), {'revision': 'a'*40})), \
                    patch.object(progress, 'run', side_effect=failure) as run, \
                    self.assertRaises(subprocess.CalledProcessError):
                progress.norrath_stats(Path('/unused'))
            self.assertIn('--require-matches', run.call_args.args[0])
            self.assertTrue(run.call_args.kwargs['public_code'])

    def test_validator_environment_has_no_job_tokens(self):
        with patch.dict(progress.os.environ, {'GH_TOKEN': 'secret', 'GITHUB_TOKEN': 'secret', 'OTHER_SECRET': 'secret'}), \
                patch.object(progress.subprocess, 'run') as run:
            progress.run(['python', '-I', 'validator.py'], public_code=True)
        env = run.call_args.kwargs['env']
        for key in ('GH_TOKEN', 'GITHUB_TOKEN', 'OTHER_SECRET'):
            self.assertNotIn(key, env)

    def test_validated_counts_use_only_main_text_and_separate_data(self):
        with tempfile.TemporaryDirectory() as folder:
            snapshot = Path(folder)
            target = snapshot / progress.NORRATH_TARGET
            target.mkdir(parents=True)
            files = {
                'rebuild.json': {'target': {'baseline_sha256': 'identity', 'text': {'address': '0x00100000', 'size': 100}},
                    'functions': [{'address': '0x00100000', 'size': 8}, {'address': '0x00500000', 'size': 16}],
                    'data_objects': [{'size': 4}]},
                'baseline.json': {'executable': {'sha256': 'identity'}, 'sections': [
                    {'name': '.text', 'address': 0x100000, 'size': 100, 'index': 1}]},
                'symbol-summary.json': {'baseline_sha256': 'identity', 'summary': {'executable_sections': [
                    {'name': '.text', 'section_bytes': 100, 'section_index': 1, 'function_symbols': 10}]}},
            }
            for name, value in files.items():
                (target / name).write_text(json.dumps(value))
            with patch.object(progress, 'norrath_snapshot', return_value=(snapshot, {'revision': 'a'*40})), \
                    patch.object(progress, 'run', return_value=''), patch.object(progress, 'clean_snapshot'):
                stats = progress.norrath_stats(snapshot)
                self.assertEqual((stats['functions_matched'], stats['bytes_matched']), (1, 8))
                self.assertEqual((stats['data_objects_matched'], stats['data_bytes_matched']), (1, 4))
                files['symbol-summary.json']['summary']['executable_sections'][0]['section_bytes'] = 200
                (target / 'symbol-summary.json').write_text(json.dumps(files['symbol-summary.json']))
                with self.assertRaisesRegex(ValueError, 'disagree'):
                    progress.norrath_stats(snapshot)

    def test_render_displays_draft_and_withdraws_closed_pr_counts(self):
        data = {'revisions': {repo: 'a'*40 for repo in progress.REPOS},
                'rta': {'bytes_matched': 8, 'text_bytes_total': 10000, 'functions_matched': 1, 'functions_total': 100},
                'research': {'named': 1, 'total': 2}, 'areas': [{'area': 'engine', 'named': 1, 'total': 2}],
                'milestones': {name: {'done': 1, 'total': 2, 'url': 'https://example.com'} for name in ('native', 'norrath')},
                'norrath_source': {'available': True, 'label': 'Draft PR #2 / unmerged', 'bytes_matched': 160,
                    'text_bytes_total': 2209032, 'functions_matched': 11, 'functions_total': 5390,
                    'data_objects_matched': 4, 'data_bytes_matched': 13, 'url': 'https://example.com'}}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'profile').mkdir()
            (root / 'profile/README.md').write_text(progress.START + '\n' + progress.END)
            progress.render(data, root)
            svgs = list((root / 'profile/progress').glob('norrath-source-*.svg'))
            self.assertEqual(len(svgs), 1)
            text = svgs[0].read_text()
            ET.fromstring(text)
            self.assertIn('Draft PR #2 / unmerged', text)
            self.assertIn('160 / 2,209,032', text)
            self.assertIn('4 data owners / 13 bytes separately', text)
            self.assertIn('No whole-game or runtime proof', text)
            data['norrath_source'] = {'available': False, 'label': 'PR #2 closed without merging', 'url': 'https://example.com'}
            progress.render(data, root)
            remaining = list((root / 'profile/progress').glob('norrath-source-*.svg'))
            self.assertEqual(len(remaining), 1)
            self.assertIn('previous draft counts withdrawn', remaining[0].read_text())
            self.assertNotIn('160 /', remaining[0].read_text())

    def test_unchanged_snapshot_does_not_create_timestamp_commits(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / 'profile/progress'
            target.mkdir(parents=True)
            snapshot = target / 'snapshot.json'
            snapshot.write_text(progress.json.dumps({'updated': 'old', 'generator_sha256': progress.sha256(Path(progress.__file__).read_bytes()).hexdigest(), 'data': {'same': True}}))
            before = snapshot.read_bytes()
            progress.render({'same': True}, root)
            self.assertEqual(snapshot.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
