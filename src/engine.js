import {clamp,lerp,smoothstep,makeCloud,mat4Multiply,perspective,lookAt} from './math.js';

const BACKGROUND_VERT = `#version 300 es
in vec2 aPosition;
out vec2 vUv;
void main(){vUv=aPosition*0.5+0.5;gl_Position=vec4(aPosition,0.,1.);}`;
const BACKGROUND_FRAG = `#version 300 es
precision highp float;
in vec2 vUv;uniform float uTime;uniform vec2 uResolution;out vec4 fragColor;
float randCell(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
void main(){
 vec2 uv=vUv;float aspect=uResolution.x/max(1.,uResolution.y);
 vec2 p=(uv-.5)*vec2(aspect,1.);
 float radius=length(p-vec2(.18,-.01));
 float aurora=exp(-radius*2.4);
 vec3 bg=mix(vec3(.012,.029,.052),vec3(.027,.095,.125),aurora);
 bg+=vec3(.005,.015,.024)*sin(14.*p.y+uTime*.06)*.55;
 vec2 cell=floor(uv*uResolution/vec2(3.5));
 float star=step(.9988,randCell(cell));
 float flicker=.6+.4*sin(uTime*(.3+randCell(cell+31.)*.8)+randCell(cell)*12.);
 bg+=star*flicker*vec3(.13,.3,.35);
 float vignette=1.-smoothstep(.12,1.14,length(p));
 bg*=vignette*.93+.07;
 fragColor=vec4(bg,1.);
}`;
const PARTICLES_VERT = `#version 300 es
precision highp float;
layout(location=0) in vec3 aSource;layout(location=1) in vec3 aTarget;
uniform mat4 uViewProjection;
uniform float uMorph;uniform float uTime;uniform float uMotion;
uniform float uDpr;uniform float uSize;
out float vGlow;out vec3 vTint;
void main(){
 float t=clamp(uMorph,0.,1.);
 vec3 p=mix(aSource,aTarget,t);
 float f=sin(dot(p,vec3(2.1,3.9,1.6))+uTime*.65);
 float g=cos(dot(p,vec3(3.7,-1.4,2.3))-uTime*.33);
 p+=uMotion*.045*vec3(f,g,f*g);
 vec4 projected=uViewProjection*vec4(p,1.);
 gl_Position=projected;
 float depth=max(1.,projected.w);
 gl_PointSize=clamp(uDpr*uSize*(12./depth),1.,8.);
 vGlow=.48+.52*abs(f);vTint=mix(vec3(.23,.77,.91),vec3(.88,1.,.79),t*.2+abs(g)*.36);
}`;
const PARTICLES_FRAG = `#version 300 es
precision highp float;
in float vGlow;in vec3 vTint;out vec4 fragColor;
void main(){
 vec2 p=gl_PointCoord*2.-1.;float r=dot(p,p);
 if(r>1.)discard;
 float core=pow(max(0.,1.-r),2.);
 float halo=exp(-3.*r);
 fragColor=vec4(vTint*(.48+vGlow*.72),clamp(.23*halo+.67*core,0.,1.));
}`;
function compile(gl,type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){const message=gl.getShaderInfoLog(s);gl.deleteShader(s);throw new Error('Shader compile failed: '+message);}return s;}
function createProgram(gl,v,f){const prog=gl.createProgram(),a=compile(gl,gl.VERTEX_SHADER,v),b=compile(gl,gl.FRAGMENT_SHADER,f);gl.attachShader(prog,a);gl.attachShader(prog,b);gl.linkProgram(prog);gl.deleteShader(a);gl.deleteShader(b);if(!gl.getProgramParameter(prog,gl.LINK_STATUS)){const err=gl.getProgramInfoLog(prog);gl.deleteProgram(prog);throw new Error('Program link failed: '+err);}return prog;}
export class WorldEngine {
  constructor(canvas,{onStatus=()=>{},onMetrics=()=>{},reducedMotion=false}={}){
    this.canvas=canvas;this.onStatus=onStatus;this.onMetrics=onMetrics;this.reducedMotion=reducedMotion;
    this.count=4800;this.source=makeCloud('sphere',this.count);this.target=this.source.slice();this.shape='sphere';this.morphStart=0;this.morphDuration=1350;this.morph=1;
    this.scroll=0;this.scrollTarget=0;this.pointer=[0,0];this.pixelRatio=1;this.lastTime=0;this.frames=0;this.fpsLast=0;this.fps=0;this.active=true;this.elapsed=0;
    this._frame=this.frame.bind(this);this._resize=this.resize.bind(this);
    this.init();this.resize();window.addEventListener('resize',this._resize,{passive:true});
    this.canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();this.active=false;this.onStatus('WEBGL CONTEXT LOST — WAITING TO RESTORE');});
    this.canvas.addEventListener('webglcontextrestored',()=>{try{this.init();this.active=true;this.onStatus('WEBGL CONTEXT RESTORED');requestAnimationFrame(this._frame);}catch(e){this.onStatus('RENDERER RESTORE FAILED');}});
    if(this.gl){requestAnimationFrame(this._frame);this.onStatus('WEBGL2 ONLINE / 4,800 LIVE PARTICLES');}else{this.onStatus('CSS FALLBACK / WEBGL2 UNAVAILABLE');}
  }
  init(){
    const gl=this.canvas.getContext('webgl2',{antialias:false,alpha:false,depth:false,powerPreference:'high-performance'});
    if(!gl){this.gl=null;return;}
    this.gl=gl;this.bgProgram=createProgram(gl,BACKGROUND_VERT,BACKGROUND_FRAG);this.particleProgram=createProgram(gl,PARTICLES_VERT,PARTICLES_FRAG);
    this.bgVao=gl.createVertexArray();gl.bindVertexArray(this.bgVao);const quad=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,quad);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);const pos=gl.getAttribLocation(this.bgProgram,'aPosition');gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
    this.pointVao=gl.createVertexArray();gl.bindVertexArray(this.pointVao);
    this.sourceBuffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,this.sourceBuffer);gl.bufferData(gl.ARRAY_BUFFER,this.source,gl.DYNAMIC_DRAW);gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,3,gl.FLOAT,false,0,0);
    this.targetBuffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,this.targetBuffer);gl.bufferData(gl.ARRAY_BUFFER,this.target,gl.DYNAMIC_DRAW);gl.enableVertexAttribArray(1);gl.vertexAttribPointer(1,3,gl.FLOAT,false,0,0);
    gl.bindVertexArray(null);gl.disable(gl.DEPTH_TEST);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);this.quality=1;
  }
  resize(){if(!this.gl)return;const vw=Math.max(1,window.innerWidth),vh=Math.max(1,window.innerHeight);this.pixelRatio=Math.min(window.devicePixelRatio||1,1.7)*this.quality;this.canvas.width=Math.round(vw*this.pixelRatio);this.canvas.height=Math.round(vh*this.pixelRatio);this.gl.viewport(0,0,this.canvas.width,this.canvas.height);}
  setScroll(target){this.scrollTarget=clamp(target,0,1);}
  setPointer(x,y){this.pointer=[clamp(x,-1,1),clamp(y,-1,1)];}
  setShape(next){
    if(!['sphere','torus','helix'].includes(next)||this.shape===next)return;
    const progress=this.morph;
    if(progress<1){const mid=new Float32Array(this.source.length);for(let i=0;i<mid.length;i++)mid[i]=lerp(this.source[i],this.target[i],smoothstep(progress));this.source=mid;}
    else this.source=this.target.slice();
    this.target=makeCloud(next,this.count);this.morph=0;this.morphStart=performance.now();this.shape=next;
    if(this.gl){const gl=this.gl;gl.bindBuffer(gl.ARRAY_BUFFER,this.sourceBuffer);gl.bufferSubData(gl.ARRAY_BUFFER,0,this.source);gl.bindBuffer(gl.ARRAY_BUFFER,this.targetBuffer);gl.bufferSubData(gl.ARRAY_BUFFER,0,this.target);}
  }
  frame(timestamp){
    if(!this.active||!this.gl)return;
    if(this.reducedMotion&&timestamp-this.lastTime<90){requestAnimationFrame(this._frame);return;}
    const delta=this.lastTime?Math.min(65,timestamp-this.lastTime):16.67;this.lastTime=timestamp;
    this.elapsed=this.reducedMotion?0:timestamp*.001;
    this.scroll=lerp(this.scroll,this.scrollTarget,this.reducedMotion?1:Math.min(1,delta*.004));
    this.morph=this.reducedMotion?1:clamp((timestamp-this.morphStart)/this.morphDuration,0,1);
    const gl=this.gl;gl.viewport(0,0,this.canvas.width,this.canvas.height);gl.disable(gl.BLEND);gl.useProgram(this.bgProgram);gl.bindVertexArray(this.bgVao);
    gl.uniform1f(gl.getUniformLocation(this.bgProgram,'uTime'),this.elapsed);
    gl.uniform2f(gl.getUniformLocation(this.bgProgram,'uResolution'),this.canvas.width,this.canvas.height);gl.drawArrays(gl.TRIANGLES,0,6);
    const scroll=this.scroll;const turn=scroll*Math.PI*1.23+this.pointer[0]*.13;const radius=11.7+Math.sin(scroll*Math.PI)*1.5;
    const eye=[Math.sin(turn)*radius,Math.sin(scroll*Math.PI*2)*1.1-this.pointer[1]*.4,Math.cos(turn)*radius];
    const view=lookAt(eye,[0,0,0]),proj=perspective((53+scroll*7)*Math.PI/180,Math.max(.1,this.canvas.width/this.canvas.height),.1,80);
    gl.enable(gl.BLEND);gl.useProgram(this.particleProgram);gl.bindVertexArray(this.pointVao);
    gl.uniformMatrix4fv(gl.getUniformLocation(this.particleProgram,'uViewProjection'),false,mat4Multiply(proj,view));
    gl.uniform1f(gl.getUniformLocation(this.particleProgram,'uMorph'),smoothstep(this.morph));gl.uniform1f(gl.getUniformLocation(this.particleProgram,'uTime'),this.elapsed);
    gl.uniform1f(gl.getUniformLocation(this.particleProgram,'uMotion'),this.reducedMotion?0:1);
    gl.uniform1f(gl.getUniformLocation(this.particleProgram,'uDpr'),this.pixelRatio);
    gl.uniform1f(gl.getUniformLocation(this.particleProgram,'uSize'),window.innerWidth<650?3.0:4.5);
    gl.drawArrays(gl.POINTS,0,this.count);
    this.frames++;
    if(timestamp-this.fpsLast>1100){
      this.fps=Math.round(this.frames*1000/Math.max(1,timestamp-this.fpsLast));this.frames=0;this.fpsLast=timestamp;
      if(!this.reducedMotion&&this.fps<27&&this.pixelRatio>1.05){this.quality=Math.max(.7,this.quality*.88);this.resize();}
      this.onMetrics({renderer:'WebGL2',particles:this.count,fps:this.fps,dpr:Number(this.pixelRatio.toFixed(2)),shape:this.shape});
    }
    requestAnimationFrame(this._frame);
  }
  destroy(){this.active=false;window.removeEventListener('resize',this._resize);if(this.gl){for(const b of [this.sourceBuffer,this.targetBuffer])this.gl.deleteBuffer(b);this.gl.deleteProgram(this.bgProgram);this.gl.deleteProgram(this.particleProgram);}}
}
