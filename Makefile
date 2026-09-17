SHELL := /bin/bash

.PHONY: bootstrap test validate public-check release-check site-check demo docker-up package

bootstrap:
	./34_DEVELOPER_EXPERIENCE/scripts/bootstrap.sh

test:
	python3 -m pytest -q

validate:
	python3 30_AUTOMATION/validate_vault.py --root .

public-check:
	./65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/scripts/public-check.sh

release-check:
	python3 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/scripts/release_prepare.py --root .

site-check:
	python3 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/scripts/site_check.py

demo:
	./65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/demo/run_demo.sh

docker-up:
	docker compose -f docker-compose.community.yml up --build

package:
	python3 34_DEVELOPER_EXPERIENCE/scripts/package_release.py --root . --output-dir dist
