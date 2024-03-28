from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page #(1)

class HomePageTest(TestCase):
  def test_root_url_resolves_to_home_page_view(self):
    found=resolve('/')	#(2)
    self.assertEqual(found.func,home_page)	#(3)
  def test_home_page_return_correct_html(self):
     request=HttpRequest()
     response=home_page(request)
     html=response.content.decode('utf8')
     self.assertTrue(html.startswith('<html>'))
     self.assertIn('<title>To-Do lists</title>',html)
     self.assertTrue(html.endswith('</html>'))
# Create your tests here.
