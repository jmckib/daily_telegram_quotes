ZIP_PKG_NAME = deployment_package.zip

.PHONY: deps
deps:
	rm -rf lambda_function/package || true
	pip install --target lambda_function/package requests pyyaml

.PHONY: zip
zip:
	rm my-deployment-package.zip || true
	(cd lambda_function/package/ && zip -r ../../$(ZIP_PKG_NAME) .)
	(cd lambda_function/ && zip ../$(ZIP_PKG_NAME) lambda_function.py secrets.yaml quotes.json nicknames.json)

.PHONY: build
build: deps zip
