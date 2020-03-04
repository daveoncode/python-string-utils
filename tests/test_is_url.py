from unittest import TestCase

from string_utils import is_url


class IsUrlTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        self.assertFalse(is_url(None))
        self.assertFalse(is_url(False))
        self.assertFalse(is_url(0))
        self.assertFalse(is_url([]))
        self.assertFalse(is_url({'a': 1}))

    def test_string_cannot_be_blank(self):
        self.assertFalse(is_url(''))
        self.assertFalse(is_url(' '))

    def test_string_cannot_contain_spaces(self):
        self.assertFalse(is_url(' http://www.google.com'))
        self.assertFalse(is_url('http://www.google.com '))
        self.assertFalse(is_url('http://www.google.com/ ncr'))
        self.assertFalse(is_url('http://www.goo gle.com'))

    def test_scheme_is_required(self):
        self.assertFalse(is_url('google.com'))
        self.assertFalse(is_url('www.google.com'))

    def test_domain_extension_is_required_for_named_urls(self):
        self.assertFalse(is_url('http://google'))
        self.assertFalse(is_url('http://google.'))

    def test_domain_extension_should_be_between_2_and_6_letters(self):
        self.assertFalse(is_url('http://google.c'))
        self.assertFalse(is_url('http://google.abcdefghi'))

    def test_should_accept_any_scheme_by_default(self):
        self.assertTrue(is_url('http://site.com'))
        self.assertTrue(is_url('http://www.site.com'))
        self.assertTrue(is_url('https://site.com'))
        self.assertTrue(is_url('https://www.site.com'))
        self.assertTrue(is_url('ftp://site.com'))
        self.assertTrue(is_url('git://site.com'))

    def test_should_restrict_checking_on_provided_schemes(self):
        self.assertTrue(is_url('git://site.com'))
        self.assertFalse(is_url('git://site.com', allowed_schemes=['http', 'https']))

    def test_url_cannot_start_with_dot(self):
        self.assertFalse(is_url('http://.site.com'))

    def test_url_can_contain_dash(self):
        self.assertTrue(is_url('http://some-site-name.com'))

    def test_url_cannot_start_with_dash(self):
        self.assertFalse(is_url('http://-site.com'))

    def test_url_cannot_start_with_slash(self):
        self.assertFalse(is_url('http:///www.site.com'))

    def test_www_is_optional(self):
        self.assertTrue(is_url('http://www.mysite.com'))
        self.assertTrue(is_url('http://mysite.com'))

    def test_localhost_is_an_accepted_url(self):
        self.assertTrue(is_url('http://localhost'))

    def test_should_accept_valid_ip_url(self):
        self.assertTrue(is_url('http://123.123.123.123'))
        self.assertTrue(is_url('http://1.123.123.123'))
        self.assertTrue(is_url('http://1.1.123.123'))
        self.assertTrue(is_url('http://1.1.1.123'))
        self.assertTrue(is_url('http://1.1.1.1'))
        self.assertTrue(is_url('http://123.123.123.1'))
        self.assertTrue(is_url('http://123.123.1.1'))
        self.assertTrue(is_url('http://123.1.1.1'))

    def test_should_exclude_invalid_ip(self):
        self.assertFalse(is_url('http://1.2.3'))
        self.assertFalse(is_url('http://1.2.3.'))
        self.assertFalse(is_url('http://123.123.123.1234'))
        self.assertFalse(is_url('http://.123.123.123.123'))
        self.assertFalse(is_url('http://123.123.123.123.'))
        self.assertFalse(is_url('http://123.123...123.123'))
        self.assertFalse(is_url('http://123..123..123.123'))

    def test_url_can_have_port_number(self):
        self.assertTrue(is_url('http://localhost:8080'))

    def test_url_can_contain_sub_folders(self):
        self.assertTrue(is_url('http://www.site.com/one'))
        self.assertTrue(is_url('http://www.site.com/one/'))
        self.assertTrue(is_url('http://www.site.com/one/two'))
        self.assertTrue(is_url('http://www.site.com/one/two/'))
        self.assertTrue(is_url('http://www.site.com/one/two/three/four/five/six'))

    def test_url_can_have_user_and_password(self):
        self.assertTrue(is_url('postgres://myuser:mypassword@localhost:5432/mydb'))

    def test_url_can_contain_file_extension(self):
        self.assertTrue(is_url('http://site.com/foo/photo.jpg'))
        self.assertTrue(is_url('http://site.com/index.html'))

    def test_file_can_contains_multiple_dots(self):
        self.assertTrue(is_url('http://site.com/foo/file.name.ext'))

    def test_url_can_contain_query_string(self):
        self.assertTrue(is_url('http://site.com/foo/?'))
        self.assertTrue(is_url('http://site.com/foo/?foo'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar&baz=1'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar&baz=1&'))

    def test_url_can_have_hash_part(self):
        self.assertTrue(is_url('http://site.com/foo#anchor'))
        self.assertTrue(is_url('http://site.com/foo#anchor2-with_several+signs++'))

    def test_a_full_url(self):
        self.assertTrue(is_url('https://www.site.com/a/b/c/banana/file.html?foo=1&bar=2#hello-world'))
