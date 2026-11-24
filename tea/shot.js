const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
const D='file://'+process.argv[2]+'/';
for(const f of ['m8s.html','tea.html']){await p.goto(D+f);await p.waitForTimeout(400);await p.screenshot({path:'tea/s-'+f+'.png',clip:{x:0,y:0,width:1280,height:260}});}
for(const h of ['p1','p2','p4']){await p.goto(D+'tea-guide.html#'+h);await p.waitForTimeout(500);
 await p.screenshot({path:`tea/g-${h}.png`,fullPage:true});
 console.log(h,await p.evaluate(()=>{const v=[...document.querySelectorAll('.panel')].find(x=>!x.hidden);return [...v.querySelectorAll('.bh')].map(x=>x.textContent).join('/')+' rows:'+v.querySelectorAll('table.tline tbody tr').length}));}
await p.click('[data-go="p4-b3"]');await p.waitForTimeout(600);console.log('hash',await p.evaluate(()=>location.hash+' '+scrollY));
console.log('errs',errs);await b.close()})();
