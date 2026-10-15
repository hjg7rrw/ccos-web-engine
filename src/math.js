export function clamp(n,min,max){return Math.min(max,Math.max(min,n));}
export function smoothstep(t){const x=clamp(t,0,1);return x*x*(3-2*x);}
export function lerp(a,b,t){return a+(b-a)*t;}
export function seedNoise(v){let x=v|0;x^=x>>>16;x=Math.imul(x,0x7feb352d);x^=x>>>15;x=Math.imul(x,0x846ca68b);return ((x^(x>>>16))>>>0)/4294967296;}
export function sampleShape(which,i,total){
  const u=(i+.5)/total,v=seedNoise(i*17+93),w=seedNoise(i*37+185);const angle=2*Math.PI*u;
  if(which==='sphere'){
    const z=1-2*u,phi=angle*1.61803398875*total*0.1375;const r=Math.sqrt(Math.max(0,1-z*z));
    return [2.65*r*Math.cos(phi),2.65*z,2.65*r*Math.sin(phi)];
  }
  if(which==='torus'){
    const a=2*Math.PI*seedNoise(i*23+31),b=2*Math.PI*seedNoise(i*47+73);const R=2.2+0.17*Math.sin(a*3),r=.88;
    return [(R+r*Math.cos(b))*Math.cos(a),(R+r*Math.cos(b))*Math.sin(a),r*Math.sin(b)];
  }
  if(which==='helix'){
    const a=u*Math.PI*12+2*Math.PI*v*.15,rad=1.25+.65*w;
    return [rad*Math.cos(a),5.7*(u-.5),rad*Math.sin(a)];
  }
  throw new Error('Unknown shape: '+which);
}
export function makeCloud(shape,count){const v=new Float32Array(count*3);for(let i=0;i<count;i++){const p=sampleShape(shape,i,count);v.set(p,i*3);}return v;}
export function mat4Multiply(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)o[c*4+r]=a[r]*b[c*4]+a[4+r]*b[c*4+1]+a[8+r]*b[c*4+2]+a[12+r]*b[c*4+3];return o;}
export function perspective(fovy,aspect,near,far){const f=1/Math.tan(fovy/2),o=new Float32Array(16);o[0]=f/aspect;o[5]=f;o[10]=(far+near)/(near-far);o[11]=-1;o[14]=2*far*near/(near-far);return o;}
export function lookAt(eye,target,up=[0,1,0]){
  const norm=v=>{const l=Math.hypot(...v)||1;return v.map(n=>n/l);};
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const z=norm(eye.map((x,i)=>x-target[i])),x=norm(cross(up,z)),y=cross(z,x);
  return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-x.reduce((s,v,i)=>s+v*eye[i],0),-y.reduce((s,v,i)=>s+v*eye[i],0),-z.reduce((s,v,i)=>s+v*eye[i],0),1]);
}
