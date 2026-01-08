#!/bin/bash
#
# reset_lab.sh - Reset GasPot HMI Lab Environment
#
# This script performs a complete reset of the GasPot HMI lab:
# - Stops all containers
# - Removes all data volumes
# - Optionally removes container images
#
# Usage: ./reset_lab.sh [--full]
#
# Options:
#   --full    Also remove container images (requires rebuild on next start)
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONTAINERS=(gaspot-historian gaspot-simulator gaspot-hmi)
VOLUMES=(gaspot-hmi-lab_historian-data)
IMAGES=(gaspot-hmi-lab-gaspot-simulator gaspot-hmi-lab-gaspot-hmi)

# Parse arguments
FULL_RESET=false
if [ "$1" = "--full" ]; then
    FULL_RESET=true
fi

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

# Confirm reset with user
confirm_reset() {
    echo ""
    echo -e "${YELLOW}WARNING: This will delete all lab data!${NC}"
    echo ""
    echo "The following will be removed:"
    echo "  - All lab containers"
    echo "  - Database volume (all historian data)"
    if [ "$FULL_RESET" = true ]; then
        echo "  - Container images (will require rebuild)"
    fi
    echo ""

    # Check if running interactively
    if [ -t 0 ]; then
        read -p "Are you sure you want to reset the lab? [y/N] " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Reset cancelled"
            exit 0
        fi
    else
        log_warning "Running non-interactively, proceeding with reset"
    fi
}

# Stop and remove containers
remove_containers() {
    log_info "Stopping and removing containers..."
    cd "$PROJECT_DIR"

    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true

    # Force remove any remaining containers
    for container in "${CONTAINERS[@]}"; do
        if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
            docker rm -f "$container" 2>/dev/null || true
        fi
    done

    log_success "Containers removed"
}

# Remove volumes
remove_volumes() {
    log_info "Removing data volumes..."
    cd "$PROJECT_DIR"

    # Remove via compose
    $COMPOSE_CMD down -v 2>/dev/null || true

    # Also try to remove named volumes directly
    for volume in "${VOLUMES[@]}"; do
        if docker volume ls --format '{{.Name}}' | grep -q "^${volume}$"; then
            docker volume rm "$volume" 2>/dev/null || true
        fi
    done

    # Remove any volumes matching the project pattern
    docker volume ls --format '{{.Name}}' | grep "gaspot-hmi-lab" | while read vol; do
        docker volume rm "$vol" 2>/dev/null || true
    done

    log_success "Data volumes removed"
}

# Remove images (optional)
remove_images() {
    if [ "$FULL_RESET" = true ]; then
        log_info "Removing container images..."

        for image in "${IMAGES[@]}"; do
            if docker images --format '{{.Repository}}' | grep -q "^${image}$"; then
                docker rmi "$image" 2>/dev/null || true
            fi
        done

        # Also try project-prefixed images
        docker images --format '{{.Repository}}:{{.Tag}}' | grep "gaspot-hmi-lab" | while read img; do
            docker rmi "$img" 2>/dev/null || true
        done

        log_success "Container images removed"
    fi
}

# Clean up dangling resources
cleanup_dangling() {
    log_info "Cleaning up dangling resources..."

    # Remove dangling images
    docker image prune -f &>/dev/null || true

    # Remove unused networks
    docker network prune -f &>/dev/null || true

    log_success "Cleanup complete"
}

# Main execution
main() {
    echo ""
    echo "============================================================"
    echo "Resetting GasPot HMI Lab"
    echo "============================================================"

    detect_compose
    confirm_reset

    echo ""
    remove_containers
    remove_volumes
    remove_images
    cleanup_dangling

    echo ""
    log_success "GasPot HMI Lab has been reset"
    echo ""
    echo "  To start fresh: ./scripts/start_lab.sh"
    echo ""
    if [ "$FULL_RESET" = true ]; then
        echo "  Note: Images were removed. First start will rebuild containers."
        echo ""
    fi
}

main "$@"
