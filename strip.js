
const fs=require('fs');const [src,out,mode]=process.argv.slice(2);
let text=fs.readFileSync(src,'utf8');
const a=text.indexOf('const data = [');const b=text.indexOf('\n];',a)+3;
eval(text.slice(a,b).replace('const data','global.data'));
for(const g of data){ if(mode==='strip'){delete g.rules;delete g.warn;}
  for(const r of g.rows){ if(mode!=='strip')continue;
    r.c=[];for(const k of ['st','mt','n','nst','pos','press','poi','tp'])delete r[k];}}
const ser=v=>{if(Array.isArray(v))return '['+v.map(ser).join(',')+']';if(v&&typeof v==='object')return '{'+Object.entries(v).map(([k,x])=>k+':'+ser(x)).join(',')+'}';return JSON.stringify(v)};
fs.writeFileSync(out,'const data = [\n'+data.map(g=>{const {rows,...h}=g;return ser(h).slice(0,-1)+(Object.keys(h).length?', ':'')+'rows:[\n'+rows.map(r=>'  '+ser(r)).join(',\n')+'\n]}'}).join(',\n')+'\n];\n');
