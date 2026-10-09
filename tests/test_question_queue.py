import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('queue_module', Path(__file__).resolve().parents[1] / 'scripts/question_queue.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class QueueTest(unittest.TestCase):
    def test_handoff_and_no_repeat(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'QUESTIONS.json').write_text('{"questions": []}')
            template = '# Content Pipeline\n\n## NEXT UP\n\n- topic goes here\n\n## BRIEF\n\n[researcher writes here]\n\nSTATUS\n\nCurrent stage: pending\n'
            (root / 'PIPELINE.md').write_text(template)
            source = root / 'input.txt'
            source.write_text('Question one?\nQuestion one?\nQuestion two?\n')
            module.import_questions(root, source, 'Topic')
            self.assertEqual(len(module.load_queue(root)['questions']), 2)
            module.select_question(root)
            self.assertIn('Question one?', (root / 'PIPELINE.md').read_text())
            self.assertIn('Resume', module.select_question(root))
            module.import_questions(root, source, 'Topic')
            self.assertEqual(module.load_queue(root)['questions'][0]['state'], 'selected')
            with self.assertRaises(ValueError):
                module.complete_question(root)
            p = root / 'PIPELINE.md'
            p.write_text(p.read_text().replace('Current stage: pending', 'Current stage: PUBLISH'))
            module.complete_question(root)
            p.write_text(template)
            module.select_question(root)
            self.assertIn('Question two?', p.read_text())
            p.write_text(p.read_text().replace('Current stage: pending', 'Current stage: PUBLISH'))
            module.complete_question(root)
            p.write_text(template)
            self.assertIn('No unused', module.select_question(root))

    def test_existing_article_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'QUESTIONS.json').write_text('{"questions": []}')
            original = 'NEXT UP\n\n- Existing topic\n\nBRIEF\n\nExisting brief'
            (root / 'PIPELINE.md').write_text(original)
            self.assertIn('occupied', module.select_question(root))
            self.assertEqual((root / 'PIPELINE.md').read_text(), original)


if __name__ == '__main__':
    unittest.main()
