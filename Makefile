path := .

define Comment
	- Run `make help` to see all the available options.
endef

.PHONY: help
help: ## 도움말
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: up
up: ## 컨테이너 실행
	@docker-compose up -d

.PHONY: down
down: ## 컨테이너 중지
	@docker-compose down

.PHONY: build
build: ## 컨테이너 빌드
	@docker-compose build

.PHONY: logs
logs: ## 컨테이너 로그
	@docker-compose logs -t -f app
