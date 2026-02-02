#!/bin/bash

# Rollback script for AnancyIO
# Usage: ./rollback.sh [environment] [backup_date]

set -e

ENVIRONMENT=${1:-production}
BACKUP_DATE=$2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_message "$YELLOW" "🔄 Rolling back AnancyIO in $ENVIRONMENT environment..."

# Determine compose file
if [ "$ENVIRONMENT" == "production" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
else
    COMPOSE_FILE="docker-compose.staging.yml"
fi

cd "$PROJECT_ROOT"

# If backup date provided, restore from backup
if [ -n "$BACKUP_DATE" ]; then
    BACKUP_DIR="$PROJECT_ROOT/backups/$BACKUP_DATE"
    
    if [ ! -d "$BACKUP_DIR" ]; then
        print_message "$RED" "❌ Backup directory not found: $BACKUP_DIR"
        exit 1
    fi
    
    print_message "$GREEN" "📦 Restoring from backup: $BACKUP_DATE"
    
    # Stop services
    docker-compose -f "$COMPOSE_FILE" down
    
    # Restore volumes
    if [ -f "$BACKUP_DIR/anancyio-data.tar.gz" ]; then
        print_message "$GREEN" "Restoring data volume..."
        docker run --rm \
            -v anancyio-data:/data \
            -v "$BACKUP_DIR":/backup \
            alpine sh -c "rm -rf /data/* && tar xzf /backup/anancyio-data.tar.gz -C /data"
    fi
    
    if [ -f "$BACKUP_DIR/anancyio-memory.tar.gz" ]; then
        print_message "$GREEN" "Restoring memory volume..."
        docker run --rm \
            -v anancyio-memory:/data \
            -v "$BACKUP_DIR":/backup \
            alpine sh -c "rm -rf /data/* && tar xzf /backup/anancyio-memory.tar.gz -C /data"
    fi
    
    print_message "$GREEN" "✓ Volumes restored"
fi

# Pull previous stable version
print_message "$GREEN" "📦 Pulling previous stable image..."
if [ "$ENVIRONMENT" == "production" ]; then
    docker pull anancyioai/anancyio:latest
else
    docker pull anancyioai/anancyio:develop
fi

# Start services
print_message "$GREEN" "🚀 Starting services..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait and health check
sleep 10

MAX_RETRIES=30
RETRY_COUNT=0
if [ "$ENVIRONMENT" == "production" ]; then
    HEALTH_URL="http://localhost:80/health"
else
    HEALTH_URL="http://localhost:8080/health"
fi

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
        print_message "$GREEN" "✅ Rollback successful! Services are healthy."
        exit 0
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    print_message "$YELLOW" "⏳ Waiting for services... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 5
done

print_message "$RED" "❌ Rollback health check failed."
exit 1
