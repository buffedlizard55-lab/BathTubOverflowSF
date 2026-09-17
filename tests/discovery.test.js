import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const raw = readFileSync(new URL('../data/research.json', import.meta.url));
const old = JSON.parse(raw);
const wave = JSON.parse(readFileSync(new URL('../data/wave17.json', import.meta.url)));
const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const core = s => norm(s.toLowerCase().replace(/\b(inc|incorporated|llc|co|company|corp|corporation|construction|contractor|contractors|general)\b/g, ''));
test('wave 17 pass 1: every retained registry field has a source transcription', () => {
  assert.equal(wave.entries.length, 50);
  assert.equal(wave.sourceTranscription.length, 52);
  assert.equal(wave.checkedAt, '2026-09-17');
  const pairs = new Set(wave.sourceTranscription.map(r => JSON.stringify([r.firm_name, r.license1])));
  for (const b of wave.entries) {
    assert.ok(pairs.has(JSON.stringify([b.name, b.registryLicenseNumber])), b.id);
    assert.deepEqual(b.observedFields, {firm_name:b.name,license1:b.registryLicenseNumber});
    for (const id of [b.source, b.crosscheckSource]) assert.ok(wave.sources.some(s => s.id === id));
  }
  for (const s of wave.sources) {
    assert.equal(new URL(s.url).hostname, 'data.sf.gov');
    assert.equal(s.access, 'page');
  }
});
test('wave 17 pass 2: no known ID, name, core or registry-number collision', () => {
  const names = new Set(old.businesses.map(b => norm(b.name)));
  const cores = new Set(old.businesses.map(b => core(b.name)));
  const ids = new Set(old.businesses.map(b => b.id));
  // Search the full existing corpus, not just its structured licence objects.
  const numbers = new Set(raw.toString().match(/\b\d{5,7}\b/g));
  for (const b of wave.entries) {
    assert.ok(!names.has(norm(b.name)), b.name);
    assert.ok(!cores.has(core(b.name)), b.name);
    assert.ok(!ids.has(b.id), b.id);
    assert.ok(!numbers.has(b.registryLicenseNumber), b.id);
    names.add(norm(b.name)); cores.add(core(b.name)); ids.add(b.id); numbers.add(b.registryLicenseNumber);
  }
});
test('wave 17 pass 3: fail closed, leave prior corpus and master untouched', () => {
  assert.equal(createHash('sha256').update(raw).digest('hex'), wave.baselineSha256);
  assert.equal(old.master.length, 0);
  assert.equal(old.businesses.length, 793);
  assert.equal(wave.stage, 'discovery-only');
  for (const b of wave.entries) {
    assert.equal(b.master, false);
    assert.equal(b.status, 'hold');
    assert.equal(b.reviews.length, 0);
    assert.equal(Object.keys(b.requirements).length, 8);
    assert.ok(Object.values(b.requirements).every(v => v === 'unconfirmed'));
    assert.ok(b.flags.length >= 2);
  }
  const checks = wave.entries.filter(b => b.licenseCheck);
  assert.equal(checks.length, 4);
  assert.equal(checks.filter(b => b.licenseCheck.status === 'active').length, 3);
  assert.equal(checks.filter(b => b.licenseCheck.status === 'suspended').length, 1);
  for (const b of checks) {
    assert.equal(b.licenseCheck.number, b.registryLicenseNumber);
    assert.equal(new URL(b.licenseCheck.url).searchParams.get('LicNum'), b.registryLicenseNumber);
    assert.deepEqual(b.licenseCheck.classes, ['B']);
    assert.equal(b.licenseCheck.checkedAt, wave.checkedAt);
  }
});
