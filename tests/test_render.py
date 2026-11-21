"""渲染层测试：单文件页面、文本嵌入与安全转义。"""

from __future__ import annotations

import unittest

from typingdrill.model import Lesson, get_lesson
from typingdrill.render import render_drill


class DrillTest(unittest.TestCase):
    def test_contains_core_ui(self) -> None:
        html = render_drill(get_lesson("home"), minutes=3)
        self.assertIn("<textarea", html)
        self.assertIn("重新开始", html)
        self.assertIn("WPM", html)
        self.assertIn("限时 3 分钟", html)
        self.assertIn("100%", html)

    def test_title_and_lesson_meta(self) -> None:
        lesson = Lesson("demo", "abc", "示例课程")
        html = render_drill(lesson, title="打字小测")
        self.assertIn("打字小测", html)
        self.assertIn("demo", html)
        self.assertIn("示例课程", html)
        self.assertIn("共 3 个字符", html)

    def test_target_embedded(self) -> None:
        html = render_drill(Lesson("demo", "abc"))
        self.assertIn('var TARGET = "abc";', html)

    def test_newline_escaped_in_json(self) -> None:
        html = render_drill(Lesson("demo", "a\nb"))
        self.assertIn('"a\\nb"', html)

    def test_script_breakout_is_escaped(self) -> None:
        html = render_drill(Lesson("demo", "a</script><b>b"))
        self.assertEqual(html.count("</script>"), 1)
        self.assertIn("<\\/script>", html)

    def test_no_external_resources(self) -> None:
        html = render_drill(get_lesson("code"))
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn("<link", html)
        self.assertNotIn("src=", html)

    def test_minutes_affect_duration(self) -> None:
        html = render_drill(get_lesson("home"), minutes=5)
        self.assertIn("var DURATION = 300;", html)
        self.assertIn("限时 5 分钟", html)

    def test_minutes_out_of_range(self) -> None:
        for minutes in (0, 31):
            with self.assertRaises(ValueError):
                render_drill(get_lesson("home"), minutes=minutes)

    def test_wrong_lesson_type(self) -> None:
        with self.assertRaises(ValueError):
            render_drill("home")  # type: ignore[arg-type]

    def test_different_lessons_differ(self) -> None:
        first = render_drill(get_lesson("home"))
        second = render_drill(get_lesson("digits"))
        self.assertNotEqual(first, second)

    def test_single_script_tag(self) -> None:
        html = render_drill(get_lesson("sentences"))
        self.assertEqual(html.count("<script>"), 1)


if __name__ == "__main__":
    unittest.main()
