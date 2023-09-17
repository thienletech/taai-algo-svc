.PHONY: all
all: clean build run

.PHONY: clean
clean:
	docker stop $$(docker ps -a -q --filter "ancestor=taai-algo-svc:latest") || true
	docker rm $$(docker ps -a -q --filter "ancestor=taai-algo-svc:latest") || true
	docker rmi -f $$(docker images -q taai-algo-svc:latest) || true

.PHONY: build
build: clean
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker build -t taai-algo-svc:latest .

.PHONY: run
run:
	docker run -d --network="host" -v /taai:/taai --env-file .env taai-algo-svc:latest

.PHONY: log
log:
	docker logs -f $$(docker ps -qf "ancestor=taai-algo-svc:latest")
