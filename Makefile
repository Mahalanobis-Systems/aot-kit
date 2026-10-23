.PHONY: help validate stats render check site

# No installed package, just scripts needing pyyaml + jsonschema: an ephemeral uv run.
PY := uv run --with pyyaml --with jsonschema python3

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

validate: ## Schema-check every library file and cross-check ids and vocabulary
	$(PY) tools/validate.py validate

stats: ## Counts by kind, status, tier, lever and domain
	$(PY) tools/validate.py stats

render: ## Regenerate the skills, catalog.yaml and the README and start lists from library/
	$(PY) tools/render_skills.py

check: validate ## Validate, and fail if anything generated is out of date
	$(PY) tools/render_skills.py --check

site: ## Build the website's data, dist/library.json
	$(PY) tools/build_site.py
