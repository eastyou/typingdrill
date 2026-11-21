# typingdrill

[![CI](https://github.com/eastyou/typingdrill/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/typingdrill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

离线英文打字练习生成器：内置基准键、上排键、下排键、数字、句子与代码六套课程，也能读取自定义文本，输出单文件 HTML，双击即可练习。纯标准库、零依赖、不联网。

## 安装

```bash
pip install -e .
```

## 用法

```bash
# 查看内置课程
typingdrill lessons

# 生成 3 分钟基准键练习
typingdrill build -o 打字练习.html

# 指定课程与限时
typingdrill build --lesson digits --minutes 5 -o 数字练习.html

# 用自己的文本（每行一段，# 开头为注释）
typingdrill build --text examples/custom.txt --minutes 3 -o 自定义.html
```

打开生成的 HTML 后，点击文本区即可开始输入：
- 逐字符高亮：绿色正确、红色错误、黄色下划线为当前字符。
- 实时显示 WPM（净速度）、正确率、进度与剩余时间。
- 时间到或打完自动结算，可「重新开始」。

## 速度与正确率

- 速度按净 WPM 计算：`正确字符数 ÷ 5 ÷ 分钟数`。
- 正确率：`正确字符数 ÷ 已输入字符数`，未输入时为 100%。
- 同一套公式在命令行模块中提供，可用于批改或二次统计。

## 项目结构

```text
typingdrill/
├── typingdrill/
│   ├── __init__.py
│   ├── __main__.py
│   ├── model.py      # 课程、文本校验与统计公式
│   ├── render.py     # 单文件 HTML 与内嵌 JS
│   └── cli.py        # 命令行入口
├── examples/
│   ├── custom.txt
│   └── sample.html
└── tests/
    ├── test_model.py
    ├── test_render.py
    └── test_cli.py
```

## 测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © 2026 eastyou
