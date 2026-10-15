# -*- coding: utf-8 -*-
"""
honesty_gate.py — PHASE-3 诚实闸门（禁止虚构业绩 / 禁止付款 / 禁止敏感材料）

为什么存在：
  任务绝对规则 1/2/7/8 明确禁止虚构工作经历、客户、品牌合作、ROAS/CTR/CPA/收入，
  并要求"没有真实投放数据就明确写 Spec / portfolio project"。
  人写文案时会漏，所以把这条红线做成**代码级确定性闸门**：
  任何申请材料在提交前必须通过本脚本扫描；命中即 FAIL，不得提交。

用法：
  python honesty_gate.py                     # 扫描当前目录（及子目录）下所有 md/txt
  python honesty_gate.py <dir>               # 扫描指定目录
  python honesty_gate.py <file> [<file>...]  # 扫描指定文件
退出码：0 = 全部 PASS；1 = 存在 FAIL
"""
import os
import re
import sys

# 未传参数时扫描当前工作目录；传目录则扫描该目录，传文件则只扫文件
DEFAULT_SCAN_DIR = os.getcwd()

# ---------------------------------------------------------------- 虚构业绩红线
# 命中即 FAIL：不得出现在任何对外提交材料里（除非出现在"禁止词清单/自检"上下文）
FABRICATION_PATTERNS = {
    "ROAS 数字": r"\b\d+(?:\.\d+)?\s*[xX]?\s*ROAS\b|\bROAS\b\s*[:=]?\s*\d",
    "CTR 数字": r"\bCTR\b\s*[:=]?\s*\d|\b\d+(?:\.\d+)?\s*%\s*CTR\b",
    "CPA 数字": r"\bCPA\b\s*[:=]?\s*\$?\d|\bCPA\s+of\s+\$?\d",
    "收入/营收数字": r"\bgenerated\s+(?:over\s+)?\$?\d|\b\d+\s*(?:million|k|M)\s+in\s+(?:revenue|sales)\b",
    "规模化投放宣称": r"\bscaled\s+(?:ads|ad\s+spend|campaigns)\b|\bmanaged\s+\$?\d+[kKmM]?\s+in\s+ad\s+spend\b",
    "大牌合作宣称": r"\bworked\s+with\s+(?:major|leading|top|global)\s+brands?\b|\bmajor\s+brand\s+collaborations?\b",
    "客户数夸大": r"\b\d+\+?\s+(?:happy\s+)?clients\b|\btrusted\s+by\s+\d+",
    "效果保证": r"\bguaranteed?\s+(?:sales|results|conversions|revenue)\b|\bviral\s+guarantee\b",
}

# ---------------------------------------------------------------- 付款红线
PAYMENT_PATTERNS = {
    "要求付款": r"\b(?:pay|payment|fee|deposit|registration\s+fee|application\s+fee|verification\s+fee|bond|security\s+deposit)\b",
}

# ---------------------------------------------------------------- 敏感材料红线
SENSITIVE_PATTERNS = {
    "护照/身份证/银行卡/SSN": r"\b(?:passport\s+number|id\s+card\s+number|bank\s+card|credit\s+card\s+number|SSN|social\s+security)\b",
}

# ---------------------------------------------------------------- 允许的上下文（白名单）
# 出现在这些行里不算违规：自检清单、禁止词说明、规则引用
ALLOW_LINE_RE = re.compile(
    r"(禁止|不得|红线|自检|compliance|forbidden|do\s+not|never|no\s+fabricat|"
    r"without\s+evidence|spec\s+work|no\s+client\s+performance|not\s+claim|"
    r"honest\s+disclosure|disclosure|不合规|风险)",
    re.I,
)


# 显式忽略区：由 <!-- HONESTY-GATE-IGNORE:START --> / :END --> 包裹的区块，
# 或行尾带 `honesty-gate: ignore` 标记的行，一律不扫描。
# 用途：写"禁止词清单 / 合规自检"这类必须引用违禁词的内容。
IGNORE_INLINE_RE = re.compile(r"honesty-gate:\s*ignore", re.I)
IGNORE_BLOCK_START = "HONESTY-GATE-IGNORE:START"
IGNORE_BLOCK_END = "HONESTY-GATE-IGNORE:END"


def scan_text(name, text):
    hits = []
    in_ignore = False
    for i, line in enumerate(text.splitlines(), 1):
        if IGNORE_BLOCK_START in line:
            in_ignore = True
            continue
        if IGNORE_BLOCK_END in line:
            in_ignore = False
            continue
        if in_ignore:
            continue
        if not line.strip():
            continue
        if IGNORE_INLINE_RE.search(line):
            continue
        if ALLOW_LINE_RE.search(line):
            continue  # 白名单上下文
        for family, pats in (
            ("虚构业绩", FABRICATION_PATTERNS),
            ("付款", PAYMENT_PATTERNS),
            ("敏感材料", SENSITIVE_PATTERNS),
        ):
            for label, pat in pats.items():
                m = re.search(pat, line, re.I)
                if m:
                    hits.append((family, label, i, m.group(0), line.strip()[:160]))
    return hits


def main():
    args = sys.argv[1:]
    targets = []
    scan_dir = DEFAULT_SCAN_DIR
    for a in args:
        if os.path.isdir(a):
            scan_dir = a
        elif os.path.isfile(a):
            targets.append(a)
        else:
            print(f"!! 路径不存在，跳过: {a}")
    if not targets:
        for dp, _, fs in os.walk(scan_dir):
            if any(s in dp for s in (".git", "node_modules", "__pycache__")):
                continue
            for f in fs:
                if f.lower().endswith((".md", ".txt")):
                    targets.append(os.path.join(dp, f))
    targets = [t for t in targets if os.path.isfile(t)]

    print("=" * 78)
    print("诚实闸门 · honesty_gate")
    print("=" * 78)
    total_fail = 0
    for t in sorted(targets):
        rel = os.path.relpath(t, scan_dir) if t.startswith(scan_dir) else t
        try:
            text = open(t, encoding="utf-8").read()
        except UnicodeDecodeError:
            text = open(t, encoding="utf-8", errors="replace").read()
        hits = scan_text(rel, text)
        if hits:
            total_fail += 1
            print(f"\n!! FAIL  {rel}")
            for family, label, ln, frag, line in hits:
                print(f"     [{family}/{label}] line {ln}: ...{frag}...")
                print(f"        > {line}")
        else:
            print(f"   PASS  {rel}")

    print("\n" + "-" * 78)
    print(f"文件数: {len(targets)}   失败: {total_fail}")
    print("结论:", "PASS — 可提交" if total_fail == 0 else "FAIL — 禁止提交，先修文案")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
