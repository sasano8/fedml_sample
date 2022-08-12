include common/Makefile

doc-export-openapi:
	@poetry run python export_open_api.py
