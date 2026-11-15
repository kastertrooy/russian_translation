from unittest import TestCase
from unittest.mock import Mock, patch

from russian_translation.install import RUSSIAN_LANGUAGE, ensure_russian_language


class TestEnsureRussianLanguage(TestCase):
	def test_creates_russian_language(self):
		with patch("russian_translation.install.frappe") as frappe:
			frappe.db.exists.return_value = False
			language = Mock()
			frappe.new_doc.return_value = language

			ensure_russian_language()

			language.update.assert_called_once_with(RUSSIAN_LANGUAGE)
			language.insert.assert_called_once_with(ignore_permissions=True)

	def test_enables_existing_russian_language(self):
		with patch("russian_translation.install.frappe") as frappe:
			frappe.db.exists.return_value = True
			language = Mock(enabled=0, language_name="Русский")
			frappe.get_doc.return_value = language

			ensure_russian_language()

			language.save.assert_called_once_with(ignore_permissions=True)
			frappe.db.set_value.assert_called_once_with(
				"Language",
				"ru",
				"language_name",
				"Russian (Русский)",
				update_modified=False,
			)
			frappe.cache.delete_value.assert_called_once_with("languages_with_name")
			frappe.client_cache.delete_value.assert_called_once_with("languages")
			self.assertEqual(language.enabled, 1)

	def test_adds_english_search_term_and_preserves_enabled_language(self):
		with patch("russian_translation.install.frappe") as frappe:
			frappe.db.exists.return_value = True
			language = Mock(enabled=1, language_name="Русский")
			frappe.get_doc.return_value = language

			ensure_russian_language()

			frappe.db.set_value.assert_called_once_with(
				"Language",
				"ru",
				"language_name",
				"Russian (Русский)",
				update_modified=False,
			)
			language.save.assert_not_called()
			frappe.cache.delete_value.assert_called_once_with("languages_with_name")
			frappe.client_cache.delete_value.assert_called_once_with("languages")

	def test_is_idempotent_for_enabled_language(self):
		with patch("russian_translation.install.frappe") as frappe:
			frappe.db.exists.return_value = True
			language = Mock(enabled=1, language_name="Russian (Русский)")
			frappe.get_doc.return_value = language

			ensure_russian_language()

			frappe.db.set_value.assert_not_called()
			language.save.assert_not_called()
			frappe.cache.delete_value.assert_not_called()
			frappe.client_cache.delete_value.assert_not_called()
