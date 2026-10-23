#!/usr/bin/env python3
"""检查中文成稿的硬禁令与常见模型化形状。只报警，不自动改文。"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HARD_STOPS = (
    "说白了",
    "说穿了",
    "先说结论",
)

HARD_JARGON = (
    "赋能",
    "抓手",
    "商业闭环",
    "价值闭环",
    "能力沉淀",
    "拉通",
    "底层逻辑",
    "顶层设计",
    "认知跃迁",
    "价值释放",
    "能力建设",
    "降本增效",
    "内容矩阵",
    "全链路",
    "组合拳",
    "打开想象空间",
    "结构性机会",
    "关键命题",
    "深层逻辑",
    "技术底座",
    "公共底座",
    "技术主权",
    "单点风险",
    "主脊柱",
    "材料锚点",
    "认知增量",
    "迭代闭环",
)

CONTEXT_JARGON = (
    "沉淀",
    "颗粒度",
    "对齐",
    "协同",
    "链路",
    "生态位",
    "心智",
    "范式",
    "方法论",
    "核心变量",
    "打法",
    "想象空间",
    "闭环",
    "不丢",
)

LYRIC_WORDS = (
    "安放",
    "抵达",
    "微光",
    "褶皱",
    "丰盈",
    "滚烫",
    "轻盈",
    "赤裸",
    "剥开",
)

ROAD_SIGNS = (
    "更微妙的是",
    "还有一层",
    "只说对了一半",
    "值得注意的是",
    "需要指出的是",
    "从某种意义上说",
)

ROAD_STRIP_CHARS = "。！？!? \n"

FORBIDDEN_PUNCTUATION = {
    "：": "中文冒号",
    ":": "英文冒号",
    "—": "破折号",
    "–": "连接号式破折号",
}

PIVOT_PATTERNS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,90}而是"),
    re.compile(r"并非[^。！？\n]{0,90}而是"),
    re.compile(r"不在于[^。！？\n]{0,90}而在于"),
    re.compile(r"与其说[^。！？\n]{0,90}(?:不如|毋宁|倒不如)"),
    re.compile(r"[。！？!?]\s*而是"),
    re.compile(r"表面(?:上)?[^。！？\n]{0,90}(?:其实|实际|实则)"),
    re.compile(r"看似[^。！？\n]{0,90}(?:其实|实际|实则)"),
)

SEMANTIC_PIVOT_PATTERNS = (
    re.compile(r"(?:总|一直|曾|都)?以为[^！？\n]{2,60}?(?:其实|才发现|才明白|才知道|后来才)"),
    re.compile(r"(?:总|都|一直)以为[^！？\n]{2,60}?[。，](?:可|但|其实)"),
    re.compile(r"回头(?:看|一看)?才(?:发现|明白|知道)"),
    re.compile(r"(?:并)?不是[^。！？\n]{1,40}，(?:更|才)?是[^，。！？\n]"),
    re.compile(r"从来(?:都)?(?:不是|与[^。！？，\n]{1,12}无关)"),
    re.compile(r"答案(?:是否定的|恰恰相反)|恰恰相反"),
    re.compile(r"表面(?:上)?[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"看似[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"[^，。！？\n]{1,12}不重要，(?:重要|要紧)的是"),
    re.compile(r"真正[^，。！？\n]{0,16}的(?:，)?是"),
    re.compile(r"不只(?:是)?[^。！？\n]{0,90}(?:还|也)"),
)

NOMINALIZATION_PATTERNS = (
    re.compile(r"进行(?:了|一次|一场|着)?[^。，！？\n]{0,10}(?:调整|优化|升级|分析|讨论|沟通|梳理|复盘|迭代|探索|尝试|思考|规划|布局)"),
    re.compile(r"实现了?[^。，！？\n]{0,14}的?[^。，！？\n]{0,6}(?:提升|增长|突破|转变|跃升|落地)"),
    re.compile(r"完成了?对[^。，！？\n]{0,16}的"),
    re.compile(r"起到了?[^。，！？\n]{0,12}的?作用"),
    re.compile(r"具有[^。，！？\n]{0,10}(?:意义|价值)"),
)

CONJUNCTIONS = (
    "因为",
    "所以",
    "但是",
    "然而",
    "同时",
    "此外",
    "而且",
    "并且",
    "因此",
    "不仅",
)

ROAD_SIGN_PATTERNS = (
    re.compile(
        rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[0])}[^。！？!?\n]{{0,24}}",
        re.MULTILINE,
    ),
    re.compile(
        rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[1])}(?=(?:更|原因|问题|意思|考虑|变化|逻辑|价值|作用|风险|影响|值得|很少|不容易|常被|往往))[^。！？!?\n]{{0,24}}",
        re.MULTILINE,
    ),
    *(
        re.compile(
            rf"(?:^|[。！？!?]\s*){re.escape(phrase)}[^。！？!?\n]{{0,24}}",
            re.MULTILINE,
        )
        for phrase in ROAD_SIGNS[2:]
    ),
)

SOFT_MARKERS = (
    "真正",
    "本质上",
    "更深层次",
    "归根结底",
    "换句话说",
    "不可否认",
    "核心是",
    "关键在于",
    "这意味着",
)

REPEATED_OPENERS = (
    "其实",
    "不过",
    "当然",
    "所以",
    "但是",
    "后来",
    "当时",
    "很多人",
    "问题是",
    "更重要的是",
    "说到这里",
)

LEFT_BRANCH_PATTERNS = (
    re.compile(r"(?:^|[。！？]\s*)在[^，。！？\n]{12,70}(?:以后|之后|之前|以前|过程中|情况下|背景下)，"),
    re.compile(r"(?:^|[。！？]\s*)那些[^，。！？\n]{10,60}的[^，。！？\n]{2,30}[，。]"),
    re.compile(r"(?:^|[。！？]\s*)(?:真正|最终|最后)让[^，。！？\n]{8,70}的，是"),
)

METAPHOR_FIELDS = {
    "温度": ("降温", "升温", "冷却", "余温", "温度最高"),
    "生死战争": ("杀死", "死因", "枪响", "开火", "战场", "引爆", "弹药"),
    "建筑灾害": ("坍塌", "崩塌", "地基", "砖头", "支柱", "废墟"),
    "仓储租赁": ("仓库", "库房", "租金", "取货", "入库", "库存"),
    "道路竞赛": ("赛道", "跑道", "岔路", "十字路口", "终点线", "门票"),
    "机器器官": ("齿轮", "引擎", "发动机", "血管", "骨架", "肌肉"),
    "海洋航行": ("蓝海", "浪潮", "潮水", "航船", "灯塔", "彼岸"),
}

# 中文序数小标题。本号惯用 `## 01 xxx` 阿拉伯数字编号，不在此列。
CHINESE_ORDINAL_HEADING = re.compile(
    r"^#{1,6}[ \t]*(?:第[一二三四五六七八九十]{1,3}|[一二三四五六七八九十]{1,3})"
    r"[、.．]?[ \t]*(?=\S)",
    re.MULTILINE,
)

# 一个分句里两个以上顿号，连起三项以上并列。
DUNHAO_RUN = re.compile(
    r"[^，,。！？!?；;：:\n]{1,60}(?:、[^，,。！？!?；;：:\n]{1,60}){2,}"
)

LIST_LINE = re.compile(r"^\s*(?:[-+*]|\d+[.、])\s")

# 段首评论语，省掉回指成分时读者要翻回上一段。
COMMENT_OPENER = re.compile(
    r"^(?:听起来|看起来|看上去|听上去|说白了|说到底|换句话说|意味着|值得注意|"
    r"不难看出|细看|再看|回过头看|问题在于|原因在于|结果是|有意思的是|"
    r"更重要的是|关键在于|真正的)"
)

# 回指成分，把上文接回来。
ANAPHOR = re.compile(
    r"^(?:这|那|其|此|上面|前面|刚才|以上|该|它|他|她|它们|他们|同样|类似|"
    r"相比|反过来|但|不过|所以|因此|于是|而|另|除此|与此)"
)

# 理想化职业人格的喻体。比喻本身不算 AI 味，只处理这一种。
PERSONIFIED_METAPHOR = re.compile(
    r"(?:像|如同|好比|仿佛|犹如|相当于|等于)[^，。！？\n]{0,8}(?:一位|一名|一个)"
    r"[^，。！？\n]{0,8}(?:导师|秘书|助手|顾问|管家|审查员|实习生|老师|教练|"
    r"向导|参谋|助理|专家|工程师|产品经理|合伙伙伴|朋友)"
)

PRAISE_MODIFIERS = (
    "智慧",
    "永不",
    "全能",
    "专业",
    "悉心",
    "尽职",
    "资深",
    "优秀",
    "贴心",
    "聪明",
    "勤奋",
    "忠诚",
    "周到",
    "体贴",
    "敬业",
    "勤劳",
)

# 概括说法盖掉了原文已有的具体数值。
ABSTRACT_BOOST = (
    "显著提升",
    "显著改善",
    "显著增强",
    "显著降低",
    "大幅增长",
    "大幅提升",
    "大幅下降",
    "大幅改善",
    "明显改善",
    "明显提升",
    "明显提高",
    "明显减少",
    "巨大提升",
    "极大提升",
)

# 翻译腔补充形态。
FRONTED_CLAUSE = re.compile(r"^当[^，。！？\n]{2,30}时[，,]")
FRONTED_SHELL = re.compile(
    r"^(?:对于[^，。！？\n]{2,15}来说|对[^，。！？\n]{2,15}而言|"
    r"就[^，。！？\n]{2,15}而言|关于[^，。！？\n]{2,15}[，,]|"
    r"在[^，。！？\n]{2,12}方面)"
)
LEAD_CONNECTORS = ("然而", "因此", "此外", "与此同时", "换言之", "总而言之")

# 公众号渲染约束
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
IMAGE_LINK = re.compile(r"!\[[^\]\n]*\]\(([^)\n]+)\)")
SEPARATOR_LINE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
FORMULA_MARK = re.compile(r"\$+")


@dataclass
class Paragraph:
    position: int
    text: str
    han: int
    sentences: int


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def excerpt(value: str, width: int = 72) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= width else value[: width - 1] + "…"


def mask_non_prose(text: str) -> str:
    """屏蔽代码、网址和机器元数据，同时保留字符位置与换行。"""

    def mask(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"!\[[^\]\n]*\]\([^)\n]*\)"),
        re.compile(r"\[[^\]\n]*\]\([^)\n]*\)"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"<[^>\n]+>"),
    )
    masked = text
    for pattern in patterns:
        masked = pattern.sub(mask, masked)
    return masked


def non_overlapping_terms(text: str, terms: tuple[str, ...]):
    matches = []
    occupied = []
    for term in sorted(terms, key=len, reverse=True):
        for match in re.finditer(re.escape(term), text):
            start, end = match.span()
            if any(start < old_end and end > old_start for old_start, old_end in occupied):
                continue
            matches.append((start, term))
            occupied.append((start, end))
    return sorted(matches)


def all_matches(text: str, patterns: tuple[re.Pattern[str], ...]):
    matches = []
    for pattern in patterns:
        matches.extend(pattern.finditer(text))
    return sorted(matches, key=lambda match: match.start())


def heavy_de_sentences(text: str):
    """找出主干可能被多个“的”压到后面的长句。"""

    matches = []
    pattern = re.compile(r"[^。！？!?\n]+(?:[。！？!?]|$)")
    for match in pattern.finditer(text):
        value = match.group()
        if han_count(value) >= 38 and value.count("的") >= 4:
            matches.append(match)
    return matches


def anaphora_runs(text: str, minimum: int = 3):
    """找出同一句里三个以上小句用同一个开头的排比。"""

    matches = []
    for sentence in re.finditer(r"[^。！？!?\n]+(?:[。！？!?]|$)", text):
        clauses = [
            clause.strip()
            for clause in re.split(r"[，、；,;]", sentence.group())
            if han_count(clause) >= 3
        ]
        if len(clauses) < minimum:
            continue
        run = 1
        for previous, current in zip(clauses, clauses[1:]):
            if previous[:2] == current[:2] and re.match(r"[一-鿿]{2}", current):
                run += 1
                if run >= minimum:
                    matches.append(sentence)
                    break
            else:
                run = 1
    return matches


def sentence_length_cv(text: str):
    """句长变异系数。人写的长短句差距大，模型的句长彼此接近。"""

    lengths = [
        han_count(match.group())
        for match in re.finditer(r"[^。！？!?\n]+[。！？!?]", text)
        if han_count(match.group()) >= 4
    ]
    if len(lengths) < 12:
        return None
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None
    variance = sum((value - mean) ** 2 for value in lengths) / len(lengths)
    return (variance ** 0.5) / mean, len(lengths)


def bracket_highlights(text: str):
    """「」括起来的短语。太密说明在批量造金句。"""

    return list(re.finditer(r"[「『][^」』\n]{1,6}[」』]", text))


def prose_paragraphs(text: str) -> list[Paragraph]:
    paragraphs = []
    cursor = 0
    for block in re.split(r"\n\s*\n", text):
        position = text.find(block, cursor)
        cursor = max(position + len(block), cursor)
        clean = re.sub(r"[>*_`]", "", block).strip()
        if not clean or clean.startswith(("#", "http", "![", "```")):
            continue
        if re.match(r"^(?:[-+*]|\d+[.、])\s", clean):
            continue
        count = han_count(clean)
        if count < 4:
            continue
        sentences = max(1, len(re.findall(r"[。！？!?]", clean)))
        paragraphs.append(Paragraph(position, clean, count, sentences))
    return paragraphs


def structure_signature(sentence: str) -> tuple[int, int]:
    """句子结构指纹：逗号数、长度档。指纹相同说明句法骨架相同。"""
    return (sentence.count("，") + sentence.count(","), len(sentence) // 12)


def isomorphic_runs(paragraph: str, minimum: int = 2):
    """段内连续几句结构指纹相同。"""
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[。！？!?]", paragraph)
        if han_count(sentence) >= 6
    ]
    runs = []
    for index in range(len(sentences) - minimum + 1):
        signatures = [
            structure_signature(sentence)
            for sentence in sentences[index : index + minimum]
        ]
        if all(signature == signatures[0] for signature in signatures):
            if signatures[0][0] >= 1:
                runs.append(sentences[index])
    return runs


def line_start(text: str, position: int) -> int:
    return text.rfind("\n", 0, position) + 1


def in_list_line(text: str, position: int) -> bool:
    return bool(LIST_LINE.match(text[line_start(text, position) :]))


def sentences_with_positions(text: str):
    """按句切分并保留每句的起始位置。"""
    for match in re.finditer(r"[^。！？!?\n]+[。！？!?]?", text):
        yield match.start(), match.group()


def mask_code_only(text: str) -> str:
    """只屏蔽 frontmatter、代码块和行内代码，保留 markdown 链接和 URL。"""

    def mask(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
    )
    masked = text
    for pattern in patterns:
        masked = pattern.sub(mask, masked)
    return masked


def frontmatter_end(text: str) -> int:
    """frontmatter 结束行号。开头那对 --- 不算分隔线。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index + 1
    return 0


def separator_lines(text: str):
    hits = []
    limit = frontmatter_end(text)
    for number, line in enumerate(text.split("\n"), start=1):
        if number <= limit:
            continue
        if SEPARATOR_LINE.match(line):
            hits.append(number)
    return hits


def long_paragraphs(text: str, limit: int = 4):
    """超过 limit 行的段落。代码块、表格、图片行、列表行不算。"""
    hits = []
    cursor = 0
    for block in re.split(r"\n\s*\n", text):
        position = text.find(block, cursor)
        cursor = max(position + len(block), cursor)
        content = block.strip()
        if not content or "```" in content:
            continue
        if content.startswith(("#", "|", ">", "![", "[!", "$$")):
            continue
        lines = [line for line in content.split("\n") if line.strip()]
        if len(lines) < limit:
            continue
        if all(LIST_LINE.match(line) for line in lines):
            continue
        hits.append(position)
    return hits


def overlong_sentences(text: str, limit: int = 40):
    hits = []
    for match in re.finditer(r"[^。！？!?\n]+[。！？!?]", text):
        count = han_count(match.group())
        if count > limit:
            hits.append((match.start(), count))
    return hits


def metaphor_cluster(text: str, distance: int = 800):
    hits = []
    for field, words in METAPHOR_FIELDS.items():
        for word in words:
            for match in re.finditer(re.escape(word), text):
                hits.append((match.start(), field, word))
    hits.sort()
    for index, (start, _, _) in enumerate(hits):
        window = [hit for hit in hits[index:] if hit[0] - start <= distance]
        fields = {hit[1] for hit in window}
        if len(fields) >= 3:
            return window, fields
    return None


def short_streak(paragraphs: list[Paragraph], limit: int = 4):
    streak = []
    for paragraph in paragraphs:
        if paragraph.han <= 24 and paragraph.sentences <= 1:
            streak.append(paragraph)
            if len(streak) >= limit:
                return streak
        else:
            streak = []
    return None


def opener_counts(paragraphs: list[Paragraph]):
    counts = collections.Counter()
    examples = {}
    for paragraph in paragraphs:
        value = paragraph.text.lstrip("“‘\"（(")
        for opener in REPEATED_OPENERS:
            if value.startswith(opener):
                counts[opener] += 1
                examples.setdefault(opener, paragraph.position)
                break
    return counts, examples


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="检查中文成稿的硬禁令与模型化形状")
    parser.add_argument("path", help="Markdown 或文本文件路径。使用 - 从标准输入读取")
    args = parser.parse_args()

    try:
        text = read_text(args.path)
    except (OSError, UnicodeError) as error:
        print(f"无法读取稿件。{error}", file=sys.stderr)
        return 2

    prose = mask_non_prose(text)
    total_han = han_count(prose)
    if total_han == 0:
        print("没有检测到汉字。", file=sys.stderr)
        return 2

    failures = []
    warnings = []

    quote_colons = []
    for symbol, label in FORBIDDEN_PUNCTUATION.items():
        matches = list(re.finditer(re.escape(symbol), prose))
        if symbol in ("：", ":"):
            hard = []
            for match in matches:
                tail = prose[match.end() : match.end() + 2].lstrip()
                if tail[:1] in ("「", "『", "“", "‘", '"'):
                    quote_colons.append(match)
                    continue
                rest = text[match.end() :].lstrip()
                if rest[:4].lower().startswith(("http", "www.", "ftp:")):
                    continue
                before = prose[max(0, match.start() - 2) : match.start()]
                after = prose[match.end() : match.end() + 2]
                if before.endswith(":") or after.startswith(":"):
                    continue
                hard.append(match)
            matches = hard
        if matches:
            lines = "、".join(str(line_number(text, match.start())) for match in matches[:8])
            failures.append(f"{label}共 {len(matches)} 处，出现在第 {lines} 行。")
    if quote_colons:
        lines = "、".join(
            str(line_number(text, match.start())) for match in quote_colons[:8]
        )
        warnings.append(
            f"引出原话的冒号 {len(quote_colons)} 处，第 {lines} 行。确认引号里确实是原话，且不是提示性用法。"
        )

    stop_matches = non_overlapping_terms(prose, HARD_STOPS)
    for position, phrase in stop_matches:
        failures.append(f"硬停词，第 {line_number(text, position)} 行，{phrase}")

    jargon_matches = non_overlapping_terms(prose, HARD_JARGON)
    for position, phrase in jargon_matches:
        failures.append(f"黑话，第 {line_number(text, position)} 行，{phrase}")

    context_jargon_matches = non_overlapping_terms(prose, CONTEXT_JARGON)
    hard_spans = [
        (position, position + len(phrase)) for position, phrase in jargon_matches
    ]
    context_jargon_matches = [
        (position, phrase)
        for position, phrase in context_jargon_matches
        if not any(
            position < end and position + len(phrase) > start
            for start, end in hard_spans
        )
    ]
    if context_jargon_matches:
        samples = "、".join(
            dict.fromkeys(phrase for _, phrase in context_jargon_matches)
        )
        lines = "、".join(
            dict.fromkeys(
                str(line_number(text, position))
                for position, _ in context_jargon_matches[:8]
            )
        )
        warnings.append(
            f"有 {len(context_jargon_matches)} 处词语需要结合语境判断。"
            f"第 {lines} 行出现 {samples}。本义准确时保留，用来抬价时改写。"
        )

    road_signs = all_matches(prose, ROAD_SIGN_PATTERNS)
    for match in road_signs:
        failures.append(
            f"模型路标，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group().lstrip(ROAD_STRIP_CHARS))}”"
        )

    pivots = all_matches(prose, PIVOT_PATTERNS)
    for match in pivots:
        failures.append(
            f"禁用翻案句，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group())}”"
        )

    occupied_spans = [match.span() for match in pivots]
    semantic_pivots = []
    for match in all_matches(prose, SEMANTIC_PIVOT_PATTERNS):
        if any(
            match.start() < end and match.end() > start
            for start, end in occupied_spans
        ):
            continue
        semantic_pivots.append(match)
        occupied_spans.append(match.span())
    for match in semantic_pivots:
        warnings.append(
            f"疑似翻案腔变形，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 44)}”。先立误解再推翻就改成正面陈述，正常用法保留。"
        )

    anaphoras = anaphora_runs(prose)
    for match in anaphoras[:4]:
        warnings.append(
            f"三连以上同构排比，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 44)}”。留两项，第三项换说法或删掉。"
        )

    lyric_matches = non_overlapping_terms(prose, LYRIC_WORDS)
    if len(lyric_matches) >= 2:
        samples = "、".join(dict.fromkeys(term for _, term in lyric_matches))
        warnings.append(
            f"模型偏爱的抒情词 {len(lyric_matches)} 处。{samples}。"
            "写具体事物时保留，给抽象概念穿衣服时删掉。"
        )

    nominalizations = all_matches(prose, NOMINALIZATION_PATTERNS)
    for match in nominalizations[:4]:
        warnings.append(
            f"名词化句式，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 36)}”。还原成直接的动词。"
        )

    conjunction_hits = non_overlapping_terms(prose, CONJUNCTIONS)
    if total_han >= 600 and len(conjunction_hits) * 1000 / total_han > 7:
        samples = "、".join(
            f"{term} {count} 次"
            for term, count in collections.Counter(
                term for _, term in conjunction_hits
            ).most_common(4)
        )
        warnings.append(
            f"连词密度偏高，每千字 {len(conjunction_hits) * 1000 // total_han} 个。{samples}。"
            "中文小句靠语序和事理相接，删掉一半试试。"
        )

    highlights = bracket_highlights(prose)
    highlight_limit = max(3, total_han // 700)
    if len(highlights) > highlight_limit:
        samples = "、".join(dict.fromkeys(match.group() for match in highlights[:6]))
        warnings.append(
            f"「」括起的短语共 {len(highlights)} 处。{samples}。太密说明在批量造金句。"
        )

    cv_result = sentence_length_cv(prose)
    if cv_result and cv_result[0] < 0.42:
        warnings.append(
            f"全文 {cv_result[1]} 个句子长度过于接近（变异系数 {cv_result[0]:.2f}）。"
            "人写的段落里十个字的句子会挨着四十个字的句子，放开几句，压短几句。"
        )

    marker_matches = non_overlapping_terms(prose, SOFT_MARKERS)
    marker_limit = max(2, total_han // 900)
    if len(marker_matches) > marker_limit:
        samples = "、".join(dict.fromkeys(term for _, term in marker_matches))
        warnings.append(
            f"洞察路标共 {len(marker_matches)} 处，当前提醒线为 {marker_limit} 处。"
            f"重点检查 {samples}。"
        )

    left_branches = all_matches(prose, LEFT_BRANCH_PATTERNS)
    left_limit = max(2, total_han // 1200)
    if len(left_branches) > left_limit:
        samples = "；".join(
            f"第 {line_number(text, match.start())} 行“{excerpt(match.group(), 44)}”"
            for match in left_branches[:4]
        )
        warnings.append(
            f"长前置成分共 {len(left_branches)} 处，可能让主干来得太晚。{samples}"
        )

    dense_de = heavy_de_sentences(prose)
    dense_de_limit = max(1, total_han // 1500)
    if len(dense_de) > dense_de_limit:
        samples = "；".join(
            f"第 {line_number(text, match.start())} 行“{excerpt(match.group(), 44)}”"
            for match in dense_de[:4]
        )
        warnings.append(
            f"有 {len(dense_de)} 个长句包含四个以上的“的”，可能要先交代人和动作。{samples}"
        )

    paragraphs = prose_paragraphs(prose)

    # 中文序数小标题
    ordinal_headings = list(CHINESE_ORDINAL_HEADING.finditer(text))
    if len(ordinal_headings) >= 3:
        lines = "、".join(
            str(line_number(text, match.start())) for match in ordinal_headings[:8]
        )
        failures.append(
            f"中文序数小标题共 {len(ordinal_headings)} 处，第 {lines} 行。"
            "删掉编号，保留标题原来的文字。"
        )

    # 顿号罗列
    dunhao_hits = []
    offset = 0
    for line in prose.split("\n"):
        if not LIST_LINE.match(line):
            for match in DUNHAO_RUN.finditer(line):
                dunhao_hits.append(offset + match.start())
        offset += len(line) + 1
    if dunhao_hits:
        lines = "、".join(
            str(line_number(text, position)) for position in dunhao_hits[:8]
        )
        warnings.append(
            f"顿号罗列共 {len(dunhao_hits)} 处，第 {lines} 行。"
            "一个分句里三个以上并列，改成概括，或改掉其中一项的句法。"
            "材料本身必须完整列出时保留。"
        )

    # 相邻句结构同款
    isomorphic_hits = []
    for paragraph in paragraphs:
        for sentence in isomorphic_runs(paragraph.text):
            position = text.find(sentence, paragraph.position)
            isomorphic_hits.append(position if position >= 0 else paragraph.position)
    if isomorphic_hits:
        lines = "、".join(
            str(line_number(text, position)) for position in isomorphic_hits[:4]
        )
        warnings.append(
            f"相邻句结构同款共 {len(isomorphic_hits)} 处，第 {lines} 行。"
            "打散其中一句的句法，换语序、拆句或改成短句。"
        )

    # 理想化职业人格的喻体
    personified = []
    for position, sentence in sentences_with_positions(prose):
        if in_list_line(prose, position):
            continue
        if PERSONIFIED_METAPHOR.search(sentence) and any(
            word in sentence for word in PRAISE_MODIFIERS
        ):
            personified.append(position)
    if personified:
        lines = "、".join(
            str(line_number(text, position)) for position in personified[:6]
        )
        failures.append(
            f"理想化职业人格的喻体共 {len(personified)} 处，第 {lines} 行。"
            "换成这东西实际做了什么。"
        )

    # 概括说法盖住具体数值
    abstract_with_data = []
    for paragraph in paragraphs:
        if re.search(r"\d", paragraph.text) and any(
            word in paragraph.text for word in ABSTRACT_BOOST
        ):
            abstract_with_data.append(paragraph.position)
    if abstract_with_data:
        lines = "、".join(
            str(line_number(text, position)) for position in abstract_with_data[:6]
        )
        warnings.append(
            f"概括说法盖住了具体数值，共 {len(abstract_with_data)} 处，第 {lines} 行。"
            "把原文已有的数字提到概括词的位置。"
        )

    # 段首零主语评论
    zero_subject = []
    for index, paragraph in enumerate(paragraphs):
        if index == 0:
            continue
        value = paragraph.text.lstrip("“‘\"（(")
        if COMMENT_OPENER.match(value) and not ANAPHOR.match(value):
            zero_subject.append(paragraph.position)
    if zero_subject:
        lines = "、".join(
            str(line_number(text, position)) for position in zero_subject[:6]
        )
        warnings.append(
            f"段首零主语评论共 {len(zero_subject)} 处，第 {lines} 行。"
            "补一个回指词，或点明评论对象。"
        )

    # 翻译腔补充形态
    fronted_clauses = []
    fronted_shells = []
    lead_connectors = []
    for position, sentence in sentences_with_positions(prose):
        if in_list_line(prose, position):
            continue
        value = sentence.lstrip()
        if FRONTED_CLAUSE.match(value):
            fronted_clauses.append(position)
        if FRONTED_SHELL.match(value):
            fronted_shells.append(position)
        if any(value.startswith(word) for word in LEAD_CONNECTORS):
            lead_connectors.append(position)
    for label, hits, advice in (
        (
            "“当……时”从句前置",
            fronted_clauses,
            "删掉“当”和“时”，让从句直接作前一分句。",
        ),
        (
            "前置话题壳",
            fronted_shells,
            "把对象放到主语位，删掉壳子。",
        ),
        (
            "句首连接词当路标",
            lead_connectors,
            "移到主语后面，或换成更口语的说法。",
        ),
    ):
        if hits:
            lines = "、".join(
                str(line_number(text, position)) for position in hits[:6]
            )
            warnings.append(f"{label}共 {len(hits)} 处，第 {lines} 行。{advice}")

    # 公众号渲染约束
    formula_marks = list(FORMULA_MARK.finditer(prose))
    if formula_marks:
        lines = "、".join(
            str(line_number(text, match.start())) for match in formula_marks[:8]
        )
        failures.append(
            f"公式源码共 {len(formula_marks)} 处，第 {lines} 行。"
            "改成大白话，或者截公式图当配图。"
        )

    without_code = mask_code_only(text)
    markdown_links = list(MARKDOWN_LINK.finditer(without_code))
    if markdown_links:
        lines = "、".join(
            str(line_number(text, match.start())) for match in markdown_links[:8]
        )
        failures.append(
            f"markdown 嵌入链接共 {len(markdown_links)} 处，第 {lines} 行。"
            "公众号点不了，写成裸 URL。"
        )

    separators = separator_lines(without_code)
    if separators:
        lines = "、".join(str(number) for number in separators[:8])
        failures.append(
            f"分隔线共 {len(separators)} 处，第 {lines} 行。删掉，用空段落分隔。"
        )

    local_images = []
    for match in IMAGE_LINK.finditer(without_code):
        url = match.group(1).strip()
        if not url.startswith(("http://", "https://")):
            local_images.append(match.start())
    if local_images:
        lines = "、".join(
            str(line_number(text, position)) for position in local_images[:8]
        )
        failures.append(
            f"本地图片路径共 {len(local_images)} 处，第 {lines} 行。传图床换云端 URL。"
        )

    long_blocks = long_paragraphs(text)
    if long_blocks:
        lines = "、".join(
            str(line_number(text, position)) for position in long_blocks[:6]
        )
        warnings.append(
            f"超过 4 行的段落共 {len(long_blocks)} 处，第 {lines} 行。按逻辑跳变点拆开。"
        )

    overlong = overlong_sentences(prose)
    if overlong:
        top = sorted(overlong, key=lambda item: item[1], reverse=True)[:3]
        details = "；".join(
            f"第 {line_number(text, position)} 行 {count} 字"
            for position, count in top
        )
        warnings.append(
            f"超过 40 字的句子共 {len(overlong)} 处，最长的几处：{details}。拆成短分句。"
        )

    if not 1400 <= total_han <= 2500:
        warnings.append(f"汉字数 {total_han}，不在 1400-2500 区间。")

    if len(paragraphs) >= 10:
        one_sentence = sum(paragraph.sentences <= 1 for paragraph in paragraphs)
        ratio = one_sentence / len(paragraphs)
        if ratio >= 0.75:
            warnings.append(
                f"可识别段落中有 {ratio:.0%} 只有一句话，可能形成统一的短段鼓点。"
            )

    two_sentence_breach = [p for p in paragraphs if p.sentences > 2]
    if two_sentence_breach:
        lines = "、".join(
            str(line_number(text, p.position)) for p in two_sentence_breach[:6]
        )
        warnings.append(
            f"超过两句的段落共 {len(two_sentence_breach)} 处，第 {lines} 行。第三句起换行分段。"
        )

    streak = short_streak(paragraphs)
    if streak:
        first = streak[0]
        warnings.append(
            f"从第 {line_number(text, first.position)} 行起连续出现 {len(streak)} 个短促单句段，"
            "检查是否在排队喊结论。"
        )

    counts, opener_examples = opener_counts(paragraphs)
    repeated = [(opener, count) for opener, count in counts.items() if count >= 4]
    if repeated:
        details = "、".join(f"{opener} {count} 次" for opener, count in repeated)
        first_position = min(opener_examples[opener] for opener, _ in repeated)
        warnings.append(
            f"段落开场重复，从第 {line_number(text, first_position)} 行附近开始。{details}。"
        )

    metaphors = metaphor_cluster(prose)
    if metaphors:
        window, fields = metaphors
        samples = "、".join(dict.fromkeys(hit[2] for hit in window))
        warnings.append(
            f"八百字内出现 {len(fields)} 套借喻。{'、'.join(sorted(fields))}。"
            f"例词有 {samples}。"
        )

    print(f"汉字数 {total_han}")
    print(
        f"翻案句 {len(pivots)}，翻案腔变形 {len(semantic_pivots)}，"
        f"同构排比 {len(anaphoras)}，同款相邻句 {len(isomorphic_hits)}，"
        f"名词化 {len(nominalizations)}，顿号罗列 {len(dunhao_hits)}，"
        f"黑话 {len(jargon_matches)}，硬停词 {len(stop_matches)}，"
        f"模型路标 {len(road_signs)}，需辨语境词 {len(context_jargon_matches)}，"
        f"抒情词 {len(lyric_matches)}，洞察路标 {len(marker_matches)}，"
        f"长前置成分 {len(left_branches)}，重定语句 {len(dense_de)}，"
        f"拟人喻体 {len(personified)}，序号小标题 {len(ordinal_headings)}，"
        f"概括盖数据 {len(abstract_with_data)}，零主语评论 {len(zero_subject)}，"
        f"前置从句 {len(fronted_clauses)}，话题壳 {len(fronted_shells)}，"
        f"句首连接词 {len(lead_connectors)}，公式 {len(formula_marks)}，"
        f"嵌入链接 {len(markdown_links)}，分隔线 {len(separators)}，"
        f"本地图 {len(local_images)}，长段 {len(long_blocks)}，超两句段 {len(two_sentence_breach)}，超长句 {len(overlong)}"
    )

    if failures:
        print("\n需要修改")
        for item in failures:
            print(f"- {item}")

    if warnings:
        print("\n需要人工判断")
        for item in warnings:
            print(f"- {item}")

    if not failures and not warnings:
        print("\n未发现这份检查器覆盖的问题。")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
