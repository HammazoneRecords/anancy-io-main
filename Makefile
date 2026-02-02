.PHONY: help build deploy-staging deploy-production rollback backup health-check clean logs

# Default target
help:
	@echo "AnancyIO Deployment Commands"
	@echo "============================="
	@echo ""
	@echo "Development:"
	@echo "  make build              - Build Docker image locally"
	@echo "  make run                - Run locally with docker-compose"
	@echo "  make stop               - Stop local containers"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-staging     - Deploy to staging environment"
	@echo "  make deploy-production  - Deploy to production environment"
	@echo "  make rollback-staging   - Rollback staging deployment"
	@echo "  make rollback-prod      - Rollback production deployment"
	@echo ""
	@echo "Maintenance:"
	@echo "  make backup-staging     - Backup staging data"
	@echo "  make backup-prod        - Backup production data"
	@echo "  make health-staging     - Check staging health"
	@echo "  make health-prod        - Check production health"
	@echo ""
	@echo "Utilities:"
	@echo "  make logs-staging       - View staging logs"
	@echo "  make logs-prod          - View production logs"
	@echo "  make clean              - Clean up Docker resources"
	@echo "  make shell              - Open shell in running container"

# Development targets
build:
	@echo "Building AnancyIO Docker image..."
	docker build -f DockerfileLocal -t anancyio:local .

build-optimized:
	@echo "Building optimized AnancyIO Docker image..."
	DOCKER_BUILDKIT=1 docker build -f DockerfileLocal.optimized -t anancyio:local .

run:
	@echo "Starting AnancyIO locally..."
	docker-compose up -d
	@echo "Application available at http://localhost:50080"

stop:
	@echo "Stopping AnancyIO..."
	docker-compose down

restart:
	@echo "Restarting AnancyIO..."
	docker-compose restart

# Staging deployment
deploy-staging:
	@echo "Deploying to staging environment..."
	chmod +x deploy/scripts/deploy.sh
	./deploy/scripts/deploy.sh staging

rollback-staging:
	@echo "Rolling back staging deployment..."
	chmod +x deploy/scripts/rollback.sh
	./deploy/scripts/rollback.sh staging

backup-staging:
	@echo "Creating staging backup..."
	chmod +x deploy/scripts/backup.sh
	./deploy/scripts/backup.sh staging

health-staging:
	@echo "Checking staging health..."
	chmod +x deploy/scripts/health-check.sh
	./deploy/scripts/health-check.sh staging

logs-staging:
	@echo "Viewing staging logs..."
	docker-compose -f docker-compose.staging.yml logs -f --tail=100

# Production deployment
deploy-production:
	@echo "Deploying to production environment..."
	@echo "WARNING: This will deploy to production. Continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	chmod +x deploy/scripts/deploy.sh
	./deploy/scripts/deploy.sh production

rollback-prod:
	@echo "Rolling back production deployment..."
	@echo "WARNING: This will rollback production. Continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	chmod +x deploy/scripts/rollback.sh
	./deploy/scripts/rollback.sh production

backup-prod:
	@echo "Creating production backup..."
	chmod +x deploy/scripts/backup.sh
	./deploy/scripts/backup.sh production

health-prod:
	@echo "Checking production health..."
	chmod +x deploy/scripts/health-check.sh
	./deploy/scripts/health-check.sh production

logs-prod:
	@echo "Viewing production logs..."
	docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Kubernetes targets
k8s-deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f deploy/k8s-deployment.yml

k8s-status:
	@echo "Checking Kubernetes status..."
	kubectl get all -n anancyio

k8s-logs:
	@echo "Viewing Kubernetes logs..."
	kubectl logs -f deployment/anancyio -n anancyio --tail=100

k8s-delete:
	@echo "Deleting Kubernetes deployment..."
	@echo "WARNING: This will delete the deployment. Continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	kubectl delete -f deploy/k8s-deployment.yml

# Utility targets
shell:
	@echo "Opening shell in running container..."
	docker-compose exec anancyio /bin/bash

shell-staging:
	docker-compose -f docker-compose.staging.yml exec anancyio /bin/bash

shell-prod:
	docker-compose -f docker-compose.prod.yml exec anancyio /bin/bash

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	@echo "Cleanup complete"

clean-all:
	@echo "WARNING: This will remove all Docker images and volumes. Continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	docker-compose down -v
	docker system prune -af --volumes

# Testing targets
test:
	@echo "Running tests..."
	docker-compose exec anancyio pytest tests/

test-local:
	@echo "Running tests locally..."
	pytest tests/

lint:
	@echo "Running linters..."
	black --check .
	flake8 .
	isort --check-only .

format:
	@echo "Formatting code..."
	black .
	isort .

# List backups
list-backups:
	@echo "Available backups:"
	@ls -lht backups/ 2>/dev/null || echo "No backups found"

# Monitor resources
monitor:
	@echo "Monitoring Docker resources..."
	docker stats

# Update scripts permissions
setup:
	@echo "Setting up deployment scripts..."
	chmod +x deploy/scripts/*.sh
	@echo "Setup complete"
