# 机器翻译 需求说明

> 本文件由 prototype-spec-annotator 基于原型代码自动生成,仅包含代码中可验证的内容。
> 标注「未在代码中体现」处为代码缺失,需人工补充或完善原型后重生成。

## 页面信息
- 页面路径：txt_trastor/text_translation.html
- 页面类型：混合（表单提交 + 列表 CRUD 弹窗 + 结果展示）
- 生成时间：2026-09-21 17:11
- 复杂度判定：复杂(原因：含表单提交「立即翻译」+ 敏感词弹窗增删改查 >3 按钮 + 状态流转 ready→loading→done/error/empty + 敏感词风控拦截逻辑)

## ① 前置条件
- 角色权限：未在代码中体现（页面无路由 meta 或权限判断代码）
- 菜单/入口可见条件：未在代码中体现（页面为独立 HTML，无父级菜单跳转代码）

## ② 业务规则
- 触发条件：未在代码中体现（页面为独立 HTML 直接访问，无路由跳转代码）
- 状态流转：翻译状态 `ready → loading → done`（正常）；`ready → loading → error`（敏感词拦截）；`ready → empty`（空内容提交）。来源：txt_trastor/text_translation.html:1183-1189（labels 定义）、:1148-1160（doTranslate 中 setStatus 调用）
- 关联影响：敏感词列表（`SENSITIVE_WORDS`）的增删改会直接影响翻译前置风控 `preRiskControl` 的拦截结果。来源：txt_trastor/text_translation.html:737（变量定义）、:1083-1089（preRiskControl 读取该数组）

## ③ 页面说明

### 字段说明
> 仅列代码真实出现的字段（`<input>`、`<textarea>`、下拉选择）。

| 字段名 | 类型 | 必填 | 说明 | 来源 |
|--------|------|------|------|------|
| 源语言（srcLang） | select | 否 | 下拉选择，默认「自动检测」，共 12 项（自动检测/中文/英语/日语/韩语/法语/德语/西班牙语/俄语/阿拉伯语/葡萄牙语/意大利语） | txt_trastor/text_translation.html:543 |
| 目标语言（tgtLang） | select | 否 | 下拉选择，默认 English（不含「自动检测」项，共 11 项），下拉容器带 `active` 类高亮 | txt_trastor/text_translation.html:555 |
| 专业领域（domain） | select | 否 | 下拉选择，默认「通用」，共 5 项（通用/信息技术/生物医药/金融财经/法律合同） | txt_trastor/text_translation.html:565 |
| 原文输入（inputText） | textarea | 否 | placeholder「请输入要翻译的单词或句子」，maxlength=2000，右下角实时计数「N / 2000」 | txt_trastor/text_translation.html:605 |
| 敏感词搜索（sensitiveSearch） | text | 否 | 弹窗内，placeholder「搜索敏感词…」，实时过滤列表 | txt_trastor/text_translation.html:676 |
| 新敏感词输入（newWordInput） | text | 否 | 弹窗底部，placeholder「输入新敏感词，回车添加」，maxlength=30 | txt_trastor/text_translation.html:696 |
| 行内编辑输入（editInput-*） | text | 否 | 弹窗列表行编辑态，maxlength=30，回车保存/Esc 取消 | txt_trastor/text_translation.html:925 |

### 状态枚举
> 仅列代码可见的字典/常量/条件。

翻译状态（statusPill）：1.已就绪(ready) 2.翻译中(loading) 3.已完成(done) 4.已拦截(error) 5.请输入内容(empty)（来源：txt_trastor/text_translation.html:1183-1189 labels 定义）

敏感词按钮激活态：`on`（列表非空，显示青色圆点）/ 非 on（列表为空，不显示圆点）（来源：txt_trastor/text_translation.html:1043-1048 updateSensitiveBtnState）

## ④ 操作说明

> 每个按钮一行。toast 文案逐字来自代码。

| 操作按钮 | 显示条件 | 点击行为 | 校验规则 | 成功反馈 | 失败反馈 | 状态变化 | 来源 |
|---------|---------|---------|---------|---------|---------|---------|------|
| 切换主题（themeBtn） | 始终显示 | 切换 html 根元素 dark/light 类，切换月亮/太阳图标 | 无 | 无 | 无 | dark↔light 主题切换 | txt_trastor/text_translation.html:512,839 |
| UI 语言（uiLangBtn） | 始终显示 | 切换 state.uiLang zh↔en，更新所有标签文案 | 无 | 无 | 无 | 中文↔英文 UI 切换 | txt_trastor/text_translation.html:515,852 |
| 交换语言（swapBtn） | 始终显示 | 交换 srcLang 与 tgtLang；若源为 auto 则取 zh 作为新目标 | 无 | 无 | 无 | 源/目标语言互换 | txt_trastor/text_translation.html:550,868 |
| 源语言下拉（srcLang） | 始终显示 | 打开/关闭菜单，选中后更新 state.srcLang 与标签 | 无 | 无 | 无 | 源语言变更 | txt_trastor/text_translation.html:543,822 |
| 目标语言下拉（tgtLang） | 始终显示 | 打开/关闭菜单，选中后更新 state.tgtLang 与结果标题 | 无 | 无 | 无 | 目标语言变更 | txt_trastor/text_translation.html:555,822 |
| 专业领域下拉（domain） | 始终显示 | 打开/关闭菜单，选中后更新 state.domain；若已有结果则重新翻译 | 无 | 无 | 无 | 领域变更 | txt_trastor/text_translation.html:565,1282 |
| 敏感词按钮（sensitiveBtn） | 始终显示（列表非空时带 on 类与青色圆点） | 打开敏感词管理弹窗，渲染列表，聚焦新词输入框 | 无 | 无 | 无 | 弹窗显示 | txt_trastor/text_translation.html:573,891 |
| 立即翻译（translateBtn） | 始终显示（翻译中 disabled） | 调用 doTranslate：空内容→setStatus(empty)；超长→showError；敏感词命中→拦截；否则模拟翻译 | 空→提示；>2000→提示；敏感词命中→拦截 | 无（成功直接显示译文） | 「文本包含敏感内容，已拦截，请修改后重试。」/「请输入要翻译的内容。」/「文本过长，请拆分后重试。」 | ready→loading→done / error / empty | txt_trastor/text_translation.html:580,1114-1164 |
| 清空（clearBtn） | 始终显示 | 清空 inputText、计数归零、清结果区、隐藏错误、聚焦输入框 | 无 | 无 | 无 | 输入与结果清空 | txt_trastor/text_translation.html:600,1073 |
| 朗读译文（speakBtn） | 始终显示（结果区有内容时有效，朗读中带 speaking 类脉冲动画） | 无结果则返回；朗读中点击则取消；否则 speechSynthesis 朗读 lastResult | 无结果→不响应 | 无 | 「浏览器不支持语音朗读」 | speaking 开关 | txt_trastor/text_translation.html:623,1217 |
| 复制译文（copyBtn） | 始终显示（结果区有内容时有效） | 过滤 `***` 脱敏符后写入剪贴板；clipboard API 失败则 execCommand 兜底 | 无结果→不响应 | 「复制成功」/「Copied」 | 「复制失败」/「Copy failed」 | 无 | txt_trastor/text_translation.html:626,1239 |
| 关闭弹窗（dialogClose） | 弹窗显示时 | 关闭弹窗，取消所有行内编辑 | 无 | 无 | 无 | 弹窗隐藏 | txt_trastor/text_translation.html:667,895 |
| 快速添加（quickAddBtn） | 弹窗显示时 | 聚焦底部新词输入框 | 无 | 无 | 无 | 无 | txt_trastor/text_translation.html:678,1022 |
| 取消（dialogCancel） | 弹窗显示时 | 关闭弹窗，取消所有行内编辑 | 无 | 无 | 无 | 弹窗隐藏 | txt_trastor/text_translation.html:699,896 |
| 保存（dialogSave） | 弹窗显示时 | 若有行内编辑则先保存；关闭弹窗；更新 footInfo；若有结果则重新翻译 | 无 | 无 | 无 | 弹窗关闭，风控列表可能更新 | txt_trastor/text_translation.html:700,1027 |
| 行-编辑（edit） | 每行显示 | 该行进入编辑态，变输入框，聚焦并全选 | 无 | 无 | 无 | 行进入编辑态 | txt_trastor/text_translation.html:941,957 |
| 行-保存（save） | 编辑态显示 | 校验非空+不重复，更新 SENSITIVE_WORDS[id]，退出编辑态 | 空→「敏感词不能为空」；重复→「该敏感词已存在」 | 「已更新」 | 「敏感词不能为空」/「该敏感词已存在」 | 列表项更新 | txt_trastor/text_translation.html:927,957 |
| 行-取消编辑（cancel） | 编辑态显示 | 退出编辑态，重新渲染 | 无 | 无 | 无 | 行退出编辑态 | txt_trastor/text_translation.html:930,957 |
| 行-删除（delete） | 每行显示 | 从 SENSITIVE_WORDS 删除该项，退出编辑态，更新按钮状态 | 无 | 「已删除」 | 无 | 列表项删除，按钮可能失活 | txt_trastor/text_translation.html:944,957 |

## ⑤ 异常处理

> 本技能只记录代码可见的异常处理逻辑。每条指向代码。

- 空内容拦截：点击「立即翻译」时若 `inputEl.value.trim()` 为空 → showError「请输入要翻译的内容。」+ setStatus("empty")，不发起翻译（来源：txt_trastor/text_translation.html:1119-1124）
- 超长文本拦截：`text.length > 2000` → showError「文本过长，请拆分后重试。」，不发起翻译（来源：txt_trastor/text_translation.html:1126-1130）。注：textarea 的 maxlength=2000 已在输入层限制（:605）
- 敏感词前置风控拦截：`state.sensitive` 为真且 `preRiskControl` 命中（文本包含 SENSITIVE_WORDS 中任一词）→ showError「文本包含敏感内容，已拦截，请修改后重试。」+ `***` 掩码 + setStatus("error") + 清空结果区（来源：txt_trastor/text_translation.html:1132-1142,1083-1089）
- 字数预警：输入长度 >1800 且 <2000 → 计数变 warn（黄色）；≥2000 → 变 danger（红色）（来源：txt_trastor/text_translation.html:1079-1081）
- 翻译中防重复：`state.isTranslating` 为真时 doTranslate 直接 return；翻译按钮 disabled（来源：txt_trastor/text_translation.html:1116,1147,1160）
- 复制兜底：navigator.clipboard.writeText 失败 → 降级 execCommand("copy")；再失败 → showToast「复制失败」（来源：txt_trastor/text_translation.html:1247-1252）
- TTS 不可用：`!("speechSynthesis" in window)` → showToast「浏览器不支持语音朗读」，不朗读（来源：txt_trastor/text_translation.html:1225-1228）
- 敏感词去重校验：新增/编辑时若词已存在于 SENSITIVE_WORDS → showToast「该敏感词已存在」，不写入（来源：txt_trastor/text_translation.html:974,996,1012）
- 中间态：翻译中 translateBtn 加 loading 类（显示 spinner + 「翻译中…」）+ setStatus("loading")，700ms 后回写结果（来源：txt_trastor/text_translation.html:1147-1160,287-288）
- 并发处理：未在代码中体现（无防抖/请求取消机制，但 isTranslating 标志位阻断了重复点击）
