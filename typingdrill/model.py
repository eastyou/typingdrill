"""打字练习的文本模型、内置课程与统计公式。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

MAX_TEXT_LENGTH = 1200
MAX_MINUTES = 30
CHARS_PER_WORD = 5.0


class TypingError(ValueError):
    """练习文本或统计参数非法。"""


def _as_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypingError("%s 必须是数字" % name)
    return float(value)


def validate_text(text: str) -> str:
    """只允许可打印 ASCII 与换行，避免打字内容出现不可输入的字符。"""

    if not isinstance(text, str):
        raise TypingError("练习文本必须是字符串")
    if not text.strip():
        raise TypingError("练习文本不能为空")
    if len(text) > MAX_TEXT_LENGTH:
        raise TypingError("练习文本过长，最多 %d 个字符" % MAX_TEXT_LENGTH)
    for index, char in enumerate(text):
        if char == "\n":
            continue
        if not 32 <= ord(char) <= 126:
            raise TypingError("第 %d 个字符 %r 不可输入" % (index, char))
    return text


@dataclass(frozen=True)
class Lesson:
    name: str
    text: str
    description: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise TypingError("课程名称不能为空")
        if len(self.name) > 40:
            raise TypingError("课程名称过长")
        validate_text(self.text)

    @property
    def characters(self) -> int:
        return len(self.text)

    def preview(self, limit: int = 48) -> str:
        if limit < 1:
            raise TypingError("预览长度必须为正")
        flat = self.text.replace("\n", " ")
        return flat if len(flat) <= limit else flat[:limit].rstrip() + "…"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "characters": self.characters,
            "text": self.text,
        }


BUILTIN_LESSONS: Dict[str, Lesson] = {
    "home": Lesson(
        "home",
        "asdf jkl; asdf jkl;\n"
        "sad lad; fall dad; ask a lad;\n"
        "add all salads; a flask falls",
        "基准键：a s d f 与 j k l ;",
    ),
    "top": Lesson(
        "top",
        "qwer uiop qwer uiop\n"
        "quiet type; write your quote;\n"
        "require power; proper prior",
        "上排键：q w e r 与 u i o p",
    ),
    "bottom": Lesson(
        "bottom",
        "zxcv m,./ zxcv m,./\n"
        "maze cave; zoom in, calm down;\n"
        "mix corn; vex not",
        "下排键：z x c v 与 m , . /",
    ),
    "digits": Lesson(
        "digits",
        "12 34 56 78 90\n"
        "2026 314 159 265\n"
        "48 60 72 96; call 555 0134",
        "数字与空格",
    ),
    "sentences": Lesson(
        "sentences",
        "The quick brown fox jumps over the lazy dog.\n"
        "Pack my box with five dozen liquor jugs.\n"
        "Sphinx of black quartz, judge my vow.",
        "含大小写与标点的英文句子",
    ),
    "code": Lesson(
        "code",
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "for n in range(3):\n"
        "    print(add(n, 2))",
        "带缩进与符号的代码片段",
    ),
}


def lesson_names() -> List[str]:
    return list(BUILTIN_LESSONS.keys())


def get_lesson(name: str) -> Lesson:
    if not isinstance(name, str):
        raise TypingError("课程名称必须是字符串")
    key = name.strip().lower()
    if key not in BUILTIN_LESSONS:
        raise TypingError(
            "没有课程 %s，可选：%s" % (name, "、".join(lesson_names()))
        )
    return BUILTIN_LESSONS[key]


def normalize_text(text: str) -> str:
    """统一换行、去掉每行尾部空白与首尾空行。"""

    if not isinstance(text, str):
        raise TypingError("文本必须是字符串")
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    normalized = "\n".join(lines)
    return validate_text(normalized)


def parse_text_file(text: str) -> str:
    """解析自定义练习文本：# 开头为注释，空行忽略。"""

    if not isinstance(text, str):
        raise TypingError("文本必须是字符串")
    kept: List[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        kept.append(line)
    if not kept:
        raise TypingError("没有找到可用的练习文本")
    return validate_text("\n".join(kept))


def wpm(characters: int, seconds: float) -> float:
    """净速度：正确字符数 / 5 / 分钟。"""

    chars = _as_number(characters, "字符数")
    duration = _as_number(seconds, "秒数")
    if chars < 0:
        raise TypingError("字符数不能为负")
    if duration <= 0:
        raise TypingError("秒数必须为正")
    minutes = duration / 60.0
    return round((chars / CHARS_PER_WORD) / minutes, 1)


def accuracy(correct: int, total: int) -> float:
    """正确率，返回 0~100 的百分数。"""

    correct_value = _as_number(correct, "正确字符数")
    total_value = _as_number(total, "总字符数")
    if correct_value < 0 or total_value < 0:
        raise TypingError("字符数不能为负")
    if correct_value > total_value:
        raise TypingError("正确字符数不能超过总数")
    if total_value == 0:
        return 100.0
    return round(correct_value / total_value * 100.0, 1)


def summarize(characters: int, correct: int, seconds: float) -> Dict[str, float]:
    """汇总速度与正确率。"""

    return {
        "wpm": wpm(characters, seconds),
        "accuracy": accuracy(correct, characters),
        "seconds": round(_as_number(seconds, "秒数"), 1),
    }


def validate_minutes(minutes: int) -> int:
    if isinstance(minutes, bool) or not isinstance(minutes, int):
        raise TypingError("练习时长必须是整数分钟")
    if not 1 <= minutes <= MAX_MINUTES:
        raise TypingError("练习时长必须在 1~%d 分钟之间" % MAX_MINUTES)
    return minutes


def lesson_table() -> List[Tuple[str, str, int]]:
    """返回 (名称, 说明, 字符数) 列表，供命令行展示。"""

    return [
        (lesson.name, lesson.description, lesson.characters)
        for lesson in BUILTIN_LESSONS.values()
    ]
