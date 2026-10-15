# evidence-gated-lead-pipeline

> Packaged by the WorkBuddy History Audit (2026-10-14). Source copied verbatim from the
> original location; **no modifications made to the original project**.

## 功能介绍
构建「自动采集线索 / 商机 / 客户名单」类流水线时使用，用确定性证据闸门与代码级自动化天花板，防止采集 Worker 产出的假证据、假触达路径与未经授权的对外动作流入下游。适用于多 Agent 的线索发现、BD 名单、竞品情报、市场信号采集等场景。触发词：线索库、客户名单、BD 名单、市场雷达、lead pipeline、证据核验、证据闸门。

## 起源与许可
- 类型: 用户原创 Skill (agent_created)
- 许可: MIT (见 LICENSE)
- 是否含密钥/Token: 否 (已通过审计扫描)

## 目录内容
- `SKILL.md` / `README.md` — 技能定义与使用说明
- 脚本与测试 — 见各子目录
- `LICENSE` — MIT

## 发布前检查清单
- [x] 无硬编码密钥 / Cookie / Token
- [x] 依赖清楚 (stdlib-only 或显式声明)
- [x] 含使用说明
- [ ] 作者补充中文/英文双语 README
- [ ] 补充 CI 测试 (如适用)

## 独立仓库

本仓库只包含 evidence-gated-lead-pipeline 一个技能。
源码目录、SKILL.md、许可和相关测试均可独立取得，不依赖其他技能仓库。
工作记录与其他技能入口：[agent-skills-worklog](https://github.com/miaorrr8888-cloud/agent-skills-worklog)。

离线验证：`python -m unittest discover -s tests -v`。
