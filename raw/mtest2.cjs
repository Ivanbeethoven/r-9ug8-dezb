const fs=require('fs');
const flow=`flowchart TB
    C["蚂蚁管控面 / K8s"] --> S["沙箱调度 / containerd"]
    subgraph EXE["执行面：runD guest（进程 / 网络 / 权限边界）"]
        R["runD 启动 / 恢复"]
        W["workspace overlay"]
        L["Nydus EROFS 镜像层<br/>不可变 packed lower"]
        U["私有可写 upper"]
        F["BrewFS FUSE"]
        L --> W
        U --> W
        W --> F
        R --> W
    end
    S --> R
    subgraph DATA["数据面：BrewFS（文件视图与版本事务）"]
        V["VFS"] --> M["元数据事务"]
        M --> H["多级缓存 / 写回 staging"]
        M --> B["元数据后端：Redis / TiKV"]
    end
    F --> V
    H --> O[("OSS")]
`;
const tl=`timeline
    title 项目里程碑：2027-02 至 2028-01
    section Q1 格式对齐
        2027-02 至 04 : 格式与接口规范 v1 : 兼容矩阵与三类镜像基线 : lazyload 挂载与增量 fork 演示
    section Q2 原型
        2027-05 至 07 : 原型 v0.1 : 冷启动与 C/R 可重复脚本 : 中期报告与初测分布
    section Q3 联调
        2027-08 至 10 : 联调版本 v0.2 : 100 并发长尾定位 : 消融与跨环境复测
    section Q4 收敛与结题
        2027-11 至 2028-01 : 原型 v1.0 : 三项指标验收包 : 论文与专利申请材料
`;
(async()=>{
 for(const [n,src] of [['flow2',flow],['timeline',tl]]){
   const enc=Buffer.from(src,'utf8').toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
   const r=await fetch('https://mermaid.ink/img/'+enc+'?bgColor=FFFFFF&width=1800');
   if(!r.ok){console.log(n,'HTTP',r.status,(await r.text()).slice(0,200));continue;}
   const b=Buffer.from(await r.arrayBuffer()); fs.writeFileSync('figures_test/'+n+'.png',b);
   console.log(n,'ok',b.length);
 }
})();
