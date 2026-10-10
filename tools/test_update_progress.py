import tempfile
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
