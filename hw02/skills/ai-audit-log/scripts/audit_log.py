"""Local, append-only AI interaction logger. Python 3 standard library only."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import uuid


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds")


def read_text(path):
    # Preserve original line endings; accept a UTF-8 BOM without storing it.
    with open(path, encoding="utf-8-sig", newline="") as stream:
        return stream.read()


@contextmanager
def writer_lock(folder):
    lock = folder / ".write.lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        yield
    finally:
        os.close(descriptor)
        lock.unlink()


def load_entries(source):
    entries = {}
    if source.exists():
        for line in source.read_text(encoding="utf-8").split("\n"):
            if not line:
                continue
            event = json.loads(line)
            if event["event"] == "begin":
                if event["id"] in entries:
                    raise ValueError("Duplicate begin event in source log")
                entries[event["id"]] = dict(event, status="pending")
            elif event["event"] == "finish":
                entry = entries[event["id"]]
                if entry["status"] == "completed":
                    raise ValueError("Duplicate finish event in source log")
                entry.update(response=event["response"], completed_at=event["completed_at"], status="completed")
            else:
                raise ValueError("Unknown source event")
    return entries


def append_event(source, event):
    with source.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def block(text):
    longest = max((len(match) for match in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}\n"


def render(folder, entries):
    parts = ["# AI Audit Log\n\n",
             "Times are capture/completion times in UTC+07:00, not original sent times.\n\n",
             "Prompts and final answers are stored verbatim. Progress commentary, tool traffic, "
             "and hidden reasoning are outside this log. Pending means no final answer was recorded.\n\n"]
    for index, entry in enumerate(entries.values(), 1):
        parts.append(f"## Interaction {index:04d}\n\n")
        for label, key in [("ID", "id"), ("AI tool", "tool"), ("Session", "session"),
                           ("Captured at", "captured_at"), ("Status", "status"),
                           ("Completed at", "completed_at"), ("Note", "note")]:
            if entry.get(key):
                parts.append(f"- {label}: {json.dumps(entry[key], ensure_ascii=False)}\n")
        parts.append("\n### User prompt\n\n" + block(entry["prompt"]))
        parts.append("\n### AI output\n\n")
        parts.append(block(entry["response"]) if entry["status"] == "completed"
                     else "No final answer recorded yet.\n")
        parts.append("\n")
    report = folder / "AI_Audit_Log.md"
    descriptor, temp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("".join(parts))
        os.replace(temp_path, report)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    begin = commands.add_parser("begin")
    begin.add_argument("--prompt-file", required=True, type=Path)
    begin.add_argument("--tool", required=True)
    begin.add_argument("--session", required=True)
    begin.add_argument("--id", default=None)
    begin.add_argument("--note", default="")
    finish = commands.add_parser("finish")
    finish.add_argument("--id", required=True)
    finish.add_argument("--response-file", required=True, type=Path)
    commands.add_parser("render")
    args = parser.parse_args()
    if not args.workspace.is_absolute() or not args.workspace.is_dir():
        parser.error("--workspace must be an existing absolute directory")
    folder = args.workspace / "ai-audit"
    folder.mkdir(exist_ok=True)
    source = folder / "interactions.jsonl"
    with writer_lock(folder):
        entries = load_entries(source)
        entry_id = getattr(args, "id", None)
        if args.command == "begin":
            entry_id = entry_id or str(uuid.uuid4())
            content = dict(prompt=read_text(args.prompt_file), tool=args.tool,
                           session=args.session, note=args.note)
            if entry_id in entries:
                if any(entries[entry_id].get(key) != value for key, value in content.items()):
                    raise ValueError("ID already exists with different content")
            else:
                append_event(source, dict(event="begin", id=entry_id, captured_at=now(), **content))
        elif args.command == "finish":
            if entry_id not in entries:
                raise ValueError("Unknown interaction ID")
            response = read_text(args.response_file)
            if entries[entry_id]["status"] == "completed":
                if entries[entry_id]["response"] != response:
                    raise ValueError("Completed response differs; existing evidence was preserved")
            else:
                append_event(source, dict(event="finish", id=entry_id, completed_at=now(), response=response))
        report = render(folder, load_entries(source))
    print(json.dumps(dict(ok=True, id=entry_id, report=str(report)), ensure_ascii=False))


if __name__ == "__main__":
    main()
