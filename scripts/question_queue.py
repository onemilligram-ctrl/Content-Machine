"""Import supplied questions and reserve the next unused one for PIPELINE.md."""
import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_queue(root):
    return json.loads((root / 'QUESTIONS.json').read_text())


def save_queue(root, queue):
    path = root / 'QUESTIONS.json'
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def import_questions(root, source, topic):
    if source.suffix.lower() == '.csv':
        with source.open(newline='', encoding='utf-8-sig') as handle:
            rows = list(csv.DictReader(handle))
        if not rows or 'question' not in rows[0]:
            raise ValueError('CSV needs a question column and at least one row.')
        questions = [row['question'] for row in rows]
    else:
        questions = source.read_text(encoding='utf-8-sig').splitlines()
    queue = load_queue(root)
    known = {item['id'] for item in queue['questions']}
    added = 0
    for question in questions:
        question = re.sub(r'^\s*(?:[-*] |\d+[.)] )', '', question).strip()
        if not question:
            continue
        key = hashlib.sha256((topic.strip().casefold() + '\n' + ' '.join(question.casefold().split())).encode()).hexdigest()[:16]
        if key in known:
            continue
        queue['questions'].append({'id': key, 'topic': topic.strip(), 'question': question, 'state': 'unused', 'selected_at': None})
        known.add(key)
        added += 1
    save_queue(root, queue)
    return f'Imported {added} new questions. Existing usage preserved.'


def select_question(root):
    queue = load_queue(root)
    path = root / 'PIPELINE.md'
    pipeline = path.read_text()
    match = re.search(r'(?m)^(?:#{1,6} )?NEXT UP\n\n(.*?)\n\n(?:#{1,6} )?BRIEF$', pipeline, re.S)
    if not match:
        raise ValueError('Unexpected PIPELINE.md structure; no files changed.')
    # Recover an interrupted selection without consuming another question.
    reserved = next((item for item in queue['questions'] if item['state'] == 'selected'), None)
    if reserved:
        marker = f"Question ID: {reserved['id']}"
        if marker in pipeline:
            return 'Resume the selected question already in PIPELINE.md; no new selection.'
        if match.group(1).strip() != '- topic goes here':
            return 'Pipeline is occupied; resolve the reserved question before selecting another.'
        chosen = reserved
    else:
        if match.group(1).strip() != '- topic goes here':
            return 'Pipeline is occupied; finish and archive it before selecting another question.'
        chosen = next((item for item in queue['questions'] if item['state'] == 'unused'), None)
        if chosen is None:
            return 'No unused questions remain. Supply more questions; none were recycled.'
        chosen['state'] = 'selected'
        chosen['selected_at'] = datetime.now(timezone.utc).isoformat()
        save_queue(root, queue)
    replacement = f"- {chosen['question']}\n\nTopic: {chosen['topic']}\nQuestion ID: {chosen['id']}"
    updated = pipeline[:match.start(1)] + replacement + pipeline[match.end(1):]
    temporary = path.with_suffix('.md.tmp')
    temporary.write_text(updated)
    temporary.replace(path)
    return f"Selected question {chosen['id']} for NEXT UP."


def complete_question(root):
    pipeline = (root / 'PIPELINE.md').read_text()
    if 'Current stage: PUBLISH' not in pipeline:
        raise ValueError('Only complete a question after the publishing package is PUBLISH.')
    queue = load_queue(root)
    item = next((item for item in queue['questions'] if item['state'] == 'selected' and f"Question ID: {item['id']}" in pipeline), None)
    if not item:
        raise ValueError('No matching selected question found.')
    item['state'] = 'used'
    save_queue(root, queue)
    return 'Question marked used. Archive and reset the pipeline before the next selection.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    importer = commands.add_parser('import')
    importer.add_argument('file', type=Path)
    importer.add_argument('--topic', required=True)
    commands.add_parser('select')
    commands.add_parser('complete')
    args = parser.parse_args()
    # Serialize operations in this checkout. Separate checkouts need sequential Git handoffs.
    lock = ROOT / '.question-queue.lock'
    owned = False
    try:
        with lock.open('x'):
            owned = True
            if args.command == 'import':
                if not args.topic.strip():
                    raise ValueError('Topic must not be empty.')
                print(import_questions(ROOT, args.file, args.topic))
            elif args.command == 'select':
                print(select_question(ROOT))
            else:
                print(complete_question(ROOT))
    except FileExistsError:
        raise SystemExit('Another queue operation is running. If interrupted, inspect state before removing the stale lock.')
    finally:
        if owned:
            lock.unlink()


if __name__ == '__main__':
    main()
