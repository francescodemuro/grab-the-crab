const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const output = path.resolve(process.env.GTC_BROWSER_OUTPUT || 'artifacts/browser');
fs.mkdirSync(output, {recursive:true});
(async () => {
 const browser = await chromium.launch({headless:true});
 const context = await browser.newContext({viewport:{width:1800,height:1080},acceptDownloads:true});
 const errors=[], external=[];
 const page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await context.route('**/*',route=>{
  if(!route.request().url().startsWith('http://127.0.0.1:8000/')){
   external.push(route.request().url()); return route.abort();
  }
  return route.continue();
 });
 await page.goto('http://127.0.0.1:8000/');
 await page.waitForFunction(()=>state.data?.case?.case_id==='incident_079');
 if(await page.locator('#case-select option').count()!==100)throw Error('Frozen case count');
 if(await page.locator('#online-map-toggle').isChecked())throw Error('Online imagery enabled by default');
 async function followRecommendation(){
  const button=page.locator('#follow-marine-btn');
  if(await button.isEnabled())await button.click();
  const aligned=await page.evaluate(()=>{const top=state.data.global_recommendations[0]; return state.selectedSite===top.site_id && state.selectedEffort===Number(top.recommended_effort);});
  if(!aligned)throw Error('Operator selection did not follow the recommendation');
 }
 for(let i=0;i<3;i++){
  await followRecommendation();
  await page.locator('#deploy-btn').click();
  await page.waitForFunction(()=>!state.busy && state.data.resources.round>0);
 }
 const middle = await page.evaluate(()=>({round:state.data.resources.round,changed:state.data.mission_changed,spent:state.data.resources.spent_budget}));
 if(middle.round!==3 || middle.spent!==15 || !middle.changed)throw Error('Default evidence-driven replan did not reproduce '+JSON.stringify(middle));
 await page.screenshot({path:path.join(output, 'evaluation-demo.png'),fullPage:true});
 for(let i=0;i<3;i++){
  await followRecommendation();
  await page.locator('#deploy-btn').click();
  await page.waitForFunction(()=>!state.busy);
 }
 await page.locator('#reveal-btn').click();
 await page.waitForFunction(()=>!state.busy && state.data.revealed);
 const downloadP=page.waitForEvent('download');
 await page.locator('.receipt-download').click();
 const download=await downloadP;
 const receiptPath=path.join(output, 'decision-receipt.json');
 await download.saveAs(receiptPath);
 const receipt=JSON.parse(fs.readFileSync(receiptPath,'utf8'));
 if(receipt.state.resources.spent_budget!==18 || !receipt.state.revealed)throw Error('Invalid exported receipt');
 const second=await browser.newContext({viewport:{width:1440,height:900}});
 const other=await second.newPage(); await other.goto('http://127.0.0.1:8000/');
 await other.waitForFunction(()=>state.data?.resources.round===0);
 const mobile=await browser.newContext({viewport:{width:390,height:844}});
 const mp=await mobile.newPage(); await mp.goto('http://127.0.0.1:8000/');
 await mp.waitForFunction(()=>state.data?.case?.case_id==='incident_079');
 const overflow=await mp.evaluate(()=>({width:window.innerWidth,scroll:document.documentElement.scrollWidth}));
 await mp.screenshot({path:path.join(output, 'mobile-check.png'),fullPage:true});
 if(external.length || errors.length)throw Error(JSON.stringify({external,errors}));
 console.log(JSON.stringify({browser:'Chromium',externalRequests:external.length,javascriptErrors:errors.length,
  defaultReplan:middle,completedMissions:receipt.state.resources.round,effortSpent:18,
  receiptDownloaded:true,separateBrowserSession:true,mobile:overflow}));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
