#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
证据 URL 结构闸门 —— 可复用参考实现

来源：2026-09-19 实测。渠道采集 Worker 产出的证据链接里出现 3 条结构不合法：
  - Upwork 线索填了 odesk.com（该平台 2015 年前的旧域名）的类目页
  - Upwork 线索填了 /hire/<品类> 分类页，冒充具体职位帖
  - Shopify 案例填了不存在的主机 enterprise.plus.shopify.com
危害：排名第 1 的线索因此被误判为「预算紧张」，差点放掉最好的客户。

用法：
    from evidence_gate import classify_evidence
    kind, ok_for_post, note = classify_evidence(url, channel)
    # ok_for_post: True 可支撑最高触达声明 / None 不强制 / False 必须降级
"""

import re
from urllib.parse import urlparse

# ---- 已废弃 / 历史域名：一旦命中，链接结构性失效 ----
LEGACY_HOSTS = {
    "odesk.com", "www.odesk.com",      # Upwork 2015 年前的旧域名
    "elance.com", "www.elance.com",    # 已并入 Upwork 的旧平台
}

# ---- 各平台「具体条目页」的路径格式 ----
# Upwork 职位帖：/freelance-jobs/apply/<slug>_~<数字ID>
UPWORK_JOB_RE = re.compile(r"^/freelance-jobs/apply/.+_~\d+")

# ---- 各渠道「官方一手域」正则 ----
# 关键设计：允许「单级前缀 + 区域 TLD」（shopify.co.nz / nz.shopify.com 是真实域名），
#           但挡掉多级前缀（enterprise.plus.shopify.com 是采集时拼错的）。
PLATFORM_HOST_RE = {
    "Upwork": re.compile(r"^(www\.)?upwork\.com$"),
    "Shopify": re.compile(
        r"^(?:(?:www|community|[a-z]{2})\.)?"
        r"shopify\.(?:com(?:\.[a-z]{2})?|co\.[a-z]{2}|[a-z]{2,3})$"),
    "Amazon": re.compile(
        r"^(?:(?:www|sellercentral[\w.-]*|sellercentral-europe)\.amazon\.[a-z.]{2,6}"
        r"|gs\.amazon\.cn|assets?\.aboutamazon\.com)$"),
}

# 不强制官方域的渠道：一手需求帖常由招聘站 / 行业媒体收录，
# 强制官方域会误伤真实可投递的线索。
NON_STRICT_CHANNELS = {"Fiverr", "TikTok Shop"}


def classify_evidence(url, channel):
    """判定一条 evidence_url 的结构合法性。

    返回 (kind, ok_for_job_post, note)：
      ok_for_job_post = True  结构合法，可支撑最高触达声明
      ok_for_job_post = False 结构不合法，必须降级触达路径
      ok_for_job_post = None  该渠道不适用（第三方来源，不强制降级）
    """
    p = urlparse(str(url))
    host = p.netloc.lower()

    if host in LEGACY_HOSTS:
        return ("DEAD_DOMAIN", False,
                "使用已废弃域名（odesk/elance），非该平台有效页面")
    if p.scheme != "https":
        return ("INSECURE", False, "证据链接非 https")

    if channel == "Upwork":
        if host == "www.upwork.com" and UPWORK_JOB_RE.match(p.path):
            return ("JOB_POST", True, "")
        if PLATFORM_HOST_RE["Upwork"].match(host):
            return ("CATEGORY_PAGE", False,
                    "Upwork 类目/招聘页，非具体职位帖")
        return ("HOST_MISMATCH", False,
                "非 Upwork 官方域名，无法支撑「回应职位帖」")

    if channel == "Shopify":
        if PLATFORM_HOST_RE["Shopify"].match(host):
            return ("OFFICIAL", True, "")
        return ("HOST_MISMATCH", False,
                "非 Shopify 官方域名（主机名可能拼写有误）")

    if channel == "Amazon":
        if PLATFORM_HOST_RE["Amazon"].match(host):
            return ("OFFICIAL", True, "")
        return ("THIRD_PARTY", None, "第三方来源，非 Amazon 官方域")

    if channel in NON_STRICT_CHANNELS:
        return ("THIRD_PARTY", None, "")

    return ("THIRD_PARTY", None, "")


def apply_gate(lead):
    """把闸门结果写回一条线索，并做必要的路径降级。

    三态处理的要点：**不要把 None 当成 False**。
    把"不确定"当"不成立"会误伤真实线索（实测过）。
    """
    kind, ok_for_post, note = classify_evidence(
        lead.get("evidence_url", ""), lead.get("channel", ""))
    lead["evidence_kind"] = kind

    if ok_for_post is True:
        lead["evidence_url_status"] = "OK"
    elif ok_for_post is None:
        lead["evidence_url_status"] = "THIRD_PARTY"
    else:
        lead["evidence_url_status"] = "FLAGGED"

    # 硬约束：最高触达声明必须持有结构合法的具体落地页
    downgraded = False
    if lead.get("acquisition_path") == "RESPOND_TO_JOB_POST" and ok_for_post is False:
        lead["acquisition_path"] = "LEADERBOARD_OBSERVABLE"
        lead["acquisition_path_downgraded"] = note or kind
        downgraded = True
    return lead, downgraded


if __name__ == "__main__":
    cases = [
        ("https://www.upwork.com/freelance-jobs/apply/Some-Job_~022074143552210628815", "Upwork"),
        ("http://www.odesk.com/freelance-jobs/ocr-tesseract", "Upwork"),
        ("https://www.upwork.com/hire/ai-receptionist-builders/", "Upwork"),
        ("https://www.shopify.co.nz/case-studies/maggy-london", "Shopify"),
        ("http://enterprise.plus.shopify.com/hk-en/case-studies/paul-and-joe", "Shopify"),
        ("https://www.onlinejobs.ph/jobseekers/job/xxx-1722698", "TikTok Shop"),
        ("https://sellercentral.amazon.it/seller-forums/discussions/t/xxx", "Amazon"),
    ]
    for u, ch in cases:
        k, ok, note = classify_evidence(u, ch)
        print("%-9s ok=%-5s %-14s %s" % (ch, str(ok), k, u[:70]))
