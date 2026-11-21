"""模型层测试：文本校验、内置课程与统计公式。"""

from __future__ import annotations

import unittest

from typingdrill.model import (
    BUILTIN_LESSONS,
    Lesson,
    TypingError,
    accuracy,
    get_lesson,
    lesson_names,
    lesson_table,
    normalize_text,
    parse_text_file,
    summarize,
    validate_minutes,
    validate_text,
    wpm,
)


class LessonTest(unittest.TestCase):
    def test_builtin_lessons_are_valid(self) -> None:
        self.assertEqual(len(BUILTIN_LESSONS), 6)
        for lesson in BUILTIN_LESSONS.values():
            self.assertIsInstance(lesson, Lesson)
            self.assertGreater(lesson.characters, 0)

    def test_lesson_names_unique(self) -> None:
        self.assertEqual(len(set(lesson_names())), 6)

    def test_get_lesson_is_case_insensitive(self) -> None:
        self.assertEqual(get_lesson(" HOME ").name, "home")

    def test_get_unknown_lesson(self) -> None:
        with self.assertRaises(TypingError):
            get_lesson("nope")

    def test_get_lesson_non_string(self) -> None:
        with self.assertRaises(TypingError):
            get_lesson(None)  # type: ignore[arg-type]

    def test_empty_name(self) -> None:
        with self.assertRaises(TypingError):
            Lesson(" ", "abc")

    def test_long_name(self) -> None:
        with self.assertRaises(TypingError):
            Lesson("x" * 41, "abc")

    def test_empty_text(self) -> None:
        with self.assertRaises(TypingError):
            Lesson("x", "   ")

    def test_preview_replaces_newline(self) -> None:
        self.assertEqual(Lesson("x", "ab\ncd").preview(), "ab cd")

    def test_preview_truncates(self) -> None:
        preview = Lesson("x", "abcdefghijkl").preview(5)
        self.assertEqual(preview, "abcde…")

    def test_preview_bad_limit(self) -> None:
        with self.assertRaises(TypingError):
            Lesson("x", "abc").preview(0)

    def test_to_dict(self) -> None:
        data = Lesson("x", "abc", "说明").to_dict()
        self.assertEqual(data["characters"], 3)
        self.assertEqual(data["description"], "说明")

    def test_lesson_table(self) -> None:
        table = lesson_table()
        self.assertEqual(len(table), 6)
        self.assertTrue(all(len(row) == 3 for row in table))


class TextTest(unittest.TestCase):
    def test_accepts_printable_ascii(self) -> None:
        self.assertEqual(validate_text("abc 123 !?"), "abc 123 !?")

    def test_non_string(self) -> None:
        with self.assertRaises(TypingError):
            validate_text(None)  # type: ignore[arg-type]

    def test_empty(self) -> None:
        with self.assertRaises(TypingError):
            validate_text("\n\n")

    def test_rejects_tab(self) -> None:
        with self.assertRaises(TypingError):
            validate_text("a\tb")

    def test_rejects_chinese(self) -> None:
        with self.assertRaises(TypingError):
            validate_text("中文")

    def test_rejects_too_long(self) -> None:
        with self.assertRaises(TypingError):
            validate_text("a" * 1201)

    def test_normalize_crlf(self) -> None:
        self.assertEqual(normalize_text("a\r\nb\r\n"), "a\nb")

    def test_normalize_trailing_spaces(self) -> None:
        self.assertEqual(normalize_text("a   \nb  \n"), "a\nb")

    def test_normalize_blank_edges(self) -> None:
        self.assertEqual(normalize_text("\n\nabc\n\n"), "abc")

    def test_parse_comments(self) -> None:
        self.assertEqual(parse_text_file("# 注释\nabc\n\ndef\n"), "abc\ndef")

    def test_parse_empty(self) -> None:
        with self.assertRaises(TypingError):
            parse_text_file("# 只有注释\n")

    def test_parse_non_string(self) -> None:
        with self.assertRaises(TypingError):
            parse_text_file(5)  # type: ignore[arg-type]


class StatsTest(unittest.TestCase):
    def test_wpm(self) -> None:
        self.assertEqual(wpm(25, 60), 5.0)
        self.assertEqual(wpm(50, 60), 10.0)
        self.assertEqual(wpm(100, 30), 40.0)

    def test_zero_characters(self) -> None:
        self.assertEqual(wpm(0, 60), 0.0)

    def test_wpm_bad_seconds(self) -> None:
        with self.assertRaises(TypingError):
            wpm(10, 0)

    def test_wpm_negative(self) -> None:
        with self.assertRaises(TypingError):
            wpm(-1, 60)

    def test_wpm_bool(self) -> None:
        with self.assertRaises(TypingError):
            wpm(True, 60)  # type: ignore[arg-type]

    def test_accuracy(self) -> None:
        self.assertEqual(accuracy(9, 10), 90.0)
        self.assertEqual(accuracy(10, 10), 100.0)

    def test_accuracy_zero_total(self) -> None:
        self.assertEqual(accuracy(0, 0), 100.0)

    def test_accuracy_above_total(self) -> None:
        with self.assertRaises(TypingError):
            accuracy(11, 10)

    def test_accuracy_negative(self) -> None:
        with self.assertRaises(TypingError):
            accuracy(-1, 10)

    def test_summarize(self) -> None:
        result = summarize(25, 20, 60)
        self.assertEqual(result["wpm"], 5.0)
        self.assertEqual(result["accuracy"], 80.0)
        self.assertEqual(result["seconds"], 60.0)

    def test_validate_minutes(self) -> None:
        self.assertEqual(validate_minutes(1), 1)
        self.assertEqual(validate_minutes(30), 30)
        for value in (0, 31):
            with self.assertRaises(TypingError):
                validate_minutes(value)

    def test_validate_minutes_rejects_bool(self) -> None:
        with self.assertRaises(TypingError):
            validate_minutes(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
