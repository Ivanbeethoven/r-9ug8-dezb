# 原始资料来源（2026-11-05 采集）

本目录保存申请书的**事实来源**，便于日后核对与申诉时追溯。PDF 为官方原件，`*.txt` 为对应正文提取。

| 文件 | 来源 | 说明 |
| --- | --- | --- |
| `2026-CCF-蚂蚁科研基金-第二批次-申报指南.pdf` | ccf.org.cn（CCF-蚂蚁科研基金项目组，2026-10-12） | 官方《项目申报指南》，含申报条件、时间计划、评审标准、16 项课题清单、管理与知识产权条款 |
| `2026-CCF-蚂蚁科研基金-第二批次-申报课题介绍.pdf` | 同上（附件 2） | 16 项课题的逐项说明；本次申报课题在"二、超算与智算方向"第 2 项 |
| `申报指南-正文提取.txt` / `申报课题介绍-正文提取.txt` | 上述 PDF 的 pypdf 文本提取 | 便于全文检索；PDF 为权威原件 |
| `蚂蚁申报页-表单字段.txt` | antresearch.com 申报页面前端代码抽取 | 在线表单的字段、下拉项、附件限制（单文件、≤500MB） |
| `冯洋-主页与荣誉-提取.txt` | fengyang-nju.github.io | 申请人履历、代表论文、荣誉（荣誉页为静态 HTML，已全文提取） |
| `BrewFS-README.md` | github.com/brewfs/brewfs | 项目定位、架构、性能基线、测试矩阵、路线图（含 2026-09-22 阿里云对齐评测全部数字） |
| `BrewFS-架构概述.md` | 仓库 `doc/architecture/arch.md` | 六层架构、读写路径、模块依赖 |
| `BrewFS-workspace-overlay-设计文档.md` | 仓库 `doc/architecture/workspace-overlay.md` | 只读基座 / 私有增量层的数据模型、租约与代次、恢复意图、GC 协议 |
| `Nydus-README.md` | github.com/dragonflyoss/nydus | EROFS / RAFS、按需加载、chunk 去重、存储后端（用于准确性核对，未在正文过度引用） |

## 采集方式备注

- CCF 站点与 antresearch 页面均需绕过前端渲染：指南/课题介绍直接下载 PDF 后用 `pypdf` 提取文本；
  申报表单字段从前端 JS chunk 中解码 `\uXXXX` 转义得到。
- BrewFS 文档直接取 `raw.githubusercontent.com`。
- 蚂蚁申报页（`/cooperation/Funds/FundsDetails/20261012001`）为 SPA，HTML 层无正文；
  其内容与 CCF 发布的指南/课题介绍一致，故以 CCF 原件为准。

## 需要注意的一处官方笔误

《申报指南》第十条把课题名写作 **"Nydus EROF"**（漏 S），《申报课题介绍》正文为 **"Nydus EROFS"**。
申请书按 **EROFS** 撰写；在线表单的"课题选择"下拉以官网实际显示为准，若显示 EROF 应照抄下拉原文。
