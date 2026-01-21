#!/bin/bash
#
# start_lab.sh - Start GasPot HMI Lab Environment
#
# This script starts all containers for the GasPot HMI cybersecurity training lab.
# It handles both Docker Compose V1 and V2, checks for port conflicts, and waits
# for all services to be healthy before displaying access information.
#
# Usage: ./start_lab.sh
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
REQUIRED_PORTS=(10001 5000 3306)
CONTAINERS=(gaspot-historian gaspot-simulator gaspot-hmi)
HEALTH_TIMEOUT=120

# Colors for output (disabled if not a terminal)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect Docker Compose command
detect_compose() {
    if docker compose version &>/dev/null; then
        COMPOSE_CMD="docker compose"
        log_info "Using Docker Compose V2"
    elif docker-compose version &>/dev/null; then
        COMPOSE_CMD="docker-compose"
        log_info "Using Docker Compose V1"
    else
        log_error "Docker Compose not found. Please install Docker Compose."
        exit 1
    fi
}

# Check if Docker daemon is running
check_docker() {
    if ! docker info &>/dev/null; then
        log_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    log_success "Docker daemon is running"
}

# Check for port conflicts
check_ports() {
    local conflicts=0

    for port in "${REQUIRED_PORTS[@]}"; do
        if ss -tuln 2>/dev/null | grep -q ":${port} " || \
           netstat -tuln 2>/dev/null | grep -q ":${port} "; then
            # Check if it's our own container
            local container_using=""
            for container in "${CONTAINERS[@]}"; do
                if docker port "$container" 2>/dev/null | grep -q ":${port}"; then
                    container_using="$container"
                    break
                fi
            done

            if [ -n "$container_using" ]; then
                log_warning "Port $port is in use by existing lab container ($container_using)"
            else
                log_error "Port $port is in use by another process"
                log_error "Run: ss -tuln | grep :$port  to identify the process"
                conflicts=$((conflicts + 1))
            fi
        fi
    done

    if [ $conflicts -gt 0 ]; then
        log_error "Cannot start lab: $conflicts port conflict(s) detected"
        log_error "Free the conflicting ports and try again"
        exit 1
    fi

    log_success "Required ports are available (10001, 5000, 3306)"
}

# Stop and remove existing containers
cleanup_existing() {
    log_info "Checking for existing containers..."

    local existing=0
    for container in "${CONTAINERS[@]}"; do
        if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
            existing=$((existing + 1))
        fi
    done

    if [ $existing -gt 0 ]; then
        log_info "Stopping existing lab containers..."
        cd "$PROJECT_DIR"
        $COMPOSE_CMD down --remove-orphans 2>/dev/null || true
        log_success "Existing containers removed"
    else
        log_info "No existing lab containers found"
    fi
}

# Build and start containers
start_containers() {
    log_info "Building and starting containers..."
    cd "$PROJECT_DIR"

    # Build images
    if ! $COMPOSE_CMD build; then
        log_error "Failed to build containers"
        exit 1
    fi
    log_success "Container images built"

    # Start containers
    if ! $COMPOSE_CMD up -d; then
        log_error "Failed to start containers"
        exit 1
    fi
    log_success "Containers started"
}

# Wait for container to be healthy
wait_for_healthy() {
    local container=$1
    local timeout=$2
    local elapsed=0
    local interval=2

    while [ $elapsed -lt $timeout ]; do
        local status=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "not_found")

        case "$status" in
            healthy)
                return 0
                ;;
            unhealthy)
                log_error "Container $container is unhealthy"
                docker logs --tail=20 "$container" 2>&1 | head -10
                return 1
                ;;
            not_found)
                log_error "Container $container not found"
                return 1
                ;;
        esac

        sleep $interval
        elapsed=$((elapsed + interval))
    done

    log_error "Timeout waiting for $container to be healthy (${timeout}s)"
    return 1
}

# Wait for all containers to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy (timeout: ${HEALTH_TIMEOUT}s)..."

    for container in "${CONTAINERS[@]}"; do
        printf "  Waiting for %-20s " "$container..."
        if wait_for_healthy "$container" "$HEALTH_TIMEOUT"; then
            echo -e "${GREEN}healthy${NC}"
        else
            echo -e "${RED}failed${NC}"
            log_error "Service $container failed to start"
            log_info "Check logs with: docker logs $container"
            exit 1
        fi
    done

    log_success "All services are healthy"
}

# Initialize database if needed
init_database() {
    log_info "Checking database initialization..."

    # Check if tanks table has data
    local tank_count=$(docker exec gaspot-historian mysql -u lab -ppassword historian -N -e "SELECT COUNT(*) FROM tanks;" 2>/dev/null || echo "0")

    if [ "$tank_count" = "0" ] || [ -z "$tank_count" ]; then
        log_info "Initializing database with seed data..."
        if [ -f "$PROJECT_DIR/historian/init.sql" ]; then
            cat "$PROJECT_DIR/historian/init.sql" | docker exec -i gaspot-historian mysql -u lab -ppassword historian
            log_success "Database initialized with seed data"
        else
            log_warning "init.sql not found, database may be empty"
        fi
    else
        log_success "Database already initialized ($tank_count tanks)"
    fi
}

# Display access information
show_access_info() {
    echo ""
    echo "============================================================"
    echo -e "${GREEN}GasPot HMI Lab Started Successfully${NC}"
    echo "============================================================"
    echo ""
    echo "Access Information:"
    echo "-------------------"
    echo ""
    echo "  HMI Dashboard:    http://localhost:5000"
    echo "  GasPot ATG:       localhost:10001 (TLS-350 protocol)"
    echo "  Historian DB:     localhost:3306 (user: lab / pass: password)"
    echo ""
    echo "Quick Test Commands:"
    echo "--------------------"
    echo ""
    echo "  # Test GasPot (get inventory)"
    echo "  echo -e '\\x01I20100\\n' | nc localhost 10001"
    echo ""
    echo "  # Test HMI"
    echo "  curl http://localhost:5000/health"
    echo ""
    echo "  # Test database connection"
    echo "  docker exec gaspot-historian mysqladmin ping -u lab -ppassword"
    echo ""
    echo "  # Interactive database session"
    echo "  docker exec -it gaspot-historian mysql -u lab -ppassword historian"
    echo ""
    echo "Management:"
    echo "-----------"
    echo ""
    echo "  Stop lab:   ./scripts/stop_lab.sh"
    echo "  Reset lab:  ./scripts/reset_lab.sh"
    echo "  View logs:  docker compose logs -f"
    echo ""
    echo "============================================================"
}

# Main execution
main() {
    echo ""
    echo "============================================================"
    echo "Starting GasPot HMI Lab"
    echo "============================================================"
    echo ""

    check_docker
    detect_compose
    check_ports
    cleanup_existing
    start_containers
    wait_for_services
    init_database
    show_access_info
}

main "$@"
