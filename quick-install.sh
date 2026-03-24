#!/bin/bash

# Adzanid Quick Installation Script
# This script downloads and installs Adzanid in a single command

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
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

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This installation requires root privileges"
        echo ""
        print_info "Please run with sudo -E to preserve environment variables:"
        print_info "  curl -fsSL https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash"
        echo ""
        print_info "Or with wget:"
        print_info "  wget -qO- https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash"
        echo ""
        print_warning "The -E flag is important if you're using conda/virtualenv"
        exit 1
    fi
}

# Check if running under sudo without preserved environment
check_sudo_environment() {
    # If we're root and SUDO_USER is set, we're under sudo
    if [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
        # Check if conda or virtualenv might be available for the original user
        local user_home=$(eval echo ~$SUDO_USER)
        
        # Check if conda is installed for the user
        if [ -f "$user_home/.conda/environments.txt" ] || [ -d "$user_home/miniconda3" ] || [ -d "$user_home/anaconda3" ] || [ -f "$user_home/.condarc" ]; then
            # Conda is installed but environment vars are not preserved
            if [ -z "$CONDA_DEFAULT_ENV" ] && [ -z "$CONDA_PREFIX" ]; then
                print_error "Conda detected but environment not preserved under sudo"
                print_info "You have conda installed, but environment variables are not preserved."
                echo ""
                print_info "Please re-run with -E flag to preserve your conda environment:"
                echo ""
                print_info "  Using curl:"
                print_info "    curl -fsSL https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash"
                echo ""
                print_info "  Using wget:"
                print_info "    wget -qO- https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash"
                echo ""
                print_warning "The -E flag preserves your active conda environment (e.g., Python 3.12)"
                exit 1
            fi
        fi
    fi
}

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed on your system"
        echo ""
        print_info "Please install Git first:"
        print_info "  macOS:   brew install git"
        print_info "  Ubuntu:  sudo apt install git"
        print_info "  Fedora:  sudo dnf install git"
        print_info "  Arch:    sudo pacman -S git"
        exit 1
    fi
}

# Main installation function
main() {
    clear
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║      Adzanid Quick Installation Script v1.0           ║"
    echo "║    Prayer Times Application for Indonesian Cities     ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Check prerequisites
    check_root
    check_sudo_environment
    check_git
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    print_info "Using temporary directory: $TEMP_DIR"
    
    # Clone repository
    print_info "Cloning Adzanid repository..."
    if git clone --quiet https://github.com/fikrisyahid/adzanid.git "$TEMP_DIR/adzanid" 2>/dev/null; then
        print_success "Repository cloned successfully"
    else
        print_error "Failed to clone repository"
        print_info "Please check your internet connection and try again"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
    
    echo ""
    print_info "Starting installation process..."
    echo ""
    
    # Change to repository directory
    cd "$TEMP_DIR/adzanid"
    
    # Make install script executable
    chmod +x install.sh
    
    # Run installation script in silent mode
    if ./install.sh --silent; then
        INSTALL_SUCCESS=true
    else
        INSTALL_SUCCESS=false
    fi
    
    # Return to original directory
    cd - > /dev/null 2>&1
    
    # Clean up
    print_info "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    print_success "Cleanup completed"
    
    # Check installation result
    if [ "$INSTALL_SUCCESS" = true ]; then
        echo ""
        echo "╔═══════════════════════════════════════════════════════╗"
        echo "║         Installation Completed Successfully! 🎉       ║"
        echo "╚═══════════════════════════════════════════════════════╝"
        echo ""
        
        # Detect OS for final instructions
        if [[ "$OSTYPE" == "darwin"* ]]; then
            print_success "Adzanid has been installed to /Applications/Adzanid.app"
            echo ""
            print_info "To launch Adzanid:"
            echo -e "  ${CYAN}•${NC} Open from Applications folder"
            echo -e "  ${CYAN}•${NC} Run ${CYAN}adzanid${NC} from terminal"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            print_success "Adzanid has been installed to /opt/adzanid"
            echo ""
            print_info "To launch Adzanid:"
            echo -e "  ${CYAN}•${NC} Find it in your application menu"
            echo -e "  ${CYAN}•${NC} Run ${CYAN}adzanid${NC} from terminal"
        fi
        
        echo ""
        print_info "Thank you for installing Adzanid!"
        print_info "Made with ❤️  for the Muslim community in Indonesia"
        echo ""
        print_warning "First-time setup: Select your city in Settings tab"
        echo ""
    else
        echo ""
        print_error "Installation failed"
        print_info "Please check the error messages above"
        echo ""
        print_info "For manual installation, visit:"
        print_info "  https://github.com/fikrisyahid/adzanid"
        exit 1
    fi
}

# Run main function
main
