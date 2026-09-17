import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const raw = readFileSync(new URL('../data/research.json', import.meta.url));
const old = JSON.parse(raw);
const w17 = JSON.parse(readFileSync(new URL('../data/wave17.json', import.meta.url)));
const w18 = JSON.parse(readFileSync(new URL('../data/wave18.json', import.meta.url)));
const wave = JSON.parse(readFileSync(new URL('../data/wave19.json', import.meta.url)));
const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const core = s => norm(s.toLowerCase().replace(/\b(inc|incorporated|llc|co|company|corp|corporation|construction|contractor|contractors|general)\b/g, ''));
const sourceIds = new Set(wave.sources.map(s => s.id));
const registry = wave.entries.filter(b => b.registryLicenseNumber);
const platform = wave.entries.filter(b => b.trade === 'platform-lead');
const checks = wave.entries.filter(b => b.licenseCheck);

// Same one-way private-context fingerprints as tests/research.test.js. They let
// the public repository test every artifact without restating excluded details.
const privateMarkerDigests = new Set([
  "710cdcb6c633b8993d8a341d73f247282495408c2a12cc797c8006bc327464a8",
  "bea6c284fb02b5d0aa611eb727ee69cdfa283f832f667cc45edb395d9510841f",
  "510d3a4233002578d42ac8558c5324d8ffbd34ab0e08eb0b2a2c00485f77a361",
  "ae2785f2d5d577ecc622fecffaec531fd1687d55c347569fe805bf27af17c47e",
  "66f4a7521f5a2a3b0b21c97c9fd4e28c0564fbe5b75ae3ce316b4d157dd55bfc",
  "9903c83e316d8a40f84bc00adf967aa5caa0e58bec37584e45cf16b97edcd317",
  "cf109ac20d0a56c95192a248efbe6bc41c16113928b786d8588830efbb79f5d6",
  "4c2733abf54ccb0f418600316449c0a3d7bfe21de1894dae833860be7f5f3434",
  "bcbb4b2505d42b71121ea904ec141a825e4f3fd90d4f694d5b81e4a3f77a07e1",
  "7cca84535e81d2d1d7a838c892dac1d7ba7d409313d44810b742b8192a63bb1d",
  "8f53059107c1aca3174b4a75a6b8f520653b0fa5e2180b2121ddb4bd59a1e4ea",
  "2c7f437a907912af18e334413020d366916094f724ec3159f823470ad701cfd4",
  "57a8ef6d2c7995352c6a74233741e7bef6c1113782966662a8eccb586d7356d3",
  "e9f172ce2a0beb97843f2a5b9aab9978d9a956a23606da206789ec714d98efa0",
]);
const digest = value => createHash('sha256').update(value).digest('hex');
function assertPrivacySafe(value, label) {
  const words = value.toLowerCase().match(/[a-z0-9]+/g) || [];
  for (let width = 1; width <= 4; width += 1)
    for (let i = 0; i + width <= words.length; i += 1)
      assert.equal(
        privateMarkerDigests.has(digest(words.slice(i, i + width).join(' '))),
        false,
        `${label} contains an excluded private-context marker`,
      );
}

test('wave 19 pass 1: every retained registry field has a source transcription', () => {
  assert.equal(wave.entries.length, 50);
  assert.equal(registry.length, 43);
  assert.equal(platform.length, 7);
  assert.equal(wave.sourceTranscription.length, 43);
  assert.equal(wave.checkedAt, '2026-09-17');
  const pairs = new Set(wave.sourceTranscription.map(r => JSON.stringify([r.firm_name, r.license])));
  for (const b of registry) {
    assert.ok(pairs.has(JSON.stringify([b.name, b.registryLicenseNumber])), b.id);
    assert.equal(b.observedFields.firm_name, b.name, b.id);
    const lic = b.observedFields.license1 ?? b.observedFields.license_number;
    assert.equal(lic, b.registryLicenseNumber, b.id);
    for (const id of [b.source, b.crosscheckSource]) {
      assert.ok(sourceIds.has(id), `${b.id} -> ${id}`);
      const s = wave.sources.find(x => x.id === id);
      assert.equal(new URL(s.url).hostname, 'data.sf.gov', id);
      assert.equal(s.access, 'page', id);
    }
    assert.notEqual(b.source, b.crosscheckSource, b.id);
  }
  for (const b of checks) {
    assert.equal(b.licenseCheck.number, b.registryLicenseNumber);
    assert.equal(new URL(b.licenseCheck.url).searchParams.get('LicNum'), b.registryLicenseNumber);
    assert.equal(b.licenseCheck.checkedAt, wave.checkedAt);
    assert.ok(sourceIds.has(`cslb-${b.registryLicenseNumber}`), b.id);
  }
  for (const r of wave.reviews) {
    assert.ok(sourceIds.has(r.source), r.id);
    assert.equal(r.checkedAt, wave.checkedAt);
    assert.ok(['review', 'business-description'].includes(r.kind), r.id);
  }
  for (const s of wave.sources) {
    assert.ok(['government', 'platform', 'community', 'context'].includes(s.kind), s.id);
    assert.ok(['page', 'search-extract'].includes(s.access), s.id);
  }
});

test('wave 19 pass 2: no known ID, name, core or registry-number collision', () => {
  const names = new Set(old.businesses.map(b => norm(b.name)));
  const cores = new Set(old.businesses.map(b => core(b.name)));
  const ids = new Set(old.businesses.map(b => b.id));
  // Search the full existing corpus prose, not just structured fields.
  const numbers = new Set(raw.toString().match(/\b\d{5,7}\b/g));
  for (const prev of [w17, w18]) {
    for (const b of prev.entries) {
      names.add(norm(b.name)); cores.add(core(b.name)); ids.add(b.id);
      if (b.registryLicenseNumber) numbers.add(b.registryLicenseNumber);
    }
  }
  for (const b of wave.entries) {
    assert.ok(!names.has(norm(b.name)), b.name);
    assert.ok(!cores.has(core(b.name)), b.name);
    assert.ok(!ids.has(b.id), b.id);
    if (b.registryLicenseNumber) assert.ok(!numbers.has(b.registryLicenseNumber), b.id);
    names.add(norm(b.name)); cores.add(core(b.name)); ids.add(b.id);
    if (b.registryLicenseNumber) numbers.add(b.registryLicenseNumber);
  }
  // Folds: one into the stored Caledonia record, one within this wave (553166 into 531666).
  assert.equal(wave.dedupeFolds.length, 2);
  const storedFold = wave.dedupeFolds.find(f => f.storedAs === 'w6-caledonia-plastering-stucco-inc');
  assert.ok(storedFold, 'caledonia fold');
  assert.ok(ids.has(storedFold.storedAs));
  const waveFold = wave.dedupeFolds.find(f => f.storedAs === 'w19-531666');
  assert.ok(waveFold, 'in-wave fold');
  assert.ok(wave.entries.some(b => b.id === 'w19-531666'));
  assert.ok(!wave.entries.some(b => b.registryLicenseNumber === '553166'), '553166 must not be a parallel entry');
});

test('wave 19 pass 3: fail closed, leave prior corpus and master untouched', () => {
  assert.equal(createHash('sha256').update(raw).digest('hex'), wave.baselineSha256);
  assert.equal(old.master.length, 0);
  assert.equal(old.businesses.length, 793);
  assert.equal(wave.stage, 'discovery-only');
  for (const b of wave.entries) {
    assert.equal(b.master, false);
    assert.equal(b.status, 'hold');
    assert.equal(Object.keys(b.requirements).length, 8);
    assert.ok(Object.values(b.requirements).every(v => v === 'unconfirmed'));
    assert.ok(b.flags.length >= 2, b.id);
  }
  for (const b of registry) assert.equal(b.reviews.length, 0, b.id);
  for (const b of platform) {
    assert.equal(b.license, null, b.id);
    for (const rid of b.reviews) assert.ok(wave.reviews.some(r => r.id === rid), `${b.id} -> ${rid}`);
  }
  for (const r of wave.reviews) assert.ok(wave.entries.some(b => b.id === r.entry), r.id);
  assert.equal(checks.length, 16);
  const byStatus = s => checks.filter(b => b.licenseCheck.status === s);
  assert.equal(byStatus('active').length, 14);
  assert.equal(byStatus('suspended').length, 1);
  assert.equal(byStatus('inactive').length, 1);
  assert.deepEqual(byStatus('suspended').map(b => b.licenseCheck.number), ['443682']);
  assert.deepEqual(byStatus('inactive').map(b => b.licenseCheck.number), ['933593']);
  const classes = Object.fromEntries(checks.map(b => [b.licenseCheck.number, b.licenseCheck.classes.join('+')]));
  assert.equal(classes['1032948'], 'B+C35+C-9+C36');
  assert.equal(classes['1087358'], 'B+C10+C36+C16');
  assert.equal(classes['937080'], 'B+C36+C54');
  assert.equal(classes['394146'], 'C10+B');
  assert.equal(classes['1050217'], 'C36+C42');
  assert.equal(classes['443682'], 'B+C-6');
  for (const n of ['1013908', '1074837', '1042086', '915382'])
    assert.equal(classes[n], 'B', n);
  for (const n of ['430548', '933593', '1003568', '1045949', '732885', '832458'])
    assert.equal(classes[n], 'C36', n);
  assert.equal(wave.reviews.length, 7);
  assert.equal(wave.reviews.filter(r => r.kind === 'review').length, 6);
  assert.equal(wave.reviews.filter(r => r.kind === 'business-description').length, 1);
});

test('wave 19 privacy: no excluded private-context marker in any field', () => {
  assertPrivacySafe(JSON.stringify(wave), 'wave19.json');
});
