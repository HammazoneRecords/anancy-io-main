#!/bin/bash

# Health check script for AnancyIO
# Usage: ./health-check.sh [environment]

ENVIRONMENT=${1:-production}

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

if [ "$ENVIRONMENT" == "production" ]; then
    BASE_URL="http://localhost:80"
    COMPOSE_FILE="docker-compose.prod.yml"
else
    BASE_URL="http://localhost:8080"
    COMPOSE_FILE="docker-compose.staging.yml"
fi

echo "🏥 Running health checks for $ENVIRONMENT environment..."
echo ""

# Check if containers are running
print_message "$YELLOW" "📦 Checking containers..."
RUNNING=$(docker-compose -f "$COMPOSE_FILE" ps --services --filter "status=running" | wc -l)
TOTAL=$(docker-compose -f "$COMPOSE_FILE" ps --services | wc -l)

if [ "$RUNNING" -eq "$TOTAL" ]; then
    print_message "$GREEN" "✅ All containers are running ($RUNNING/$TOTAL)"
else
    print_message "$RED" "❌ Some containers are not running ($RUNNING/$TOTAL)"
    docker-compose -f "$COMPOSE_FILE" ps
    exit 1
fi

echo ""

# Check HTTP endpoint
print_message "$YELLOW" "🌐 Checking HTTP endpoint..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health" || echo "000")

if [ "$HTTP_STATUS" == "200" ]; then
    print_message "$GREEN" "✅ HTTP endpoint is healthy (Status: $HTTP_STATUS)"
else
    print_message "$RED" "❌ HTTP endpoint is unhealthy (Status: $HTTP_STATUS)"
    exit 1
fi

echo ""

# Check disk space
print_message "$YELLOW" "💾 Checking disk space..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -lt 80 ]; then
    print_message "$GREEN" "✅ Disk space is healthy ($DISK_USAGE% used)"
elif [ "$DISK_USAGE" -lt 90 ]; then
    print_message "$YELLOW" "⚠️  Disk space is getting high ($DISK_USAGE% used)"
else
    print_message "$RED" "❌ Disk space is critical ($DISK_USAGE% used)"
    exit 1
fi

echo ""

# Check memory usage
print_message "$YELLOW" "🧠 Checking memory usage..."
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')

if [ "$MEMORY_USAGE" -lt 80 ]; then
    print_message "$GREEN" "✅ Memory usage is healthy ($MEMORY_USAGE% used)"
elif [ "$MEMORY_USAGE" -lt 90 ]; then
    print_message "$YELLOW" "⚠️  Memory usage is getting high ($MEMORY_USAGE% used)"
else
    print_message "$RED" "❌ Memory usage is critical ($MEMORY_USAGE% used)"
fi

echo ""

# Check container logs for errors
print_message "$YELLOW" "📝 Checking for recent errors in logs..."
ERROR_COUNT=$(docker-compose -f "$COMPOSE_FILE" logs --tail=100 | grep -i "error\|exception\|fatal" | wc -l)

if [ "$ERROR_COUNT" -eq 0 ]; then
    print_message "$GREEN" "✅ No recent errors found in logs"
elif [ "$ERROR_COUNT" -lt 5 ]; then
    print_message "$YELLOW" "⚠️  Found $ERROR_COUNT recent errors in logs"
else
    print_message "$RED" "❌ Found $ERROR_COUNT recent errors in logs"
    print_message "$YELLOW" "Recent errors:"
    docker-compose -f "$COMPOSE_FILE" logs --tail=50 | grep -i "error\|exception\|fatal" | tail -5
fi

echo ""
print_message "$GREEN" "✅ Health check completed!"
