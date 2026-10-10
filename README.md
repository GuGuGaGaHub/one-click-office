\# One Click Office



\*\*One Click Office（一键办公）\*\* 是一个开源的 AI Agent 办公任务总控 Skill。



它不直接修改或生成 Office 文件，而是根据用户的任务意图，自动识别办公任务类型，并将任务路由到对应的专业 Skill 执行。



支持 Word / 文档、Excel / 表格、PowerPoint / 幻灯片、PDF，以及其他办公类任务。



\## ✨ Features



\- 📝 Word / 文档任务智能路由

\- 📊 Excel / CSV / 表格任务智能路由

\- 📽️ PowerPoint / PPT 任务智能路由

\- 📄 PDF 任务智能路由

\- 🔀 专业 Skill 自动委派

\- 🔍 已执行步骤状态检查

\- ♻️ 基于环境状态的幂等重执行

\- 💬 执行过程进度播报

\- ✅ 生成后的产物验证

\- 📦 统一交付最终文件或链接



\## 🧩 Architecture



One Click Office 本身是一个\*\*总控 / 路由型 Skill\*\*。



基本工作流程：



```text

用户请求

&#x20;  │

&#x20;  ▼

one-click-office

&#x20;  │

&#x20;  ├── 任务意图识别

&#x20;  │

&#x20;  ├── 专业 Skill 路由

&#x20;  │

&#x20;  ├── 环境状态检查

&#x20;  │

&#x20;  ├── 委派专业 Skill 执行

&#x20;  │

&#x20;  ├── 结果验证

&#x20;  │

&#x20;  └── 最终交付

&#x20;         │

&#x20;         ├── 文件

&#x20;         └── 在线文档 / 表格 / 幻灯片链接

```



\## 🔧 Supported Skills



当前路由设计包括：



| 任务类型 | 专业 Skill |

|---|---|

| Word / 文档 | `lark-doc` |

| Excel / 表格 | `sheet` |

| PowerPoint / 幻灯片 | `ppt` |

| PDF | `doubao-pdf` |



这些专业 Skill 需要在运行环境中单独存在。



`one-click-office` 不会将这些专业 Skill 的实现代码复制到自身仓库中。



\## 📁 Directory Structure



```text

one-click-office/

├── SKILL.md

├── README.md

├── LICENSE

├── scripts/

│   └── check\_step\_state.py

└── references/

&#x20;   └── office-routing.md

```



\### SKILL.md



AI Agent 的主要 Skill 定义文件。



包含：



\- Skill 名称和描述

\- 触发条件

\- 核心原则

\- 任务执行流程

\- 专业 Skill 路由

\- 幂等执行规则

\- 进度话语规则

\- 资源说明



\### scripts/



包含 Skill 所需的辅助脚本。



当前包括：



```text

scripts/check\_step\_state.py

```



该脚本用于检查已经执行步骤的环境状态。



支持：



```text

exists

newer

contains

fresh

size

```



\### references/



存放按需加载的详细规则。



当前包括：



```text

references/office-routing.md

```



该文件包含：



\- Word / 文档路由规则

\- Excel / 表格路由规则

\- PowerPoint / 幻灯片路由规则

\- PDF 路由规则

\- 其他办公任务路由规则

\- 通用交付规则



\## ♻️ Idempotent Execution



One Click Office 支持基于环境状态判断是否需要重复执行。



例如：



```text

检查产物

&#x20;   │

&#x20;   ├── 不存在 → 重新执行

&#x20;   │

&#x20;   ├── 已过期 → 重新执行

&#x20;   │

&#x20;   ├── 内容不符合 → 重新执行

&#x20;   │

&#x20;   └── 状态正常 → 跳过重复执行

```



状态检查脚本的退出码：



```text

0 = 条件成立

1 = 条件不成立

2 = 参数错误或读取错误

```



例如：



```bash

python scripts/check\_step\_state.py exists output.xlsx

```



检查文件是否存在。



检查目标文件是否不早于源文件：



```bash

python scripts/check\_step\_state.py newer output.xlsx source.xlsx

```



检查文本文件是否包含指定内容：



```bash

python scripts/check\_step\_state.py contains output.txt "关键词"

```



检查文件是否在指定时间范围内更新：



```bash

python scripts/check\_step\_state.py fresh output.txt --within 3600

```



检查文件大小：



```bash

python scripts/check\_step\_state.py size output.xlsx --min-bytes 1000

```



\## 📦 Dependencies



本 Skill 是一个总控 / 路由 Skill。



运行具体办公任务时，需要相应的专业 Skill：



```text

lark-doc

sheet

ppt

doubao-pdf

```



这些 Skill 不包含在本仓库中。



请根据你的 AI Agent 运行环境安装或配置对应的专业 Skill。



\## 🔒 Safety \& Design Principles



One Click Office 遵循以下设计原则：



1\. 不直接修改 Office 文件。

2\. 不绕过专业 Skill 的执行规则。

3\. 执行具体任务前读取对应专业 Skill 的说明。

4\. 对可能重复执行的步骤进行状态检查。

5\. 不因为已有产物就盲目重复生成。

6\. 生成后进行独立验证。

7\. 最终结果统一交付。

8\. 不在 Skill 中保存 API Key、密码或其他敏感凭据。



\## 🌐 Open Source



本项目以开源方式发布。



你可以查看、复制、修改和再分发本项目，但请遵守仓库中的 `LICENSE` 条款。



\## 📄 License



This project is licensed under the MIT License.



See \[`LICENSE`](LICENSE) for details.



\## ⭐ Contributing



欢迎提交：



\- Bug 修复

\- 路由规则改进

\- 新办公软件 Skill 支持

\- 文档改进

\- 状态检查能力改进

\- Agent 工作流优化



如果你扩展了新的办公 Skill，可以在 `references/office-routing.md` 中增加对应的路由规则。



\## 💡 Example



用户：



```text

帮我制作一份关于 AI Agent 的 PPT。

```



One Click Office：



```text

识别任务

&#x20;  ↓

PowerPoint / 幻灯片

&#x20;  ↓

调用 ppt Skill

&#x20;  ↓

读取 ppt/SKILL.md

&#x20;  ↓

检查已有产物

&#x20;  ↓

执行 PPT 创建

&#x20;  ↓

验证 PPT

&#x20;  ↓

交付 .pptx

```



用户：



```text

帮我整理这个 Excel 数据。

```



路由：



```text

Excel / 表格

&#x20;  ↓

sheet Skill

&#x20;  ↓

读取 sheet/SKILL.md

&#x20;  ↓

处理数据

&#x20;  ↓

验证结果

&#x20;  ↓

交付表格

```



\---



\*\*One Click Office · Open Source\*\*



一个面向 AI Agent 的办公任务智能路由 Skill。

