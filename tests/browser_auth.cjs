// Browser integration: stub only Google OAuth, exercise real app HTTP, cookies, JS and FalkorDB.
// Run with NODE_PATH pointing to a Playwright installation.
const {chromium} = require('playwright');
const {spawn, spawnSync} = require('node:child_process');
const assert = require('node:assert/strict');
const uid = 'browser-auth-' + Date.now();
const env = {...process.env, AUTH_MODE:'firebase', APP_ENV:'development', PROFILE_STORE:'falkordb', AI_ENABLED:'false', BROWSER_TEST_UID:uid};
const python = '.venv/bin/python';
const server = spawn(python, ['-c', `
import os
from types import SimpleNamespace
from app.ui import router

def verify(token):
    if token != 'browser-test-token':
        raise ValueError('Invalid test token')
    return {'uid':os.environ['BROWSER_TEST_UID'],'name':'Browser Tester','email':'browser-test@example.invalid'}
router.firebase_auth=lambda:SimpleNamespace(verify_id_token=verify)
import uvicorn
uvicorn.run('app.main:app',host='127.0.0.1',port=8017,log_level='warning')
`], {env, stdio:['ignore','pipe','pipe']});
let logs='';server.stderr.on('data',x=>logs+=x);
let browser;
(async()=>{
  for(let i=0;i<100;i++) {try {if((await fetch('http://127.0.0.1:8017/')).ok)break;}catch{} await new Promise(r=>setTimeout(r,200));}
  browser=await chromium.launch({headless:true,channel:'chrome'});
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  await context.route('https://www.gstatic.com/firebasejs/**/firebase-app.js',route=>route.fulfill({contentType:'text/javascript',body:'export const initializeApp=x=>x;'}));
  await context.route('https://www.gstatic.com/firebasejs/**/firebase-auth.js',route=>route.fulfill({contentType:'text/javascript',body:`export const getAuth=()=>({}); export const inMemoryPersistence={};export const setPersistence=async()=>{};export class GoogleAuthProvider{};export const signInWithPopup=async()=>{if(window.__oauthError)throw {code:'auth/popup-blocked'};return {user:{getIdToken:async()=>'browser-test-token'}}};export const signOut=async()=>{};`}));
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8017/');
  await page.screenshot({path:'/tmp/studyspace-landing.png',fullPage:true});
  await page.getByRole('link',{name:'Build my study space'}).click();
  await page.getByRole('button',{name:'Continue with Google'}).click();
  await page.waitForURL('**/onboarding');
  await page.locator('#full-name').fill('Browser Tester');
  await page.locator('#name').fill('Alex');
  await page.locator('#role').selectOption('student');
  await page.locator('#industry').selectOption('Technology');
  await page.locator('#interest').fill('Mathematics');
  await page.screenshot({path:'/tmp/studyspace-onboarding.png',fullPage:true});
  await page.getByRole('button',{name:'Build my study space'}).click();
  await page.waitForURL('**/agent');
  await page.getByText('Hi, Alex',{exact:false}).waitFor();
  await page.locator('#subject option').first().waitFor({state:'attached'});
  await page.screenshot({path:'/tmp/studyspace-dashboard.png',fullPage:true});
  await page.locator('#goal').fill('I want to learn logic and quantifiers');
  await page.getByRole('button',{name:'Ask the agent',exact:true}).click();
  await page.getByRole('button',{name:'Approve this plan',exact:true}).click();
  await page.getByRole('link',{name:'Continue learning'}).waitFor();
  await page.screenshot({path:'/tmp/studyspace-saved-plans.png',fullPage:true});
  await page.getByRole('link',{name:'Continue learning'}).click();
  await page.getByRole('button',{name:'Mark as studied'}).click();
  await page.waitForURL('**/agent');
  await page.getByText('You’ve studied every lesson in your saved plans.',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL('**/login');
  await page.evaluate(()=>window.__oauthError=true);
  await page.getByRole('button',{name:'Continue with Google'}).click();
  await page.getByText('Your browser blocked the sign-in window.',{exact:false}).waitFor();
  assert(await page.getByRole('button',{name:'Continue with Google'}).isEnabled());
  await page.evaluate(()=>window.__oauthError=false);
  await page.getByRole('button',{name:'Continue with Google'}).click();
  await page.waitForURL('**/agent');
  await page.getByText('Welcome back, Alex',{exact:false}).waitFor();
  await page.getByRole('link',{name:'Edit profile'}).click();
  assert.equal(await page.locator('#name').inputValue(),'Alex');
  await page.locator('#name').fill('Lex');
  await page.getByRole('button',{name:'Save changes'}).click();
  await page.waitForURL('**/agent');
  await page.getByText('Welcome back, Lex',{exact:false}).waitFor();
  await page.setViewportSize({width:390,height:844});
  await page.goto('http://127.0.0.1:8017/onboarding?edit=1');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile profile overflows');
  assert.deepEqual(errors,[], 'Browser JavaScript errors');
  console.log('PASS: landing, Google callback, onboarding save, dashboard, logout, returning sign-in, edit profile, plan approval, continue lesson, completion persistence, blocked-popup recovery, mobile layout; no browser JS errors.');
})().catch(e=>{console.error(e);console.error(logs);process.exitCode=1}).finally(async()=>{
  if(browser)await browser.close();
  server.kill();
  spawnSync(python,['-c',`from app.learn.state import reset_learner; from app.kg.connection import student_graph; reset_learner('${uid}'); student_graph().query('MATCH (l:Learner {uid:$uid}) DETACH DELETE l',{'uid':'${uid}'})`],{env});
});
