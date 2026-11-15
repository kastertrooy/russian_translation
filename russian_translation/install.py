import frappe

RUSSIAN_LANGUAGE = {
	"language_code": "ru",
	"language_name": "Russian (Русский)",
	"enabled": 1,
	"date_format": "dd.mm.yyyy",
	"time_format": "HH:mm:ss",
	"number_format": "# ###,##",
	"first_day_of_the_week": "Monday",
}


def ensure_russian_language():
	if frappe.db.exists("Language", "ru"):
		language = frappe.get_doc("Language", "ru")
		if not language.enabled:
			language.enabled = 1
			language.save(ignore_permissions=True)

		if "Russian" not in language.language_name:
			# Language.language_name is set_only_once in Frappe; retain its localized name while
			# adding an English search term after saving any other changes.
			frappe.db.set_value(
				"Language",
				"ru",
				"language_name",
				f"Russian ({language.language_name})",
				update_modified=False,
			)
			frappe.cache.delete_value("languages_with_name")
			frappe.client_cache.delete_value("languages")
		return

	language = frappe.new_doc("Language")
	language.update(RUSSIAN_LANGUAGE)
	language.insert(ignore_permissions=True)
