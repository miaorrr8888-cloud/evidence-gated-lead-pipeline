---
name: evidence-gated-lead-pipeline
description: 对线索证据 URL、材料文案和状态推进做离线检查，区分未知、结构无效与已核实。
license: MIT
---

# 线索证据闸门

`references/evidence_gate.py` 提供 `classify_evidence(url, channel)` 与 `apply_gate(lead)`。其结果只说明 URL 结构是否符合内置规则；页面存在、内容匹配、项目开放与联系权限仍需现场核验。规则可能随平台变化。

保留 True / False / None 三态：None 不是 False，更不是已核实。降级或修正后的记录才应进入下游，并保留修改理由和原始证据。

`references/honesty_gate.py` 可扫描指定文件或目录里的虚构业绩、付款与敏感材料词汇。它是可漏报或误报的文本启发式；不能替代逐项核验事实。不要用忽略标记掩盖真实问题。

`references/automation_ceiling.py` 提供 `check_advance` 示例，要求对表示已发生外部动作的状态记录人工标记与备注。这是调用方需要采用的校验函数，不会约束绕过它的程序，也不验证备注真实性。

没有发送回执就不标已联系，没有订单证据就不标成交。线索整理本身不授权发送消息。

## 上手示例与当前限制

先读 [README.md](README.md) 的快速开始、输入输出和未完成项；可运行例子在 examples/，本次修订见 CHANGELOG.md。不要把合成演示或离线检查当成真实平台验证。

## 扩展能力

新增本地快照内容检查，明确摘录是否存在、快照是否过期以及快照哈希，补上仅检查网址之后的证据步骤。 使用前阅读 [README.md](README.md) 的“第二轮”命令和当前限制。不要把本地检查、人工声明或模拟响应解释为实时平台验证。
