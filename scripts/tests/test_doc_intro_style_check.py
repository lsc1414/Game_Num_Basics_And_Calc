import unittest

from scripts.check_doc_intro_style import (
    find_header_intro_violations,
    find_header_separator_violations,
)


class TestDocIntroStyleCheck(unittest.TestCase):
    def test_flags_bold_quote_after_summary(self) -> None:
        text = """---
title: "Demo"
---
> **摘要**：这是摘要。

---

> **"这是引言"**
>
> 正文
"""
        violations = find_header_intro_violations(text)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0][0], 8)

    def test_accepts_intro_label_after_summary(self) -> None:
        text = """---
title: "Demo"
---
> **摘要**：这是摘要。

---

> 引言：「这是引言」
>
> 正文
"""
        violations = find_header_intro_violations(text)
        self.assertEqual(violations, [])

    def test_ignores_bold_quote_without_summary(self) -> None:
        text = """---
title: "Demo"
---
> **"这是普通引用"**
"""
        violations = find_header_intro_violations(text)
        self.assertEqual(violations, [])

    def test_ignores_bold_quote_after_first_h2(self) -> None:
        text = """---
title: "Demo"
---
> **摘要**：这是摘要。

## 1. 标题

> **"这是正文引用，不是头部引言"**
"""
        violations = find_header_intro_violations(text)
        self.assertEqual(violations, [])

    def test_flags_header_separator_after_summary(self) -> None:
        text = """---
title: "Demo"
---
> **摘要**：这是摘要。

---

## 1. 标题
"""
        violations = find_header_separator_violations(text)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0][0], 6)

    def test_ignores_frontmatter_separators(self) -> None:
        text = """---
title: "Demo"
---
> **摘要**：这是摘要。
## 1. 标题
"""
        violations = find_header_separator_violations(text)
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
