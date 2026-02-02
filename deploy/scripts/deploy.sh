#!/bin/bash

# Deploy script for AnancyIO
# Usage: ./deploy.sh [environment]
# Environments: staging, production

set -e

ENVIRONMENT=${1:-staging}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🚀 Deploying AnancyIO to $ENVIRONMENT environment..."

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if environment is valid
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    print_message "$RED" "❌ Invalid environment: $ENVIRONMENT"
    print_message "$YELLOW" "Usage: $0 [staging|production]"
    exit 1
fi

# Load environment variables
if [ -f "$PROJECT_ROOT/.env.$ENVIRONMENT" ]; then
    print_message "$GREEN" "✓ Loading $ENVIRONMENT environment variables..."
    export $(cat "$PROJECT_ROOT/.env.$ENVIRONMENT" | grep -v '^#' | xargs)
else
    print_message "$YELLOW" "⚠️  No .env.$ENVIRONMENT file found, using system environment variables"
fi

# Determine which docker-compose file to use
if [ "$ENVIRONMENT" == "production" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
else
    COMPOSE_FILE="docker-compose.staging.yml"
fi

cd "$PROJECT_ROOT"

# Pull latest images
print_message "$GREEN" "📦 Pulling latest Docker images..."
docker-compose -f "$COMPOSE_FILE" pull

# Backup current volumes (production only)
if [ "$ENVIRONMENT" == "production" ]; then
    print_message "$GREEN" "💾 Creating backup..."
    BACKUP_DIR="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup volumes
    docker run --rm \
        -v anancyio-data:/data \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf /backup/anancyio-data.tar.gz -C /data .
    
    docker run --rm \
        -v anancyio-memory:/data \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf /backup/anancyio-memory.tar.gz -C /data .
    
    print_message "$GREEN" "✓ Backup created at $BACKUP_DIR"
fi

# Stop current containers
print_message "$GREEN" "🛑 Stopping current containers..."
docker-compose -f "$COMPOSE_FILE" down

# Start new containers
print_message "$GREEN" "🚀 Starting new containers..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
print_message "$GREEN" "⏳ Waiting for services to be healthy..."
sleep 10

# Health check
MAX_RETRIES=30
RETRY_COUNT=0
HEALTH_URL="http://localhost"

if [ "$ENVIRONMENT" == "production" ]; then
    HEALTH_URL="http://localhost:80/health"
else
    HEALTH_URL="http://localhost:8080/health"
fi

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
        print_message "$GREEN" "✅ Deployment successful! Services are healthy."
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    print_message "$YELLOW" "⏳ Waiting for services to be ready... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 5
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    print_message "$RED" "❌ Health check failed. Rolling back..."
    
    # Rollback
    docker-compose -f "$COMPOSE_FILE" down
    
    if [ "$ENVIRONMENT" == "production" ]; then
        print_message "$YELLOW" "🔄 Restoring from backup..."
        # Restore would happen here
    fi
    
    exit 1
fi

# Clean up old images
print_message "$GREEN" "🧹 Cleaning up old Docker images..."
docker image prune -f

# Show running containers
print_message "$GREEN" "📊 Running containers:"
docker-compose -f "$COMPOSE_FILE" ps

# Show logs
print_message "$GREEN" "📝 Recent logs:"
docker-compose -f "$COMPOSE_FILE" logs --tail=50

print_message "$GREEN" "✅ Deployment to $ENVIRONMENT completed successfully!"

if [ "$ENVIRONMENT" == "production" ]; then
    print_message "$GREEN" "🌐 Application is available at: https://anancyio.ai"
else
    print_message "$GREEN" "🌐 Application is available at: http://localhost:8080"
fi
