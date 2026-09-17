import { escapeHTML as e, csvCell } from './lib.js';
const queue = document.querySelector('#queue');
const count = document.querySelector('#result-count');
const query = document.querySelector('#query');
const stage = document.querySelector('#stage');
const exportButton = document.querySelector('#export');
let data;
const link = (url, text) => `<a href="${e(url)}" target="_blank" rel="noopener noreferrer">${e(text)} ↗</a>`;
function visible() {
  const q = query.value.trim().toLowerCase();
  return data.entries.filter(b =>
    [b.name, b.registryLicenseNumber, ...b.flags].join(' ').toLowerCase().includes(q) &&
    (stage.value === 'all' || (stage.value === 'checked' && b.licenseCheck) ||
    (stage.value === 'unread' && !b.licenseCheck) ||
    (stage.value === 'suspended' && b.licenseCheck?.status === 'suspended')));
}
function render() {
  const rows = visible();
  count.textContent = `${rows.length} of ${data.entries.length} leads · all on hold · no qualified matches`;
  queue.innerHTML = rows.length ? rows.map(b => {
    const c = b.licenseCheck;
    const source = data.sources.find(s => s.id === b.crosscheckSource);
    return `<article class="lead" id="${e(b.id)}"><div class="lead-head"><div><div class="eyebrow">${c ? 'REGULATOR PAGE READ' : 'HISTORICAL REGISTRY ONLY'}</div><h3>${e(b.name)}</h3></div><span class="badge ${c?.status === 'suspended' ? 'danger' : ''}">${c?.status === 'suspended' ? 'Suspension flagged' : 'On hold'}</span></div>
    <p class="record-number">City registry number ${e(b.registryLicenseNumber)} · firm ZIP query: 94122</p>
    <div class="gates"><span>Plumbing: unconfirmed</span><span>Drywall: unconfirmed</span><span>Outer Sunset dispatch: unconfirmed</span></div>
    <p>${c ? `CSLB: <strong>${e(c.status)}</strong> · ${e(c.classes.join(', '))} · expiry ${e(c.expires)}. Read ${e(c.checkedAt)}.` : 'Licence status, classifications and legal identity have not been checked at CSLB.'}</p>
    <details><summary>Evidence, flags & next verification steps</summary><p>${e(b.discoveryContext)}</p>${c ? `<p>Regulator name: ${e(c.legalName)}<br>Regulator address: ${e(c.address)}</p><p>Displayed source timestamp: ${e(c.sourceAsOf)}</p><blockquote>${e(c.statusExcerpt)}</blockquote>` : ''}<ul>${b.flags.map(f => `<li>${e(f)}</li>`).join('')}</ul><p>Next: match the current legal identity, confirm both trades and dispatch, then obtain attributable repair evidence, project insurance and written scope. Do not interpret missing reviews as a positive or negative review.</p></details>
    <div class="lead-links">${link(source.url, 'City name/number evidence')}${link(c?.url || `https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=${b.registryLicenseNumber}`, c ? 'Read CSLB source' : 'CSLB lookup — not read')}</div></article>`;
  }).join('') : '<p class="empty">No leads match these filters. Try another name or reset the filters.</p>';
}
document.querySelector('#filters').addEventListener('submit', ev => ev.preventDefault());
document.querySelector('#filters').addEventListener('reset', () => {
  query.value = ''; stage.value = 'all'; if (data) render();
});
query.addEventListener('input', () => { if (data) render(); });
stage.addEventListener('change', () => { if (data) render(); });
exportButton.addEventListener('click', () => {
  const rows = [['Name','Registry number (not verified licence)','Status','Plumbing','Drywall','Outer Sunset dispatch','CSLB status','Checked','Evidence','Flags'], ...visible().map(b => [b.name,b.registryLicenseNumber,'hold','unconfirmed','unconfirmed','unconfirmed',b.licenseCheck?.status || 'not read',data.checkedAt,data.sources.find(s => s.id === b.crosscheckSource).url,b.flags.join(' | ')])];
  const url = URL.createObjectURL(new Blob(['\uFEFF'+rows.map(r => r.map(csvCell).join(',')).join('\r\n')], {type:'text/csv;charset=utf-8'}));
  const a = document.createElement('a'); a.href = url; a.download = 'sunset-discovery-wave17.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
try {
  const response = await fetch('./data/wave17.json');
  if (!response.ok) throw new Error('The discovery dataset is unavailable.');
  data = await response.json();
  render();
  document.querySelector('#sources').innerHTML = data.sources.map(s => `<p>${link(s.url, s.id === 'city-crosscheck' ? 'Targeted City cross-check — all 52 rows read' : 'City discovery query — partial response read')}<br><small>${e(s.coverage)}</small></p>`).join('');
  exportButton.disabled = false;
} catch (error) {
  count.textContent = 'Discovery could not load.';
  queue.innerHTML = `<p class="empty">${e(error.message)} Reload the page or open <a href="./data/wave17.json">the source dataset</a>.</p>`;
}
