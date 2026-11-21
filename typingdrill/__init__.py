"""typingdrill：离线英文打字练习生成器。"""

from .model import (
    BUILTIN_LESSONS,
    MAX_MINUTES,
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
from .render import render_drill

__all__ = [
    "BUILTIN_LESSONS",
    "MAX_MINUTES",
    "Lesson",
    "TypingError",
    "accuracy",
    "get_lesson",
    "lesson_names",
    "lesson_table",
    "normalize_text",
    "parse_text_file",
    "summarize",
    "validate_minutes",
    "validate_text",
    "wpm",
    "render_drill",
]

__version__ = "0.1.0"
