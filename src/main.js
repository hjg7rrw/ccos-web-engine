import {WorldEngine} from './engine.js';
import {WORLD_DESCRIPTIONS,SHAPE_ORDER} from './data.js';
import {clamp} from './math.js';

const $=selector=>document.querySelector(selector);
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const canvas=$('#universe');
let previousSection='origin';let manuallyChosen=false;let engine;
function setStatus(message){$('#render-status').textContent=message;}
function updateMetrics(data){$('#diag-renderer').textContent=data.renderer;$('#diag-particles').textContent=data.particles.toLocaleString();$('#diag-fps').textContent=data.fps;$('#diag-dpr').textContent=data.dpr;$('#diag-shape').textContent=data.shape.toUpperCase();}
try{engine=new WorldEngine(canvas,{onStatus:setStatus,onMetrics:updateMetrics,reducedMotion});}
catch(error){console.error('Renderer unavailable:',error);setStatus('3D UNAVAILABLE / CONTENT REMAINS ACCESSIBLE');}
function choose(shape){if(!SHAPE_ORDER.includes(shape))return;engine?.setShape(shape);document.querySelectorAll('[data-shape]').forEach(button=>{const isActive=button.dataset.shape===shape;button.classList.toggle('is-active',isActive);button.setAttribute('aria-pressed',String(isActive));});$('#world-description').textContent=WORLD_DESCRIPTIONS[shape];}
document.querySelectorAll('[data-shape]').forEach(button=>button.addEventListener('click',()=>{manuallyChosen=true;choose(button.dataset.shape);}));
$('#trigger-morph').addEventListener('click',()=>{const ix=SHAPE_ORDER.indexOf(engine?.shape||'sphere');choose(SHAPE_ORDER[(ix+1)%SHAPE_ORDER.length]);});
$('#quality').addEventListener('click',()=>{const diag=$('#diag'),open=diag.hidden;diag.hidden=!open;$('#quality').setAttribute('aria-expanded',String(open));$('#quality-label').textContent=open?'LIVE':'AUTO';});
function scrollState(){const sections=[...document.querySelectorAll('.chapter')];const max=Math.max(1,document.documentElement.scrollHeight-window.innerHeight);const position=clamp(window.scrollY/max,0,1);engine?.setScroll(position);
 let closest=null,best=Infinity;for(const s of sections){const r=s.getBoundingClientRect(),dist=Math.abs((r.top+r.height/2)-window.innerHeight/2);if(dist<best){best=dist;closest=s.dataset.world;}}
 if(closest&&closest!==previousSection){previousSection=closest;if(closest==='origin'){manuallyChosen=false;choose('sphere');}if(closest==='signal'){manuallyChosen=false;choose('helix');}if(closest==='worlds'&&!manuallyChosen)choose('torus');}
}
window.addEventListener('scroll',scrollState,{passive:true});window.addEventListener('resize',scrollState,{passive:true});
window.addEventListener('pointermove',event=>{engine?.setPointer(2*event.clientX/Math.max(1,window.innerWidth)-1,1-2*event.clientY/Math.max(1,window.innerHeight));},{passive:true});
window.addEventListener('pagehide',()=>engine?.destroy(),{once:true});
scrollState();
if(reducedMotion)setStatus('REDUCED-MOTION MODE / INTERACTIONS ENABLED');
