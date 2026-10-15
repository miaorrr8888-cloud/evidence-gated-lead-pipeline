# AI线索的证据与状态核对：用户使用指南

## 它能帮你做什么

检查网址结构与部分证据规则；核对原文摘录是否出现在本地快照，保留来源、时效和未验证状态。

## 适合谁

为AI研究、获客或资料整理流程做质量检查的人，进阶接入更适合开发者。

## 具体解决什么问题

类目页被当成具体机会，原文未核对就写成已验证，准备联系被写成已联系。

**不适合这些目标：**独立确认真实需求、自动联系客户、保证所有状态转换不可绕过或替代实时网页核验。

## 下载与准备

- [打开独立仓库](https://github.com/miaorrr8888-cloud/evidence-gated-lead-pipeline)
- [直接下载源码ZIP](https://github.com/miaorrr8888-cloud/evidence-gated-lead-pipeline/archive/refs/heads/main.zip)

也可在仓库页面点 Code → Download ZIP。解压后打开包含 SKILL.md、README.md、USER_GUIDE.md 的那层文件夹。不要停在外层目录或只复制一个脚本。

建议使用Windows电脑和Python 3.12；这是本次验证环境。先在该文件夹打开PowerShell，再执行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

这里直接使用虚拟环境里的Python，不需要运行激活脚本或修改系统执行策略。安装步骤及其他系统说明见[通用安装说明](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/INSTALLATION.md)。

本指南的基础示例只用Python标准库，无需安装第三方Python包。

## 第一次使用：先跑自带示例

对比一个类目页和一个职位样式网址，再检查本地原文快照是否有摘录；结构通过也不升级为内容已核实。

```powershell
.\.venv\Scripts\python.exe examples/check_evidence.py
.\.venv\Scripts\python.exe scripts/review_snapshot.py examples/snapshot.json
```

## 结果怎么看

第一条打印合成网址的结构判断与降级信息；第二条打印 quote_found、fresh_within_24h、scope=LOCAL_SNAPSHOT_ONLY。日期过期则HOLD，live_page_verified始终为false。

## 换成自己的资料

网址、渠道、取得路径；快照记录写 snapshot、source_url、quote、带时区 captured_at，快照文件放在记录所在目录内。

自己取得有权保存的页面内容后，写下实际采集时间和准确摘录，检查结果。接入其他程序时，需要由调用方真正调用这些检查函数。

## 不想手动敲命令：给AI助手的任务

以下任务适用于能读取所选目录、执行本地命令的助手。WorkBuddy需要先确认当前版本的权限与技能启用状态；本项目未完成WorkBuddy实际导入验收。

```text
请先读取我选定文件夹中的 SKILL.md 和 USER_GUIDE.md，只在该项目范围内处理。
运行合成网址和快照示例，逐项解释结构检查、摘录存在、时效和实时内容核验有什么不同。不要把结构通过写成职位或预算已证实，也不要改写为已联系客户。
缺少依赖时先说明用途，优先放进本项目虚拟环境；不要读取其他目录中的密码、密钥或浏览器登录数据。
```

## 常见问题

**quote_found=true为什么还不算已核实**

只证明本地文件中有这段文字，不能证明网页来源或购买意图。

**自带快照返回HOLD**

示例使用固定采集日期，过期会正常HOLD。自己的资料应填写真实时间，不改日期伪装新证据。

**找不到文件或脚本**

确认终端当前目录就是包含SKILL.md的技能根目录；路径含空格时加双引号。输出目录已存在时换新名字，不覆盖已有结果。

## 当前能力边界

本地快照可以被修改，不能独立证明来源或内容真实；网址结构不是职位真实性。没有实际联系动作就不能填已联系。

## 验证范围

本指南示例已在Windows独立副本中运行复核，见[命令复核结果](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/USER_GUIDES_VERIFICATION.md)。已有回归测试只覆盖被测试行为，不证明真实业务结果。WorkBuddy实际运行、手机端使用和所有系统版本均不在本次已验证范围内。

许可证和素材来源分别见 [LICENSE](LICENSE)、[PROVENANCE.md](PROVENANCE.md)。
