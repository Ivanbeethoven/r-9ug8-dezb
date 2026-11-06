const fs=require('fs');
const flow=`flowchart TB
    subgraph CTRL["控制面"]
        C["蚂蚁管控面 / K8s"] --> S["沙箱调度 / containerd"]
    end
    subgraph EXE["执行面：runD guest（进程 / 网络 / 权限隔离）"]
        R["runD 启动 / 恢复"] --> W["workspace overlay<br/>packed lower + 私有 upper"]
        L["Nydus EROFS 镜像层"] --> W
        W --> F["BrewFS FUSE"]
    end
    subgraph DATA["数据面：BrewFS"]
        V["VFS"] --> M["元数据事务"]
        M --> B[("元数据后端<br/>Redis / TiKV")]
        M --> H["多级缓存 / 写回"] --> O[("OSS")]
    end
    S --> R
    F --> V
`;
(async()=>{
   const enc=Buffer.from(flow,'utf8').toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
   const r=await fetch('https://mermaid.ink/img/'+enc+'?bgColor=FFFFFF&width=1800');
   const b=Buffer.from(await r.arrayBuffer()); fs.writeFileSync('figures_test/flow3.png',b);
   console.log('ok',r.status,b.length);
})();
