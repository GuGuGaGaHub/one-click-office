# 一键办公（One Click Office）· 开源

> **开源声明**：本技能以开源精神发布，代码与文档可自由查看、复制、修改与再分发，但须遵守本项目 `LICENSE` 中的授权条款。

## 简介

One Click Office 是一个面向 AI Agent 的**办公任务总控 / 路由 Skill**。

本技能不直接读取、修改或生成 `.pptx`、`.xlsx`、`.docx` 等办公软件文件，而是：

1. 识别用户办公任务类型；
2. 路由到对应的专业 Skill；
3. 按专业 Skill 的要求执行；
4. 根据环境状态判断已完成步骤是否需要重新执行；
5. 验证最终产物；
6. 统一交付最终文件或在线文档链接。

本技能本身不替代专业办公 Skill。

---

# 核心原则

## 1. 智能委派，不直接修改办公软件文件

本技能**不直接**读写、修改或生成：

- `.pptx`
- `.xlsx`
- `.xls`
- `.docx`
- `.doc`
- `.csv`
- `.pdf`

等办公软件文件。

所有实际文件操作必须委派给对应的专业 Skill。

| 办公软件域      | 调用技能         | 首要要求                       |
| ---------- | ------------ | -------------------------- |
| Word / 文档  | `lark-doc`   | 首步读取 `lark-doc/SKILL.md`   |
| Excel / 表格 | `sheet`      | 首步读取 `sheet/SKILL.md`      |
| PowerPoint | `ppt`        | 每次新指令后重新读取 `ppt/SKILL.md`  |
| PDF        | `doubao-pdf` | 首步读取 `doubao-pdf/SKILL.md` |

详细触发条件和执行要求见：

```text
references/office-routing.md
```

---

## 2. 执行过程中提供进度反馈

执行命令、委派专业 Skill、生成文件或进行较长处理时，应根据当前阶段向用户提供简短、相关的进度话语。

禁止在长时间执行过程中完全静默。

进度话语应自然融入当前任务，不要求机械照搬示例文本。

---

## 3. 已执行步骤进行状态检查

对于可能已经执行过的步骤，应优先检查当前环境状态，再决定是否重新执行。

检查内容包括：

- 产物是否存在；
- 产物是否早于源文件；
- 文本产物是否包含预期内容；
- 文件是否在指定时间范围内生成；
- 文件大小是否达到最低要求。

使用：

```text
scripts/check_step_state.py
```

进行确定性检查。

只有当检查结果表明环境已经变化、产物缺失或产物不符合要求时，才重新执行对应步骤。

---

# 执行流程

## Step 1：解析用户意图

首先判断用户请求属于：

- Word / 文档
- Excel / 表格
- PowerPoint / 幻灯片
- PDF
- 其他办公任务

例如：

```text
帮我制作一个 PPT
```

应识别为：

```text
PowerPoint / 幻灯片
```

例如：

```text
帮我整理这个 Excel
```

应识别为：

```text
Excel / 表格
```

---

## Step 2：路由到专业 Skill

根据任务类型选择对应专业 Skill。

例如：

```text
PowerPoint
    ↓
ppt
```

```text
Excel / CSV
    ↓
sheet
```

```text
Word / 飞书文档
    ↓
lark-doc
```

```text
PDF
    ↓
doubao-pdf
```

执行专业 Skill 前，必须遵守该 Skill 自身的 `SKILL.md` 要求。

向用户提供简短的路由说明，例如：

> 这个任务属于 PowerPoint，我会调用 `ppt` 技能来处理。

---

## Step 3：检查已有执行状态

对于可能已经执行过的步骤，运行：

```text
python scripts/check_step_state.py ...
```

根据返回的退出码判断当前状态。

### 退出码

```text
0 = 条件成立
1 = 条件不成立
2 = 参数错误或读取错误
```

### 判断规则

如果：

```text
退出码 = 0
```

说明对应检查条件成立，可以根据任务逻辑跳过重复步骤。

如果：

```text
退出码 = 1
```

说明条件不满足，需要重新执行相关步骤。

如果：

```text
退出码 = 2
```

说明检查本身发生参数或读取错误。

此时不得把它误认为“产物已经有效”，应根据错误继续处理或向用户说明。

---

## Step 4：委派专业 Skill 执行

调用对应专业 Skill 完成实际办公任务。

执行过程中：

- 遵守专业 Skill 的规则；
- 不绕过专业 Skill；
- 不自行重复实现专业 Skill 已提供的功能；
- 长任务过程中提供必要的进度反馈。

---

## Step 5：验证最终产物

生成完成后，不应只根据“生成命令成功”判断任务完成。

应通过与生成过程不同的方式回读或检查最终产物。

根据文件类型进行适当验证：

- 文件是否存在；
- 文件是否可读取；
- 内容是否符合预期；
- 数据是否完整；
- 数据是否可以重新计算；
- 文档结构是否正常；
- PPT 页面是否完整；
- PDF 是否可以正常读取。

如果验证失败，不应直接向用户声称任务已经完成。

---

## Step 6：交付

最终产物通过运行环境支持的文件交付机制进行交付。

默认使用：

```text
present_files
```

进行最终文件交付。

在线文档、在线表格或在线幻灯片则交付对应的有效链接。

每个产物只交付一次。

多个最终产物应按照用户阅读或使用顺序进行组织。

---

# 进度话语库

执行过程中可以根据当前阶段自然选择或改写以下话语。

### 开始

> 好的，马上处理你的 XX 任务，先识别该用哪个办公技能。

### 路由

> 这个任务属于 XX，我会调用 XX 技能来处理。

### 检查

> 先检查一下环境，看看这一步之前是否已经完成。

### 执行中

> 正在生成 XX，请稍候。

### 跳过重复步骤

> 检测到 XX 已存在且未变化，这一步跳过，不重复执行。

### 验证

> XX 已生成，我正在检查结果是否完整。

### 完成

> XX 已完成，正在验证并交付给你。

进度话语应根据上下文自然变化，不要机械重复。

---

# 幂等重执行规则

对可能已经执行过的步骤，按照实际需要进行检查。

## 1. 检查产物是否存在

```bash
python scripts/check_step_state.py exists <产物路径>
```

例如：

```bash
python scripts/check_step_state.py exists output.xlsx
```

---

## 2. 检查产物是否不早于源文件

当任务存在源文件和生成文件之间的依赖关系时：

```bash
python scripts/check_step_state.py newer <产物> <源文件>
```

例如：

```bash
python scripts/check_step_state.py newer output.xlsx source.xlsx
```

如果目标文件时间戳不早于源文件，可以认为目标文件没有因为源文件更新而立即失效。

---

## 3. 检查文本内容

对于文本文件：

```bash
python scripts/check_step_state.py contains <产物> <关键词>
```

例如：

```bash
python scripts/check_step_state.py contains report.txt "AI Agent"
```

---

## 4. 检查文件时效

```bash
python scripts/check_step_state.py fresh <路径> --within <秒>
```

例如：

```bash
python scripts/check_step_state.py fresh output.txt --within 3600
```

表示检查文件是否在最近 3600 秒内修改。

---

## 5. 检查文件大小

```bash
python scripts/check_step_state.py size <路径> --min-bytes <N>
```

例如：

```bash
python scripts/check_step_state.py size output.xlsx --min-bytes 1000
```

---

# 状态判断

检查结果：

```text
退出码 0
```

表示对应条件成立。

例如：

```text
EXISTS: output.xlsx
```

可以根据当前任务判断：

> 产物已经存在，可以避免不必要的重复执行。

检查结果：

```text
退出码 1
```

表示对应条件不成立。

例如：

```text
MISSING: output.xlsx
```

需要重新执行相关步骤。

检查结果：

```text
退出码 2
```

表示参数或读取发生错误。

此时不能把该结果当成“步骤已完成”。

---

# Resources

## scripts/

### `scripts/check_step_state.py`

环境状态检查器。

特点：

- Python 标准库；
- 不依赖第三方 Python 包；
- 只读取环境；
- 不修改办公软件文件；
- 返回确定性的退出码。

支持：

```text
exists
newer
contains
fresh
size
```

---

## references/

### `references/office-routing.md`

办公任务路由详细规则。

包含：

- Word / 文档触发条件；
- Excel / 表格触发条件；
- PowerPoint / 幻灯片触发条件；
- PDF 触发条件；
- 其他办公任务处理方式；
- 对应专业 Skill；
- 专业 Skill 执行要求；
- 交付规则。

该文件应根据实际需要按需读取，而不是在每次任务中无条件读取全部内容。

---

# Dependencies

本 Skill 是一个**总控 / 路由型 Skill**，不包含所有具体办公能力。

当前设计依赖以下专业 Skill：

```text
lark-doc
sheet
ppt
doubao-pdf
```

这些 Skill 不包含在本仓库中。

使用本 Skill 前，请确保运行环境中已经安装或提供相应专业 Skill。

---

# 安全原则

1. 不在本 Skill 中保存 API Key。
2. 不在仓库中保存密码或访问令牌。
3. 不绕过专业 Skill 的权限控制。
4. 不把未验证的结果声明为成功。
5. 不因为检查命令失败就假定产物有效。
6. 不无条件重复执行可能产生重复文件或重复操作的任务。
7. 对外部文件和用户提供的数据遵守运行环境的安全限制。
8. 遵守专业 Skill 自身的安全要求。

---

# Open Source

One Click Office 以开源方式发布。

代码、Skill 定义、脚本和文档可以在本项目许可证允许的范围内进行查看、复制、修改、再分发和二次开发。

具体授权条件请参阅：

```text
LICENSE
```
