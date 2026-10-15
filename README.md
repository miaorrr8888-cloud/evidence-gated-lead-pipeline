# 线索证据与状态闸门

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

## 仍然缺什么

不访问网页，不验证实际职位、预算或真实性；文本规则可能误报。状态检查函数只有被调用方接入才会生效，不是不可绕过的安全机制。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)
