#!/bin/bash

# Adzanid Uninstallation Script for macOS and Linux
# This script removes all installed components of Adzanid

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_info "Detected operating system: macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_info "Detected operating system: Linux"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check for root privileges
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run with root privileges"
        print_info "Please run: sudo ./uninstall.sh"
        exit 1
    fi
}

# Uninstall for Linux
uninstall_linux() {
    print_info "Uninstalling Adzanid from Linux..."
    
    local FOUND=false
    
    # Remove installation directory
    if [ -d "/opt/adzanid" ]; then
        print_info "Removing /opt/adzanid..."
        rm -rf /opt/adzanid
        print_success "Installation directory removed"
        FOUND=true
    else
        print_warning "Installation directory /opt/adzanid not found"
    fi
    
    # Remove launcher script
    if [ -f "/usr/local/bin/adzanid" ]; then
        print_info "Removing launcher script..."
        rm -f /usr/local/bin/adzanid
        print_success "Launcher script removed"
        FOUND=true
    else
        print_warning "Launcher script /usr/local/bin/adzanid not found"
    fi
    
    # Remove desktop entry
    if [ -f "/usr/share/applications/adzanid.desktop" ]; then
        print_info "Removing desktop entry..."
        rm -f /usr/share/applications/adzanid.desktop
        print_success "Desktop entry removed"
        FOUND=true
        
        # Update desktop database
        if command -v update-desktop-database &> /dev/null; then
            print_info "Updating desktop database..."
            update-desktop-database /usr/share/applications > /dev/null 2>&1
        fi
    else
        print_warning "Desktop entry /usr/share/applications/adzanid.desktop not found"
    fi
    
    # Check for user autostart entries (optional cleanup)
    local REMOVED_USER_AUTOSTART=false
    for user_home in /home/*; do
        if [ -d "$user_home" ]; then
            local autostart_file="$user_home/.config/autostart/adzanid.desktop"
            if [ -f "$autostart_file" ]; then
                print_info "Removing autostart entry for user: $(basename $user_home)"
                rm -f "$autostart_file"
                REMOVED_USER_AUTOSTART=true
            fi
        fi
    done
    
    if [ "$REMOVED_USER_AUTOSTART" = true ]; then
        print_success "User autostart entries removed"
        FOUND=true
    fi
    
    if [ "$FOUND" = false ]; then
        print_warning "No Adzanid installation found on this system"
        return 1
    fi
    
    print_success "Adzanid has been completely uninstalled from Linux"
}

# Uninstall for macOS
uninstall_macos() {
    print_info "Uninstalling Adzanid from macOS..."
    
    local FOUND=false
    
    # Remove application bundle
    if [ -d "/Applications/Adzanid.app" ]; then
        print_info "Removing /Applications/Adzanid.app..."
        rm -rf /Applications/Adzanid.app
        print_success "Application bundle removed"
        FOUND=true
    else
        print_warning "Application bundle /Applications/Adzanid.app not found"
    fi
    
    # Remove launcher script
    if [ -f "/usr/local/bin/adzanid" ]; then
        print_info "Removing launcher script..."
        rm -f /usr/local/bin/adzanid
        print_success "Launcher script removed"
        FOUND=true
    else
        print_warning "Launcher script /usr/local/bin/adzanid not found"
    fi
    
    # Check for user LaunchAgents (optional cleanup)
    local REMOVED_USER_LAUNCHAGENT=false
    for user_home in /Users/*; do
        if [ -d "$user_home" ]; then
            local launchagent_file="$user_home/Library/LaunchAgents/com.fikrisyahid.adzanid.plist"
            if [ -f "$launchagent_file" ]; then
                print_info "Removing LaunchAgent for user: $(basename $user_home)"
                rm -f "$launchagent_file"
                REMOVED_USER_LAUNCHAGENT=true
            fi
        fi
    done
    
    if [ "$REMOVED_USER_LAUNCHAGENT" = true ]; then
        print_success "User LaunchAgent entries removed"
        FOUND=true
    fi
    
    if [ "$FOUND" = false ]; then
        print_warning "No Adzanid installation found on this system"
        return 1
    fi
    
    print_success "Adzanid has been completely uninstalled from macOS"
}

# Main uninstallation process
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║       Adzanid Uninstallation Script v1.0             ║"
    echo "║    Prayer Times Application for Indonesian Cities     ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Detect OS
    detect_os
    
    # Check for root privileges
    check_root
    
    # Confirm uninstallation
    echo ""
    print_warning "This will completely remove Adzanid from your system"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
    
    echo ""
    print_info "Starting uninstallation..."
    echo ""
    
    # Uninstall based on OS
    if [ "$OS" == "linux" ]; then
        uninstall_linux
    elif [ "$OS" == "macos" ]; then
        uninstall_macos
    fi
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║           Uninstallation Complete! ✓                 ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    print_info "Adzanid has been removed from your system"
    print_info "User settings and configurations are preserved in:"
    
    if [ "$OS" == "linux" ]; then
        print_info "  ~/.config/Adzanid/ (can be manually deleted if desired)"
    elif [ "$OS" == "macos" ]; then
        print_info "  ~/Library/Preferences/com.fikrisyahid.adzanid.plist"
        print_info "  ~/Library/Application Support/Adzanid/"
    fi
    
    echo ""
    print_info "Thank you for using Adzanid!"
    echo ""
}

# Run main uninstallation
main
