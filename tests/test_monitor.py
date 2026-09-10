import importlib.util
import unittest
from unittest.mock import patch
from pathlib import Path
spec = importlib.util.spec_from_file_location('monitor', Path(__file__).parents[1] / 'scripts/check_sources.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SourceMonitorTests(unittest.TestCase):
    def test_normalizes_whitespace_entities_and_quotes(self):
        self.assertEqual(m.normalize(' It’s\n a &amp; B '), "it's a & b")

    def test_parser_ignores_scripts_but_quarantines_structured_reviews(self):
        p = m.PageParser()
        p.feed('<p>Visible evidence</p><style>hidden</style><script>bad</script><script type="application/ld+json">{"@type":"Review","author":{"name":"A"},"reviewBody":"Good job","datePublished":"2026-01-01"}</script>')
        self.assertEqual(' '.join(p.text), 'Visible evidence')
        rows = m.structured_reviews(p.json_documents)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['identity'], 'unresolved')
        self.assertEqual(rows[0]['state'], 'quarantine')

    def test_deduplicates_reviews_without_claiming_entity_match(self):
        doc = {'@type': 'Review', 'reviewBody': 'Good job'}
        self.assertEqual(len(m.structured_reviews([doc, doc])), 1)

    def test_invalid_json_is_not_invented(self):
        p = m.PageParser()
        p.feed('<script type="application/ld+json">bad-json</script>')
        self.assertEqual(m.structured_reviews(p.json_documents), [])

    def test_rejects_non_public_urls(self):
        for url in ['file:///etc/passwd', 'javascript:alert(1)', 'http://user:password@example.com', 'http://example.com:4173/']:
            with self.assertRaises(ValueError):
                m.public_url(url)
        with patch.object(m.socket, 'getaddrinfo', return_value=[(2, 1, 6, '', ('127.0.0.1', 80))]):
            with self.assertRaises(ValueError):
                m.public_url('http://example.com/')

    def test_access_failure_does_not_claim_verification(self):
        class Blocked:
            def fetch(self, url):
                return None, url, [], 'access_error', 'HTTP 403'
        out = m.audit_one(Blocked(), 'https://example.com/', [{'id': 1}], [('x', 'words')])
        self.assertNotIn('evidenceChecks', out)
        self.assertEqual(out['state'], 'access_error')

    def test_missing_text_is_flagged_not_promoted(self):
        class Changed:
            def fetch(self, url):
                return '<p>Different content</p>', url, [], 'retrieved', 'HTTP 200'
        out = m.audit_one(Changed(), 'https://example.com/', [{'id': 1, 'kind': 'business'}], [('x', 'original evidence')])
        self.assertFalse(out['evidenceChecks'][0]['excerptFound'])
        self.assertTrue(out['findings'])

    def test_robots_failure_skips_page(self):
        with patch.object(m, 'public_url', return_value=m.parse.urlsplit('https://example.com/')):
            monitor = m.Monitor()
            monitor.policy = lambda origin: None
            self.assertEqual(monitor.fetch('https://example.com/')[3], 'robots_unavailable')


if __name__ == '__main__':
    unittest.main()
