#!/bin/bash
#
# stop_lab.sh - Stop GasPot HMI Lab Environment
#
# This script cleanly stops all containers for the GasPot HMI lab.
# Data volumes are preserved for later use.
#
# Usage: ./stop_lab.sh
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONTAINERS=(gaspot-historian gaspot-simulator gaspot-hmi)

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
    elif docker-compose version &>/dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        log_error "Docker Compose not found. Please install Docker Compose."
        exit 1
    fi
}

# Check if any lab containers are running
check_running() {
    local running=0
    for container in "${CONTAINERS[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
            running=$((running + 1))
        fi
    done
    echo $running
}

# Stop containers
stop_containers() {
    log_info "Stopping GasPot HMI Lab containers..."
    cd "$PROJECT_DIR"

    if ! $COMPOSE_CMD down --remove-orphans; then
        log_error "Failed to stop containers"
        exit 1
    fi
}

# Verify containers stopped
verify_stopped() {
    local remaining=$(check_running)
    if [ "$remaining" -gt 0 ]; then
        log_warning "$remaining container(s) still running"
        log_info "Forcing removal..."
        for container in "${CONTAINERS[@]}"; do
            docker rm -f "$container" 2>/dev/null || true
        done
    fi
}

# Main execution
main() {
    echo ""
    echo "============================================================"
    echo "Stopping GasPot HMI Lab"
    echo "============================================================"
    echo ""

    detect_compose

    local running=$(check_running)
    if [ "$running" -eq 0 ]; then
        log_info "No lab containers are currently running"
        echo ""
        echo "To start the lab, run: ./scripts/start_lab.sh"
        echo ""
        exit 0
    fi

    log_info "Found $running running container(s)"
    stop_containers
    verify_stopped

    echo ""
    log_success "GasPot HMI Lab stopped"
    echo ""
    echo "  Data volumes preserved. To restart: ./scripts/start_lab.sh"
    echo "  To fully reset (delete data):       ./scripts/reset_lab.sh"
    echo ""
}

main "$@"
