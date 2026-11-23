import { chromium } from 'playwright';
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const base = process.env.NOVA_URL || 'http://localhost:3212';
const out = path.resolve('deliverables');
await mkdir(path.join(out,'screenshots'),{recursive:true});
const browser = await chromium.launch({headless:true, args:['--use-angle=swiftshader','--enable-webgl']});
const page = await browser.newPage({viewport:{width:1440,height:1100},reducedMotion:'reduce'});
const errors=[]; page.on('pageerror',e=>errors.push(e.message));
const screenshot = async name => page.screenshot({path:path.join(out,'screenshots',name+'.png'),fullPage:true});
const valid={pilotName:'Ace',age:'25',email:'a@b.com',mobile:'09171234567'};
const cases=[
 {id:1,data:{...valid,pilotName:''},field:'pilotName',expected:'Every pilot needs a callsign (3 to 20 characters)!'},
 {id:2,data:{...valid,age:'17'},field:'age',expected:'Pilots must be 18 to 60 years old.'},
 {id:3,data:{...valid,age:'61'},field:'age',expected:'Pilots must be 18 to 60 years old.'},
 {id:4,data:{...valid,email:'banana'},field:'email',expected:'That email is lost in space.'},
 {id:5,data:{...valid,mobile:''},field:'mobile',expected:'Please enter a valid mobile number.'},
 {id:6,data:{...valid,age:''},field:'age',expected:'Please enter your age.'},
 {id:7,data:{...valid,pilotName:'Captain Zoomzoom Starfighter'},field:'pilotName',expected:'Every pilot needs a callsign (3 to 20 characters)!'},
 {id:8,data:{...valid,pilotName:'Nova',age:'30',email:'nova@academy.edu'},expected:'Welcome aboard, Nova!'}
];
const fill=async data=>{for(const [key,value] of Object.entries(data))await page.locator('#'+key).fill(value);};
await page.goto(base); await page.evaluate(()=>document.fonts.ready); await screenshot('00_desktop');
assert.equal(await page.locator('.orbit-canvas canvas').count(),1,'Three.js canvas is present');
for(const item of cases){
 await page.goto(base); await fill(item.data); await page.getByRole('button',{name:'Request boarding clearance'}).click();
 const locator=item.field?page.locator('#'+item.field+'-error'):page.getByRole('status');
 await locator.waitFor(); const actual=item.field?await locator.innerText():await locator.locator('strong').innerText();
 assert.equal(actual,item.expected); item.actual=actual; item.pass=true;
 if(item.field){assert.equal(await page.locator('#'+item.field).getAttribute('aria-invalid'),'true'); assert.equal(await page.locator('#'+item.field).evaluate(el=>el===document.activeElement),true); if(item.field!=='email') assert.equal(await page.locator('#email').inputValue(),item.data.email);}
 else {for(const key of Object.keys(item.data)) assert.equal(await page.locator('#'+key).inputValue(),''); await screenshot('05_success');}
 const api=await page.request.post(base+'/api/pilots',{headers:{Origin:base},data:item.data}); assert.equal(api.status(),item.field?422:200); item.serverStatus=api.status();
}
await page.goto(base); await page.getByRole('button',{name:'Request boarding clearance'}).click();
assert.equal(await page.locator('.field-error').count(),4); await screenshot('04_multiple_errors');
await page.goto(base); await fill(valid); await page.getByRole('button',{name:/Plan your launch/}).click(); await page.locator('#launchDate').fill('2000-01-01'); await page.getByRole('button',{name:'Request boarding clearance'}).click();
assert.equal(await page.locator('#launchDate-error').innerText(),'You cannot launch yesterday!'); await screenshot('06_launch_date_error');
const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Manila',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
await page.locator('#launchDate').fill(today); await page.getByRole('button',{name:'Request boarding clearance'}).click(); await page.getByRole('status').waitFor();
const extra=[];
for(const [name,options,status] of [
 ['missing origin',{data:valid},403],
 ['cross origin',{headers:{Origin:'https://other.example'},data:valid},403],
 ['malformed JSON',{headers:{Origin:base,'Content-Type':'application/json'},data:Buffer.from('{')},400],
 ['wrong content type',{headers:{Origin:base,'Content-Type':'text/plain'},data:'hi'},415],
 ['oversized body',{headers:{Origin:base},data:{pilotName:'x'.repeat(9000)}},413]
]){const result=await page.request.post(base+'/api/pilots',options);assert.equal(result.status(),status,name);extra.push({name,expected:status,actual:result.status(),pass:true});}
assert.equal((await page.request.get(base+'/api/pilots')).status(),405);
await page.goto(base); await fill(valid); await page.route('**/api/pilots',route=>route.abort()); await page.getByRole('button',{name:'Request boarding clearance'}).click(); await page.waitForFunction(() => document.querySelector('.error-summary')?.textContent?.includes('could not reach')); assert.match(await page.locator('.error-summary').innerText(),/could not reach/);assert.equal(await page.locator('#pilotName').inputValue(),'Ace'); await page.unroute('**/api/pilots');
for(const checkpoint of ['model','controller','view']){
 await page.goto(base+'/lab/'+checkpoint); await page.locator('pre').waitFor();
 // Keep source wrapping readable in checkpoint evidence; text/line numbers are unchanged.
 await page.addStyleTag({content:'.code-panel pre{white-space:pre-wrap}.code-line{overflow-wrap:anywhere}'});
 await screenshot('0'+(['model','controller','view'].indexOf(checkpoint)+1)+'_'+checkpoint+'_source');
}
await page.setViewportSize({width:390,height:844}); await page.goto(base); await page.evaluate(()=>document.fonts.ready); assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await screenshot('07_mobile');
await page.getByRole('button',{name:'Request boarding clearance'}).click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
await page.setViewportSize({width:320,height:800});await page.goto(base); assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
assert.equal(errors.length,0,errors.join('\n'));
// Destructive worksheet experiments are executed in isolated test copies only.
const source=await readFile('lib/pilot.ts','utf8'); const target=' || Number(ageText) < 18 || Number(ageText) > 60'; assert.ok(source.includes(target));
await mkdir('artifacts/qa',{recursive:true});await writeFile('artifacts/qa/pilot-no-range.ts',source.replace(target,''));
const mutant=await import(pathToFileURL(path.resolve('artifacts/qa/pilot-no-range.ts')).href);
assert.equal(mutant.validatePilot({...valid,age:'5'}).ok,true);
const {validatePilot}=await import(pathToFileURL(path.resolve('lib/pilot.ts')).href);
assert.equal(validatePilot({...valid,age:'5'}).ok,false);
function brokenSuccessBranch(raw){const validation=validatePilot(raw); return {validation,ok:true,message:`Welcome aboard, ${raw.pilotName||''}!`};}
const unsafe=brokenSuccessBranch({}); assert.equal(unsafe.validation.ok,false); assert.equal(unsafe.ok,true);
const report={date:new Date().toISOString(),url:base,cases,additional:extra,checks:{worksheetUI:8,worksheetAPI:8,threeCanvas:true,emptyErrors:4,firstErrorFocus:true,preservedInvalidValues:true,successClearsForm:true,launchYesterdayRejected:true,launchTodayAccepted:true,networkFailurePreservesInput:true,mobile390And320NoOverflow:true,reducedMotion:true,pageErrors:errors},experiments:[{name:'Remove the age range in an isolated validator copy',input:{...valid,age:'5'},actual:'Accepted age 5 after removing the range; original validator rejects it.',pass:true},{name:'Ignore the validation result in an isolated success-branch harness',input:{},actual:'Blank data produced Welcome aboard, ! despite validation.ok being false.',pass:true}],scope:'Executed in local Chromium against production Next.js. Break-it experiments use isolated copies/harness; live validation remains enabled. No real registration is stored.'};
await writeFile(path.join(out,'TEST_RESULTS.json'),JSON.stringify(report,null,2));
await browser.close();console.log(JSON.stringify(report,null,2));
