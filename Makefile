include common/Makefile

doc-export-openapi:
	@poetry run python export_open_api.py

doc-build: doc-export-openapi
	@poetry run mkdocs build
