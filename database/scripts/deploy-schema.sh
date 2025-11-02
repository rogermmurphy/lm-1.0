#!/bin/bash
# Deploy Little Monster Database Schema
# Usage: ./deploy-schema.sh [environment]
# Environments: dev, prod

set -e  # Exit on error

ENVIRONMENT=${1:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_DIR="$SCRIPT_DIR/../schemas"

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Database connection parameters
if [ "$ENVIRONMENT" = "prod" ]; then
    DB_HOST=${DB_HOST:-"localhost"}
    DB_PORT=${DB_PORT:-5432}
    DB_NAME=${DB_NAME:-"littlemonster"}
    DB_USER=${DB_USER:-"postgres"}
else
    DB_HOST=${DB_HOST:-"localhost"}
    DB_PORT=${DB_PORT:-5432}
    DB_NAME=${DB_NAME:-"littlemonster_dev"}
    DB_USER=${DB_USER:-"postgres"}
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Little Monster Database Schema Deployment${NC}"
echo -e "${YELLOW}Environment: $ENVIRONMENT${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Check if PostgreSQL client is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}ERROR: psql command not found. Please install PostgreSQL client.${NC}"
    exit 1
fi

# Check if master-schema.sql exists
if [ ! -f "$SCHEMA_DIR/master-schema.sql" ]; then
    echo -e "${RED}ERROR: master-schema.sql not found in $SCHEMA_DIR${NC}"
    exit 1
fi

# Test database connection
echo -e "${YELLOW}Testing database connection...${NC}"
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c '\q' 2>/dev/null; then
    echo -e "${RED}ERROR: Cannot connect to PostgreSQL server${NC}"
    echo "Please ensure PostgreSQL is running and credentials are correct."
    exit 1
fi
echo -e "${GREEN}✓ Database connection successful${NC}"
echo ""

# Create database if it doesn't exist
echo -e "${YELLOW}Checking if database '$DB_NAME' exists...${NC}"
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
    echo -e "${YELLOW}Creating database '$DB_NAME'...${NC}"
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${GREEN}✓ Database already exists${NC}"
fi
echo ""

# Deploy schema
echo -e "${YELLOW}Deploying master schema...${NC}"
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$SCHEMA_DIR/master-schema.sql"; then
    echo -e "${GREEN}✓ Schema deployed successfully${NC}"
else
    echo -e "${RED}ERROR: Schema deployment failed${NC}"
    exit 1
fi
echo ""

# Verify deployment
echo -e "${YELLOW}Verifying deployment...${NC}"
TABLE_COUNT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
echo -e "Tables created: ${GREEN}$TABLE_COUNT${NC}"

if [ "$TABLE_COUNT" -ge 12 ]; then
    echo -e "${GREEN}✓ Deployment verification successful${NC}"
else
    echo -e "${YELLOW}WARNING: Expected at least 12 tables, found $TABLE_COUNT${NC}"
fi
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Schema deployment completed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Database Details:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo ""
echo "Next steps:"
echo "  1. Verify tables: psql -U $DB_USER -d $DB_NAME -c '\\dt'"
echo "  2. Run seed data (if available)"
echo "  3. Test with service connections"
