import { escapeHTML as e, csvCell } from './lib.js';
const queue = document.querySelector('#queue');
const count = document.querySelector('#result-count');
const query = document.querySelector('#query');
const stage = document.querySelector('#stage');
const exportButton = document.querySelector('#export');
let data;
const link = (url, text) => `<a href="${e(url)}" target="_blank" rel="noopener noreferrer">${e(text)} ↗</a>`;
const STATUS_LABEL = { active: 'Active', suspended: 'Suspended', inactive: 'Inactive', expired: 'Expired' };
function visible() {
  const q = query.value.trim().toLowerCase();
  return data.entries.filter(b => {
    const text = [b.name, b.registryLicenseNumber || '', b.licenseCheck?.legalName || '', ...b.flags].join(' ').toLowerCase();
    if (!text.includes(q)) return false;
    if (stage.value === 'all') return true;
    if (stage.value === 'checked') return Boolean(b.licenseCheck);
    if (stage.value === 'active') return b.licenseCheck?.status === 'active';
    if (stage.value === 'nonactive') return Boolean(b.licenseCheck) && b.licenseCheck.status !== 'active';
    if (stage.value === 'registry') return Boolean(b.registryLicenseNumber) && !b.licenseCheck;
    if (stage.value === 'platform') return b.trade === 'platform-lead';
    return true;
  });
}
function registryBody(b) {
  const c = b.licenseCheck;
  const citySource = data.sources.find(s => s.id === b.source);
  const xSource = data.sources.find(s => s.id === b.crosscheckSource);
  const number = b.observedFields.license1 ?? b.observedFields.license_number;
  const links = [link(citySource.url, 'City discovery query'), link(xSource.url, 'City cross-check query')];
  links.push(c?.url
    ? link(c.url, 'Read CSLB source')
    : link(`https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=${number}`, 'CSLB lookup — not read'));
  return { links, number };
}
function platformBody(b) {
  const p = b.platformEvidence;
  const links = [link(p.categoryUrl, 'Read platform category')];
  if (p.profileUrl) links.push(link(p.profileUrl, 'Profile link as displayed'));
  return { links };
}
function render() {
  const rows = visible();
  count.textContent = `${rows.length} of ${data.entries.length} leads · all on hold · no qualified matches`;
  queue.innerHTML = rows.length ? rows.map(b => {
    const c = b.licenseCheck;
    const isPlatform = b.trade === 'platform-lead';
    const eyebrow = c ? 'REGULATOR PAGE READ' : isPlatform ? 'PLATFORM / COMMUNITY LISTING' : 'HISTORICAL REGISTRY ONLY';
    const badge = c
      ? `<span class="badge ${c.status === 'suspended' ? 'danger' : c.status === 'active' ? '' : 'danger'}">${STATUS_LABEL[c.status]} licence read</span>`
      : '<span class="badge">On hold</span>';
    const { links } = isPlatform ? platformBody(b) : registryBody(b);
    const reviews = (b.reviews || []).map(rid => data.reviews.find(r => r.id === rid)).filter(Boolean);
    const p = b.platformEvidence;
    return `<article class="lead" id="${e(b.id)}"><div class="lead-head"><div><div class="eyebrow">${eyebrow}</div><h3>${e(b.name)}</h3></div>${badge}</div>
    <p class="record-number">${isPlatform
      ? `${e(p.platform)} category listing · read ${e(data.checkedAt)}`
      : `City registry number ${e(b.registryLicenseNumber)} · firm ZIP query: 94122 · cross-checked in a second City query`}</p>
    <div class="gates"><span>Plumbing: unconfirmed</span><span>Drywall: unconfirmed</span><span>Outer Sunset dispatch: unconfirmed</span></div>
    ${c ? `<p>CSLB: <strong>${e(c.status)}</strong> · ${e(c.classes.join(', '))} · expiry ${e(c.expires)}. Read ${e(c.checkedAt)}.</p>` : isPlatform
      ? `<p>${p.rating ? `Rating ${e(p.rating)} (${e(String(p.reviewCount ?? '?'))}) · ` : ''}${p.hires != null ? `${e(String(p.hires))} hires · ` : ''}${e(p.services || '')}</p>`
      : '<p>Licence status, classifications and legal identity have not been checked at CSLB.</p>'}
    <details><summary>Evidence, flags & next verification steps</summary><p>${e(b.discoveryContext)}</p>${c ? `<p>Regulator name: ${e(c.legalName)}<br>Regulator address: ${e(c.address)}</p><p>Displayed source timestamp: ${e(c.sourceAsOf)}</p><blockquote>${e(c.statusExcerpt)}</blockquote><p>${e(c.bond)}</p><p>${e(c.workersComp)}</p>${(c.additional || []).map(a => `<p>${e(a)}</p>`).join('')}` : ''}${isPlatform ? `<p>${e(p.badges)}</p><p>${e(p.serves)}</p>` : ''}${reviews.map(r => `<blockquote>“${e(r.excerpt)}”<br><small>${e(r.attribution)} · ${e(r.platform)} · ${e(r.access)} read ${e(r.checkedAt)} · ${e(r.kind === 'business-description' ? 'business self-description, not a customer review' : 'customer review excerpt')}${r.truncatedStart ? ' · truncated at start as displayed' : ''}${r.truncatedEnd ? ' · truncated at end as displayed' : ''}</small></blockquote>`).join('')}<ul>${b.flags.map(f => `<li>${e(f)}</li>`).join('')}</ul><p>Next: match the current legal identity, confirm both trades and dispatch, then obtain attributable repair evidence, project insurance and written scope. Do not interpret missing reviews as a positive or negative review.</p></details>
    <div class="lead-links">${links.join('')}</div></article>`;
  }).join('') : '<p class="empty">No leads match these filters. Try another name or reset the filters.</p>';
}
document.querySelector('#filters').addEventListener('submit', ev => ev.preventDefault());
document.querySelector('#filters').addEventListener('reset', () => {
  query.value = ''; stage.value = 'all'; if (data) render();
});
query.addEventListener('input', () => { if (data) render(); });
stage.addEventListener('change', () => { if (data) render(); });
exportButton.addEventListener('click', () => {
  const rows = [['Name','Registry number (not verified licence)','Status','Plumbing','Drywall','Outer Sunset dispatch','Evidence stage','CSLB status','Checked','Evidence','Flags'], ...visible().map(b => [b.name,b.registryLicenseNumber || 'platform listing','hold','unconfirmed','unconfirmed','unconfirmed',b.licenseCheck ? 'CSLB read' : b.trade === 'platform-lead' ? 'platform' : 'registry only',b.licenseCheck?.status || 'not read',data.checkedAt,b.licenseCheck?.url || b.platformEvidence?.categoryUrl || '',b.flags.join(' | ')])];
  const url = URL.createObjectURL(new Blob(['\uFEFF'+rows.map(r => r.map(csvCell).join(',')).join('\r\n')], {type:'text/csv;charset=utf-8'}));
  const a = document.createElement('a'); a.href = url; a.download = 'sunset-discovery-wave18.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
try {
  const response = await fetch('./data/wave18.json');
  if (!response.ok) throw new Error('The discovery dataset is unavailable.');
  data = await response.json();
  render();
  const groups = { government: 'Government sources', platform: 'Platform sources', community: 'Community sources', context: 'Mechanism context (not business evidence)' };
  document.querySelector('#sources').innerHTML = Object.entries(groups).map(([kind, title]) => {
    const list = data.sources.filter(s => s.kind === kind);
    return list.length ? `<h3>${title}</h3>${list.map(s => `<p>${link(s.url, s.id)}<br><small>${e(s.coverage)}</small></p>`).join('')}` : '';
  }).join('');
  exportButton.disabled = false;
} catch (error) {
  count.textContent = 'Discovery could not load.';
  queue.innerHTML = `<p class="empty">${e(error.message)} Reload the page or open <a href="./data/wave18.json">the source dataset</a>.</p>`;
}
