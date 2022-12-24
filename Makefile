ZIP_PKG_NAME = deployment_package.zip

.PHONY: install_deps
install_deps:
	rm -rf lambda_function/package || true
	pip install --target lambda_function/package requests pyyaml

.PHONY: build_zip
build_zip:
	rm my-deployment-package.zip || true
	(cd lambda_function/package/ && zip -r ../../$(ZIP_PKG_NAME) .)
	(cd lambda_function/ && zip ../$(ZIP_PKG_NAME) lambda_function.py secrets.yaml)

.PHONY: build
build: install_deps build_zip
