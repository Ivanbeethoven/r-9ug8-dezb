# 写作任务简报：CCF-蚂蚁科研基金（第二批次）项目申请书

> 本文件是给写作 agent 的事实底稿 + 写作规范。所有事实以此为准，不得编造数字。

## 1. 申报项目基本信息（已确认，不得改动）

- 基金：2026 年度 CCF-蚂蚁科研基金（第二批次），由 CCF 与蚂蚁集团联合设立
- 方向：**超算与智算**
- 课题：**面向 AI Agent 沙箱极速冷启动的 Nydus EROFS 按需加载与 Checkpoint/Restore 机制研究**
- 支持金额：不超过 **30 万元/项**；合作周期：**1 年**
- 申报截止：2026-11-11 24:00（北京时间）；结果公布 2026-12-29；合同签署 2027-02 中旬
- 申请人（PI）：**冯洋**，南京大学计算机学院 副教授、博士生导师；软件安全与编译技术实验室
- 依托单位：南京大学
- 依托开源项目：**BrewFS**（Rust 分布式文件系统，https://github.com/brewfs/brewfs ，MIT）

## 2. 课题原文（蚂蚁方需求，写作必须逐条呼应）

### 研究背景（原文要点）
> 随着 AI 大模型与智能体技术进入规模化落地阶段，截至 2026 年 9 月，Agent 执行环境的启动速度、资源周转效率和服务稳定性被推向了新的高度。AI Agent 任务通常具有高并发、短生命周期、快速弹性扩缩容、环境依赖复杂等特点，沙箱作为 Agent 代码执行、工具调用和任务隔离的基础载体，其启动速度直接影响用户首次响应体验、任务调度效率和算力资源利用率。当前沙箱启动并不是单点问题，而是覆盖管控请求下发、沙箱调度、节点侧 containerd 创建、镜像准备、runD 运行时启动、OSS/存储挂载、网络设备初始化、日志初始化等多个环节的全链路问题。尤其在大镜像冷启动、无缓存节点扩容、批量任务拉起和高并发创建场景下，镜像完整下载与解压、运行时从零初始化、网络和存储资源串行准备、原生控制面链路过长、containerd 高并发 GC 抖动等问题会显著拉长启动时间，并造成创建长尾。

### 技术判断（原文要点）
> 实现 AI Agent 沙箱极速启动的关键，是将传统"完整下载镜像、从零初始化运行时、串行准备资源"的启动路径，转变为"按需加载、状态复用、并行预热、轻量调度"的新启动范式。现有不足：传统 OCI 镜像需完整拉取和解压，大镜像冷启动耗时高；runD 等安全运行时每次创建都需重新准备运行环境、初始化资源并启动 guest 内核，重复开销明显；原生 K8s 控制面链路较长，难以满足毫秒级调度和快速拉起；网络、存储、containerd 等周边环节在高并发下容易出现内核锁争抢、RPC 排队、GC 风暴和创建长尾。**更重要的是，镜像按需加载与沙箱运行时状态快照恢复往往分别设计，缺少面向 AI Agent 沙箱场景的统一数据格式、恢复链路和调度协同机制。**
> 本课题拟以 Nydus EROFS 格式的冷启动镜像 Lazyload 和 Nydus EROFS 格式的 Checkpoint/Restore 为核心，研究大镜像按需加载、沙箱状态固化与快速恢复、全链路协同优化机制，形成面向 AI Agent 沙箱的极速冷启动技术体系。

### 预计产出（硬性交付）
1. 报告：结项验收表、结项验收报告
2. 论文：CCF-A 类及蚂蚁认可期刊/会议论文 **1-2 篇**并最终收录，提供论文底稿及收录邮件
3. 专利：协助蚂蚁和/或其关联公司提交国内、国际专利 **1 项**，交付专利申请号与材料
4. 算法原型：一套面向 AI Agent 沙箱的极速冷启动原型系统，支持 Nydus EROFS 格式大镜像冷启动 Lazyload、Nydus EROFS 格式 Checkpoint/Restore、沙箱池化预热、网络/存储资源池化、控制面链路精简与运行时高并发优化
5. **技术指标**：典型场景下
   - 大镜像（以 4G 镜像为例）冷启动从 **10s 左右降到 1s 左右**
   - 基于快照的沙箱启动在 **100ms 级**
   - 单机 **100 个沙箱并发创建无明显长尾**

### 评审标准（写作用力方向）
1. 课题的价值、创新性和可行性
2. proposal 与蚂蚁课题需求的**匹配度**
3. 执行计划及交付成果的价值
4. 申请人（及团队）的学术水平和科研能力

## 3. 团队与研究基础（真实事实，可引用）

### PI：冯洋（南京大学计算机学院，副教授、博导）
研究方向两条主线：
- **软件质量保障与智能技术**：DeepGini (ISSTA 2020) 深度神经网络测试优先级；Adaptive Test Selection (ICSE 2022)；QATest (ASE 2022) 问答系统模糊测试；Datactive (ISSTA 2024) 目标检测数据故障定位；AtPatch (ICSE 2026) Transformer 注意力异常诊断与修复；TACO (ICSE 2026) 编程辅助场景大模型可信度评估；VADA (ICSE 2026) 价值对齐评估；Drivence (TSE 2026)；MoCo (TSE 2025) 深度学习库测试生成；RediI (ICSE 2025) 分布式系统确定性故障复现；深度学习框架缺陷实证研究 (IST 2022)
- **语言与软件工程 / AI 基础设施**：FRIES (ISSTA 2024) Rust 库交互模糊测试；PALM (ASE 2025) 单元测试覆盖率；RustGTC (ASE 2026) 约束引导 API 测试生成；RustC4/RustC4++ (TOSEM 2026) 代码-注释一致性；PanicFI (TOSEM 2026) panic bug 修复基础设施；SugBreaker (FSE 2026) 编译器修复建议测试；C/C++→Rust 可信迁移
- **分布式文件系统与面向 AI 的异构引擎**（网站明确列出的在研方向）："The team is currently working on the design and implementation of distributed file systems and heterogeneous engines for AI."
- 荣誉：ACM SIGSOFT Distinguished Paper Award ×3（ASE 2022、ESEC/FSE 2023、Internetware 2023）；华为火花奖（2024）、华为技术创新奖（2023）、华为创新实践奖（2023）；小米青年科技奖（2025）；**旋武社区 2025 贡献奖（OpenAtom 旋武开源社区）**；**蚂蚁集团 TuGraph 社区 2024 年度合作伙伴**；CCF ChinaSoft 2023 优秀论坛奖
- 服务：ICSE 2027、FSE 2027 程序委员会；《Rust 语言程序设计》教材（机械工业出版社，付印中）；全国计算机类课程实验教学案例设计竞赛一等奖（2023、2026）

### 开源项目 BrewFS（申请书的技术底座）
定位：*A Rust distributed filesystem for object storage, POSIX workloads, and isolated agent workspaces.* 旋武社区（OpenAtom）Rust 开源项目推荐，MIT 许可。

架构事实：
- 单一 Rust 数据通路：FUSE（自研 asyncfuse）→ VFS → 元数据事务 → 缓存/写回 → 对象存储
- 元数据后端可插拔：SQLite / PostgreSQL / Redis / etcd / TiKV（SeaORM + Lua CAS / 事务）
- 数据后端：S3 兼容（RustFS、MinIO、AWS S3、Ceph RGW）或本地文件系统
- 数据布局：文件切 64 MiB chunk、4 MiB block，块为不可变对象，位于事务性命名空间之下
- 分层缓存：Linux page cache、BrewFS 内存缓存、SSD 缓存、预读、写回 staging、大写入合并（write coalescing）
- 控制面：`info` / `gc` 通过 Unix domain socket 与 daemon 通信；`.stats` 暴露 FUSE/缓存计数器

**Workspace Overlay（与本课题最相关的核心能力）**
- 一份**不可变 packed lower**（打包快照，manifest + digest + 校验）+ 每个 agent 一份**私有可写 upper**（no seal step，head 不轮转）
- 从精确 revision 创建/fork workspace：只写元数据与新的可写头，**不复制 clean 数据**、不遍历复制目录树
- 未命中 upper 的条目回落到 lower；显式 tombstone 抑制回落；元数据变更与新数据 slice 归 upper
- `diff` / lease-aware `discard`；可 seal 封存、snapshot 生成版本，再基于快照 fork 迭代
- **后端租约 + generation fencing**：保证每个 workspace 恰好一个写者，防止所有权变更后 stale mount 继续写
- 只隔离文件视图；进程、网络、权限由上层沙箱负责（与 runD 的职责边界天然互补）
- 后端：Redis / TiKV 分布式 catalog（SQLite 用于本地语义与开发）
- 与 JuiceFS Clone 的差异：Clone 复制目录项与元数据；BrewFS fork 依托封存基线只存增量元数据，无需遍历复制整棵目录树，并规避克隆期源目录变动的不一致风险
- 当前状态：`workspace-overlay` 为可选 Cargo feature，`workspace-v1` 不回落 flat 行为；运维工具链仍在成熟（这点要在"风险与工程路径"中诚实处理）

工程与正确性基线：
- Rust 工作区测试；**xfstests 708 个配置用例**通过（SQLite / Redis / etcd / TiKV 四种后端 profile）；**pjdfstest 246 个文件、9134 条断言**通过（Redis、TiKV，无默认排除）；LTP 文件系统 profile 四后端通过；stress-ng + fio 压测；fuzzing；可复现 Docker Compose runner
- 观测：`brewfs_fuse_read_ops_total` / `brewfs_fuse_read_bytes_total` / page cache / block cache / persistent slice 读取计数器

公开性能基线（2026-09-22 阿里云对齐评测，BrewFS vs JuiceFS 1.4.1，同 ECS 规格/镜像/盘型/地域/OSS 内网路径/fio 负载，各 4 GiB 内存缓存 + 8 GiB SSD 缓存，11 项工具全部通过；含写入的负载使用"完全排空吞吐"口径）：

| 负载 | BrewFS | JuiceFS 1.4.1 | 增益 |
| --- | ---: | ---: | ---: |
| 大文件读 | 334.42 MiB/s | 328.94 MiB/s | +1.7% |
| 顺序读 | 1814.4 MiB/s | 1321.6 MiB/s | +37.3% |
| 随机读 | 2510.7 MiB/s | 1773.3 MiB/s | +41.6% |
| 大文件写（完全排空） | 217.55 MiB/s | 208.26 MiB/s | +4.5% |
| 顺序写（完全排空） | 320.43 MiB/s | 184.57 MiB/s | +73.6% |
| 随机写（完全排空） | 328.73 MiB/s | 198.31 MiB/s | +65.8% |
| 混合随机 I/O（完全排空） | 475.77 MiB/s | 190.55 MiB/s | +149.7% |

写回排空：BrewFS 大/顺序/随机/混合写分别 4/4/2/2 秒，JuiceFS 4/127/118/91 秒。
已知短板（要写进优化目标）：BrewFS 随机写 p99 463.471 ms、混合写 p99 492.831 ms，JuiceFS 为 92.799 / 10.945 ms —— **前台写尾延迟是明确的优化目标**。

2026-11-02 本地小写合并对比（release d5e53e1，Redis/RustFS，flat-v1，同二进制合并开/关）：随机写 wall+drain 2.237 → 4.752 MiB/s（+112.44%），混合随机 I/O 2.555 → 3.164 MiB/s（+23.87%），随机写 PUT/GiB 261,490.89 → 16,379.61（−93.74%），随机写 p99 387.973 → 235.930 ms（−39.19%）。

## 4. 与蚂蚁技术栈的衔接点（写作要显式建立，但不得编造蚂蚁内部数据）

- 蚂蚁沙箱栈涉及：containerd、**runD**（安全容器运行时，Rust 生态）、**Nydus**（EROFS 镜像格式 + lazyload + 可做 C/R 镜像）、OSS、K8s 控制面
- BrewFS 同样是 Rust 实现、单进程 daemon、FUSE 挂载、对象存储原生 —— 与 runD/Nydus 的语言与部署形态一致，可以共建"统一数据格式 + 统一恢复链路"
- 本课题的关键科学问题正是课题原文点明的"**镜像按需加载与运行时状态快照恢复分别设计，缺少统一数据格式、恢复链路和调度协同机制**"——BrewFS 的 workspace overlay（packed lower + 私有 upper + lease/fencing）天然就是这个统一层
- 必须诚实：BrewFS 不是蚂蚁官方项目，是团队主导的开源项目；申请书里应表述为"团队主导的开源底座"，并说明与蚂蚁栈的对接方式（FUSE mount 到 runD guest 内 / 宿主机侧 workspace 服务 / OSS 后端）

## 5. 技术主张（本申请书的创新点骨架，写作时按此展开并使之自洽）

**核心论点**：把"沙箱冷启动"从"镜像传输问题"重新定义为"**文件系统视图的按需构建与状态复用问题**"，用 BrewFS 的 workspace overlay 作为 Nydus EROFS 之上/之下的统一元数据与数据面，使 lazyload、C/R、池化预热、并发创建共享同一套格式、同一套缓存、同一套生命周期机制。

候选创新点（4 项，需各自有可验证的技术指标）：
1. **统一镜像-工作区格式**：Nydus EROFS 镜像层作为不可变 packed lower，Agent 的运行时/工作区增量作为私有 upper；一次 fork 只写元数据头，做到 O(元数据) 而非 O(数据) 的沙箱创建。目标：4G 镜像 10s → ≤1s（冷启动、无本地缓存节点），创建路径的字节级传输量下降 ≥90%
2. **EROFS 语义下的按需加载与元数据预热**：按 chunk/block 粒度 range read + 预读策略 + 内存/SSD 两级缓存，把随机小 I/O 的首次命中延迟压到可接受；块按需提升（只在观察到复用后提升）避免缓存污染。目标：首次 read 命中 p99、元数据 attach 时间
3. **快照 Checkpoint/Restore 的持久化与快速恢复**：利用 packed manifest + 校验 + 租约/generation fencing，实现沙箱状态镜像的一致固化（fsync/原子命名空间）+ 从对象存储直接恢复挂载（无需本地解压）；目标：快照沙箱启动 100ms 级
4. **高并发创建的长尾抑制**：单机 100 沙箱并发创建无长尾；前台/后台资源隔离（写回、GC、compaction 与创建路径解耦）、元数据批量提交（per-operation batched rows）、控制面链路精简、池化预热（pool warmup）。目标：p99 创建时延、GC 抖动抑制

## 6. 写作要求（严格执行）

1. **语言**：中文（技术术语可保留英文）。学术申请书语气：准确、克制、可验证，不写营销口号，不用"颠覆""革命性"。
2. **禁止编造**：不得虚构蚂蚁内部指标、不得虚构未验证的实验结果、不得虚构团队成员姓名与论文。涉及"预期"的数字要标明是目标值（target）并给出论证依据（基于 BrewFS 已有实测的合理外推）。
3. **对齐课题**：每一节都要让评审看到"这就是蚂蚁那个课题"。技术指标章必须逐条映射课题的三条硬指标。
4. **具体**：写清数据结构、关键路径、失败模式、评测方法（fio/xfstests/自建 benchmark harness、对照基线、口径）。宁少写空话，多写机制。
5. **诚实处理边界**：workspace overlay 仍是 opt-in feature、运维工具链在成熟、写尾延迟是短板——这些要写进"风险与应对"，反而增强可信度。
6. 论文标注：成果论文需标注 "This work was supported by Ant Group through CCF-Ant Research Fund"（在"成果与知识产权"节体现）。

## 7. 交付章节与字数（总计约 12000–15000 字）

| 文件 | 章节 | 字数 |
| --- | --- | --- |
| `sections/01-summary.md` | 摘要 + 项目基本信息表 + 一句话价值主张 | 700 |
| `sections/02-background.md` | 研究背景与问题分析（拆解沙箱启动全链路 8 个环节、定位 5 类开销、指出"分别设计"这一根本缺口） | 1800 |
| `sections/03-goals.md` | 研究目标、关键科学问题、三条硬指标的可行性推演（用 BrewFS 实测数据做量化论证） | 1500 |
| `sections/04-content.md` | 研究内容（4 个课题分解，每个含问题/思路/机制/预期结果） | 3500 |
| `sections/05-route.md` | 技术路线与系统架构（分层图、关键数据结构、启动时序、失败恢复；mermaid 图 + 文字说明） | 2500 |
| `sections/06-eval.md` | 技术指标与评测方案（指标表逐条映射、benchmark 设计、对照基线、消融、复现） | 1500 |
| `sections/07-plan.md` | 研究计划与里程碑（12 个月，4 个季度，甘特表） | 900 |
| `sections/08-team.md` | 研究基础与团队（冯洋履历、BrewFS 工程与性能数据、团队分工、与蚂蚁的既有合作） | 1200 |
| `sections/09-deliverables.md` | 交付成果、经费预算（30 万分解表）、风险与应对、知识产权 | 1400 |

写作风格细节：
- 用 `##`/`###` 组织层级；表格用 markdown；图用 mermaid（flowchart / sequenceDiagram / gantt）
- 引用真实数据时给出处（如"2026-09-22 阿里云对齐评测"）
- 每节开头一句话点题，结尾落到"对蚂蚁的价值"
