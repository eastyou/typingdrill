"""命令行测试：课程列表、内置课程与自定义文本。"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from typingdrill.cli import main


class LessonsCommandTest(unittest.TestCase):
    def test_lists_all_lessons(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["lessons"])
        output = buffer.getvalue()
        self.assertEqual(code, 0)
        for name in ("home", "top", "bottom", "digits", "sentences", "code"):
            self.assertIn(name, output)


class BuildCommandTest(unittest.TestCase):
    def test_default_home_lesson(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out" / "drill.html"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["build", "-o", str(target)])
            self.assertEqual(code, 0)
            content = target.read_text(encoding="utf-8")
            self.assertIn("asdf jkl;", content)
            self.assertIn("已生成", buffer.getvalue())

    def test_named_lesson_and_minutes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "drill.html"
            main(["build", "--lesson", "digits", "--minutes", "5", "-o", str(target)])
            content = target.read_text(encoding="utf-8")
            self.assertIn("var DURATION = 300;", content)
            self.assertIn("555 0134", content)

    def test_custom_text_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "mytext.txt"
            source.write_text("# 注释\nhello world\nsecond line\n", encoding="utf-8")
            target = Path(tmp) / "drill.html"
            main(["build", "--text", str(source), "-o", str(target)])
            content = target.read_text(encoding="utf-8")
            self.assertIn('var TARGET = "hello world\\nsecond line";', content)

    def test_custom_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "drill.html"
            main(["build", "-o", str(target), "--title", "信息课练习"])
            self.assertIn("信息课练习", target.read_text(encoding="utf-8"))

    def test_missing_text_file(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["build", "--text", "/no/such/text.txt"])
        self.assertEqual(code, 2)
        self.assertIn("无法读取文本文件", error.getvalue())

    def test_unknown_lesson(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["build", "--lesson", "nope"])
        self.assertEqual(code, 2)
        self.assertIn("没有课程", error.getvalue())

    def test_bad_minutes(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["build", "--minutes", "0"])
        self.assertEqual(code, 2)

    def test_both_sources_is_parser_error(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["build", "--lesson", "home", "--text", "x.txt"])
        self.assertEqual(caught.exception.code, 2)


class ParserTest(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)

    def test_missing_command_exits(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                main([])


if __name__ == "__main__":
    unittest.main()
