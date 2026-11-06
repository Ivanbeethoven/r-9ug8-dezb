const fs=require('fs');
const t=fs.readFileSync('proposal.md','utf8');
const blocks=[...t.matchAll(/```mermaid([\s\S]*?)```/g)].map(m=>m[1].trim());
console.log('blocks',blocks.length, JSON.stringify(blocks.map(b=>b.split('\n')[0])));
fs.mkdirSync('figures_test',{recursive:true});
(async()=>{
 for(let i=0;i<blocks.length;i++){
   const enc=Buffer.from(blocks[i],'utf8').toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
   try{
     const r=await fetch('https://mermaid.ink/img/'+enc+'?bgColor=FFFFFF&width=1800');
     if(!r.ok){console.log(i+1,'HTTP',r.status,(await r.text()).slice(0,150));continue;}
     const b=Buffer.from(await r.arrayBuffer());
     fs.writeFileSync('figures_test/m'+(i+1)+'.png',b);
     console.log(i+1,'ok',b.length,'bytes');
   }catch(e){console.log(i+1,'ERR',e.message);}
 }
})();
