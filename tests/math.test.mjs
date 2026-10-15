import test from 'node:test';import assert from 'node:assert/strict';
import {clamp,lerp,smoothstep,sampleShape,makeCloud,lookAt,mat4Multiply,perspective} from '../src/math.js';
test('clamp and interpolation boundaries',()=>{assert.equal(clamp(2,0,1),1);assert.equal(lerp(0,10,.3),3);assert.equal(smoothstep(-2),0);assert.equal(smoothstep(2),1);assert.equal(smoothstep(.5),.5);});
test('deterministic geometry for three original shapes',()=>{for(const s of ['sphere','torus','helix']){const p=makeCloud(s,500);assert.equal(p.length,1500);assert.ok(p.every(Number.isFinite));assert.deepEqual(p,makeCloud(s,500));assert.ok(sampleShape(s,23,500).every(Number.isFinite));}});
test('invalid geometry rejected',()=>assert.throws(()=>makeCloud('nonsense',20),/Unknown shape/));
test('projection matrices are finite and proper size',()=>{const view=lookAt([0,1,10],[0,0,0]),proj=perspective(Math.PI/3,16/9,.1,100),m=mat4Multiply(proj,view);assert.equal(m.length,16);assert.ok(m.every(Number.isFinite));assert.equal(view[15],1);});
