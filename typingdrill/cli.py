"""命令行入口：列出课程或生成离线打字练习页。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import (
    Lesson,
    TypingError,
    get_lesson,
    lesson_table,
    parse_text_file,
    validate_minutes,
)
from .render import render_drill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="typingdrill",
        description="英文打字练习：生成单文件、可离线运行的 HTML 练习页。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="生成练习页")
    source = build.add_mutually_exclusive_group()
    source.add_argument("--lesson", help="内置课程名称，默认 home")
    source.add_argument("--text", help="自定义文本文件，每行一段，# 开头为注释")
    build.add_argument("-o", "--output", default="typing-drill.html")
    build.add_argument("--minutes", type=int, default=3, help="限时分钟数，默认 3")
    build.add_argument("--title", default="英文打字练习")

    sub.add_parser("lessons", help="列出内置课程")
    return parser


def _read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise TypingError("无法读取文本文件：%s" % exc)
    except UnicodeDecodeError as exc:
        raise TypingError("文件编码不是 UTF-8：%s" % exc)


def _write(path: str, content: str) -> int:
    try:
        target = Path(path)
        if target.parent and not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except OSError as exc:
        print("写入失败：%s" % exc, file=sys.stderr)
        return 1
    print("已生成 %s" % path)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "lessons":
            print("%-10s %-30s %s" % ("名称", "说明", "字符数"))
            for name, description, characters in lesson_table():
                print("%-10s %-30s %d" % (name, description, characters))
            return 0

        if args.command == "build":
            validate_minutes(args.minutes)
            if args.text:
                text = parse_text_file(_read_text(args.text))
                lesson = Lesson(name=Path(args.text).stem or "custom", text=text)
            else:
                lesson = get_lesson(args.lesson or "home")
            content = render_drill(lesson, minutes=args.minutes, title=args.title)
            return _write(args.output, content)
    except TypingError as exc:
        print("参数错误：%s" % exc, file=sys.stderr)
        return 2

    print("未知命令", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
