#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代码级自动化天花板 —— 可复用参考实现

来源：2026-09-19 实测。用户红线是「不要自动发送消息」。
文档里写一句承诺是没用的，下一次重构就冲掉了。
做法：让状态机的最高状态在**语义上**等于"已对外发出消息"，
      然后要求推进到该状态必须显式声明是人工做的、并写清发生了什么。

效果：无人参与时，系统物理上不可能越过红线。
"""

STATUSES = ["NEW", "CONTACT_READY", "CONTACTED", "REPLIED",
            "NEGOTIATION", "WON", "LOST"]

# 只允许合法跃迁，禁止从 NEW 直接跳到 WON 这类"看起来很好"的伪造
TRANSITIONS = {
    "NEW": ["CONTACT_READY", "LOST"],
    "CONTACT_READY": ["CONTACTED", "LOST"],
    "CONTACTED": ["REPLIED", "LOST"],
    "REPLIED": ["NEGOTIATION", "LOST"],
    "NEGOTIATION": ["WON", "LOST"],
    "WON": [],
    "LOST": [],
}

# 自动化天花板：流水线自己最高只能推到这里
AUTOMATION_CEILING = "CONTACT_READY"

# 这些状态的语义是"已经发生了对外动作"，必须留下人工痕迹
HUMAN_REQUIRED = {"CONTACTED", "REPLIED", "NEGOTIATION", "WON"}


def check_advance(cur, to, note=None, human=False):
    """校验一次状态推进。返回 (ok, code, message)。

    code: 0 允许 / 1 非法跃迁 / 2 越过红线
    """
    if to not in STATUSES:
        return False, 1, "unknown status: %s" % to
    if to not in TRANSITIONS.get(cur, []):
        return False, 1, "illegal transition: %s -> %s (allowed: %s)" % (
            cur, to, TRANSITIONS.get(cur, []))

    # 红线一：碰"已发出消息"类状态，必须显式声明是人工做的
    if to in HUMAN_REQUIRED and not human:
        return False, 2, ("BLOCKED: advancing to %s means a message was sent. "
                          "This system never sends messages." % to)

    # 红线二：必须留下实况备注，否则状态是空壳
    if to in HUMAN_REQUIRED and not note:
        return False, 2, ('BLOCKED: status %s requires -n "<备注>" '
                          "recording what actually happened." % to)

    return True, 0, "ok"


if __name__ == "__main__":
    tests = [
        # (当前, 目标, note, human, 期望)
        ("CONTACT_READY", "CONTACTED", None, False, "拒绝-红线"),
        ("CONTACT_READY", "WON", None, False, "拒绝-非法跃迁"),
        ("CONTACT_READY", "CONTACTED", None, True, "拒绝-缺备注"),
        ("CONTACT_READY", "CONTACTED", "已在 X 平台投递提案（人工执行）", True, "允许"),
    ]
    for cur, to, note, human, expect in tests:
        ok, code, msg = check_advance(cur, to, note, human)
        print("[%-6s] %s -> %-14s human=%-5s => %s | %s"
              % (expect, cur, to, human, "PASS" if ok else "BLOCK", msg))
