#!/usr/bin/env python3
"""Read-only source monitoring. Never promotes businesses or overwrites research.

Uses public, robots-permitted pages only. Unknown robots policy, authentication,
CAPTCHAs, non-public hosts and access barriers fail closed. The initial curated
search extracts are not treated as full page reads by this monitor.
"""
import argparse
import concurrent.futures
import hashlib
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import socket
import threading
import time
from datetime import datetime, timezone
from urllib import request, error, parse, robotparser

ROOT = Path(__file__).resolve().parents[1]
AGENT = 'SunsetRepairSourceAudit/1.0'
LIMIT = 2_000_000
TIMEOUT = 15


def normalize(text):
    return re.sub(r'\s+', ' ', html.unescape(text).translate(str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-'}))).strip().casefold()


def public_url(url):
    parsed = parse.urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Non-public URL scheme or credentials rejected')
    if parsed.port not in (None, 80, 443):
        raise ValueError('Non-standard port rejected')
    for addr in socket.getaddrinfo(parsed.hostname, parsed.port or 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(addr[4][0]).is_global:
            raise ValueError('Non-public network target rejected')
    return parsed


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.skip = 0
        self.in_json = False
        self.json_parts = []
        self.json_documents = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip += 1
            if tag == 'script' and dict(attrs).get('type', '').lower() == 'application/ld+json':
                self.in_json = True
                self.json_parts = []

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = max(0, self.skip - 1)
            if self.in_json and tag == 'script':
                try:
                    self.json_documents.append(json.loads(''.join(self.json_parts)))
                except (ValueError, TypeError):
                    pass
                self.in_json = False

    def handle_data(self, text):
        if self.in_json:
            self.json_parts.append(text)
        elif not self.skip:
            self.text.append(text)


def structured_reviews(documents):
    """Short, quarantined candidates. No implication of entity/transaction match."""
    found = {}
    def walk(obj):
        if isinstance(obj, list):
            for item in obj:
                walk(item)
        elif isinstance(obj, dict):
            kind = obj.get('@type', '')
            if kind == 'Review' or isinstance(kind, list) and 'Review' in kind:
                body = obj.get('reviewBody', obj.get('description', ''))
                if isinstance(body, str) and body.strip():
                    author = obj.get('author', {})
                    author = author.get('name') if isinstance(author, dict) else author if isinstance(author, str) else None
                    date = obj.get('datePublished')
                    key = hashlib.sha256(normalize(body).encode()).hexdigest()
                    found[key] = {'hash': key, 'author': author, 'published': date, 'excerpt': body[:500], 'identity': 'unresolved', 'state': 'quarantine'}
            for val in obj.values():
                walk(val)
    walk(documents)
    return list(found.values())


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Monitor:
    def __init__(self):
        self.opener = request.build_opener(NoRedirect)
        self.host_locks = {}
        self.lock = threading.Lock()
        self.policies = {}
        self.last = {}

    def get(self, url):
        """Single request. Redirects are explicitly revalidated and robot-checked."""
        public_url(url)
        with self.opener.open(request.Request(url, headers={'User-Agent': AGENT, 'Accept': 'text/html,text/plain,application/json'}), timeout=TIMEOUT) as response:
            raw = response.read(LIMIT + 1)
            if len(raw) > LIMIT:
                raise ValueError('Page size exceeds monitoring limit')
            mime = response.headers.get_content_type()
            if mime not in ('text/html', 'text/plain', 'application/xhtml+xml',
                             'application/json', 'application/geo+json'):
                raise ValueError('Not an HTML/text/JSON page')
            return raw.decode(response.headers.get_content_charset() or 'utf-8', errors='replace'), response.status

    def policy(self, origin):
        if origin in self.policies:
            return self.policies[origin]
        try:
            raw, _ = self.get(origin + '/robots.txt')
            if '<html' in raw.lower():
                result = None  # HTML is not a valid robots policy for this conservative audit.
            else:
                result = robotparser.RobotFileParser()
                result.parse(raw.splitlines())
        except error.HTTPError as ex:
            if ex.code == 404:
                result = robotparser.RobotFileParser()
                result.parse(['User-agent: *', 'Disallow:'])
            else:
                result = None
        except Exception:
            result = None
        self.policies[origin] = result
        return result

    def fetch(self, url):
        chain = []
        for _ in range(6):
            parsed = public_url(url)
            origin = f'{parsed.scheme}://{parsed.netloc}'
            with self.lock:
                lock = self.host_locks.setdefault(parsed.hostname, threading.Lock())
            with lock:
                policy = self.policy(origin)
                if policy is None:
                    return None, url, chain, 'robots_unavailable', 'Robots policy could not be established; skipped.'
                if not policy.can_fetch(AGENT, url):
                    return None, url, chain, 'robots_disallowed', 'Robots policy disallows automated retrieval.'
                delay = max(1.0, float(policy.crawl_delay(AGENT) or 0))
                if delay > 60:
                    return None, url, chain, 'crawl_delay_exceeded', 'Requested crawl delay exceeds audit limit; skipped.'
                time.sleep(max(0, delay - (time.monotonic() - self.last.get(parsed.hostname, 0))))
                try:
                    body, status = self.get(url)
                    return body, url, chain, 'retrieved', f'HTTP {status}; retrieval alone is not factual verification.'
                except error.HTTPError as ex:
                    if ex.code in (301, 302, 303, 307, 308) and ex.headers.get('Location'):
                        destination = parse.urljoin(url, ex.headers['Location'])
                        chain.append({'from': url, 'to': destination, 'status': ex.code})
                        url = destination
                    else:
                        return None, url, chain, 'access_error', f'HTTP {ex.code}; no bypass attempted.'
                finally:
                    self.last[parsed.hostname] = time.monotonic()
        return None, url, chain, 'redirect_limit', 'Too many redirects; review required.'


def audit_one(monitor, url, sources, expected):
    result = {'sourceIds': [s['id'] for s in sources], 'url': url, 'checkedAt': datetime.now(timezone.utc).isoformat(), 'findings': []}
    try:
        body, final, redirects, state, note = monitor.fetch(url)
        result.update(finalUrl=final, redirects=redirects, state=state, note=note)
        if redirects:
            result['findings'].append('Redirect detected: recheck page identity, not just link availability.')
        if body:
            parsed = PageParser()
            stripped = body.lstrip()
            if stripped.startswith(('{', '[')):
                # SODA and other official open-data endpoints are JSON. Treat
                # the complete response as searchable text rather than feeding
                # it through an HTML parser, which would discard it.
                text = normalize(body)
                try:
                    parsed.json_documents.append(json.loads(body))
                except (ValueError, TypeError):
                    pass
            else:
                parsed.feed(body)
                text = normalize(' '.join(parsed.text))
            result['textHash'] = hashlib.sha256(text.encode()).hexdigest()
            # Avoid classifying ordinary contact-form CAPTCHA mentions as a barrier.
            if len(text) < 1500 and any(x in text for x in ('verify you are human', 'just a moment', 'access denied', 'enable javascript and cookies')):
                result.update(state='access_barrier', note='Challenge page detected; evidence was not checked.')
                return result
            if 'website expired' in text:
                result['findings'].append('Website-expired page detected; not proof the business is closed.')
            result['evidenceChecks'] = [{'reference': ref, 'excerptFound': normalize(quote) in text} for ref, quote in expected]
            if any(not check['excerptFound'] for check in result['evidenceChecks']):
                result['findings'].append('Retained text not found: page may have changed, be partial, or require rendering. No conclusion of falsehood.')
            if any(s['kind'] == 'government' for s in sources):
                statuses = [x for x in ('this license is current and active.', 'this license is expired and not able to contract at this time.') if x in text]
                result['licenseStatusText'] = statuses or ['Status not confidently parsed; no inference made.']
            result['reviewCandidates'] = structured_reviews(parsed.json_documents)
    except Exception as ex:
        result.update(state='fetch_failed', note=f'{type(ex).__name__}: {ex}')
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--limit', type=int, default=0, help='Optional smoke-test URL limit; 0 checks all registered sources.')
    ap.add_argument('--output', default=str(ROOT / 'reports'))
    args = ap.parse_args()
    data = json.loads((ROOT / 'data/research.json').read_text())
    groups = {}
    expected = {}
    for s in data['sources']:
        groups.setdefault(s['url'], []).append(s)
    by_id = {s['id']: s['url'] for s in data['sources']}
    for b in data['businesses']:
        for i, c in enumerate(b['claims']):
            expected.setdefault(by_id[c['source']], []).append((f'{b["id"]}.claims[{i}]', c['excerpt']))
    for r in data['reviews']:
        expected.setdefault(by_id[r['source']], []).append((r['id'], r['quote']))
    jobs = list(groups.items())[:args.limit or None]
    monitor = Monitor()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(audit_one, monitor, url, ss, expected.get(url, [])) for url, ss in jobs]
        results = [f.result() for f in futures]
    report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'researchSnapshot': data['researchedAt'], 'scope': 'Read-only source audit; no semantic verification, no master promotion.', 'completeReviewCorpus': False, 'results': results}
    dest = Path(args.output)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'source-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Source monitoring report', '', report['scope'], '', f'Checked {len(results)} unique URLs. Reviewed research was not overwritten.', '', '| Source IDs | Retrieval outcome | Findings |', '| --- | --- | --- |']
    for result in results:
        ids = ', '.join(map(str, result['sourceIds']))
        lines.append(f'| {ids} | {result["state"]} | {"; ".join(result["findings"]) or result.get("note", "")} |')
    (dest / 'source-audit.md').write_text('\n'.join(lines) + '\n')
    print(f'Wrote {dest / "source-audit.json"} ({len(results)} URLs); no research or qualification status modified.')


if __name__ == '__main__':
    main()
