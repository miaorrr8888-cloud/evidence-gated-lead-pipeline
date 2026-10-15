# 线索证据与状态闸门

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`evidence-gated-lead-pipeline` · 独立技能仓库 · MIT

适合：构建获客流水线、研究助手和数据整理工具的开发者

## 解决什么问题

避免类目页冒充具体职位、未知被写成已核实、准备联系被写成已联系。

## 快速开始

Python 3.10+，标准库。

在本仓库根目录运行：

```sh
python examples/check_evidence.py
```

## 输入与输出

**输入**：evidence_url、channel 和 acquisition_path；示例解释 True/False/None 三态。

**输出**：证据类别、结构检查状态、必要的路径降级；人工回执和业务验证需另外记录。

## 本次完善

原有缺口：URL 边界处理不足，调用方容易把 URL 结构检查当内容核验。

已补：畸形网址、嵌入凭据和异常端口会被拒绝；官方域名和职位路径更严格；结果明确写 URL_STRUCTURE_ONLY 和 content_verified=false。

## 当前限制

本地快照不证明实时网页和内容真实性；状态仅 READY_FOR_HUMAN_REVIEW，不自动升级为已核实或已联系。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)

## 第二轮：内容证据补充

新增本地快照内容检查，明确摘录是否存在、快照是否过期以及快照哈希，补上仅检查网址之后的证据步骤。

在仓库根目录运行：

```sh
python scripts/review_snapshot.py examples/snapshot.json
```

新增工具的输入字段见脚本参数与 examples/。快照示例采用固定日期，过期后正常返回 HOLD；需要检查新采集的页面时填写真实带时区的采集时间，不要改日期伪装新证据。
