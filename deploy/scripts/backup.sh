#!/bin/bash

# Backup script for AnancyIO
# Usage: ./backup.sh [environment]

set -e

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

print_message "$GREEN" "💾 Creating backup for $ENVIRONMENT environment..."

mkdir -p "$BACKUP_DIR"

# Determine volume names based on environment
if [ "$ENVIRONMENT" == "production" ]; then
    DATA_VOLUME="anancyio-data"
    LOGS_VOLUME="anancyio-logs"
    MEMORY_VOLUME="anancyio-memory"
    KNOWLEDGE_VOLUME="anancyio-knowledge"
else
    DATA_VOLUME="anancyio-staging-data"
    LOGS_VOLUME="anancyio-staging-logs"
    MEMORY_VOLUME="anancyio-staging-memory"
    KNOWLEDGE_VOLUME="anancyio-staging-knowledge"
fi

# Backup data volume
print_message "$YELLOW" "Backing up data volume..."
docker run --rm \
    -v "$DATA_VOLUME":/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf /backup/data.tar.gz -C /data . 2>/dev/null || true

# Backup logs volume
print_message "$YELLOW" "Backing up logs volume..."
docker run --rm \
    -v "$LOGS_VOLUME":/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf /backup/logs.tar.gz -C /data . 2>/dev/null || true

# Backup memory volume
print_message "$YELLOW" "Backing up memory volume..."
docker run --rm \
    -v "$MEMORY_VOLUME":/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf /backup/memory.tar.gz -C /data . 2>/dev/null || true

# Backup knowledge volume
print_message "$YELLOW" "Backing up knowledge volume..."
docker run --rm \
    -v "$KNOWLEDGE_VOLUME":/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf /backup/knowledge.tar.gz -C /data . 2>/dev/null || true

# Create metadata file
cat > "$BACKUP_DIR/metadata.txt" << EOF
Backup Date: $(date)
Environment: $ENVIRONMENT
Hostname: $(hostname)
Docker Version: $(docker --version)
EOF

print_message "$GREEN" "✅ Backup completed: $BACKUP_DIR"

# Clean up old backups (keep last 7 days)
print_message "$YELLOW" "Cleaning up old backups..."
find "$PROJECT_ROOT/backups" -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
print_message "$GREEN" "📦 Backup size: $BACKUP_SIZE"

# List recent backups
print_message "$GREEN" "📋 Recent backups:"
ls -lht "$PROJECT_ROOT/backups" | head -6
