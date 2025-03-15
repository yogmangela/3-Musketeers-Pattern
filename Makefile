# Define variables for Docker Compose commands
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_BUILD = $(DOCKER_COMPOSE) build
DOCKER_COMPOSE_UP = $(DOCKER_COMPOSE) up -d
DOCKER_COMPOSE_DOWN = $(DOCKER_COMPOSE) down
DOCKER_COMPOSE_LOGS = $(DOCKER_COMPOSE) logs
DOCKER_COMPOSE_CLEAN = $(DOCKER_COMPOSE) down -v

# Build the Docker images using Docker Compose
build:
	$(DOCKER_COMPOSE_BUILD)

# Start the containers and services defined in the Docker Compose file
up:
	$(DOCKER_COMPOSE_UP)

# Stop the containers
down:
	$(DOCKER_COMPOSE_DOWN)

# Show logs from all containers
logs:
	$(DOCKER_COMPOSE_LOGS)

# Clean up Docker volumes (to remove persistent data)
clean:
	$(DOCKER_COMPOSE_CLEAN)

# Full cycle: build, up, and clean if needed
full: build up
	@echo "Application is up and running. You can access it on http://localhost:5000"
	@echo "To stop the services, run: make down"