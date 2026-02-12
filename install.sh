#!/bin/bash

# Adzanid Installation Script for macOS and Linux
# This script automates the build and installation process

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

# Check if Python is installed
check_python() {
    print_info "Checking for Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed on your system"
        print_info "Please install Python 3.10 or higher (but less than 3.13)"
        print_info "Visit: https://www.python.org/downloads/"
        exit 1
    fi
    
    print_success "Python found: $PYTHON_CMD"
}

# Validate Python version
validate_python_version() {
    print_info "Validating Python version..."
    
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
    
    print_info "Python version: $PYTHON_VERSION"
    
    # Check if version is >= 3.10
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        print_error "Python version must be 3.10 or higher"
        print_info "Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    # Check if version is < 3.13
    if [ "$PYTHON_MAJOR" -gt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]); then
        print_error "Python version must be less than 3.13 for PyInstaller compatibility"
        print_info "Current version: $PYTHON_VERSION"
        print_info "Please use Python 3.10, 3.11, or 3.12"
        exit 1
    fi
    
    print_success "Python version is compatible: $PYTHON_VERSION"
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists, removing old one..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    # Install PyInstaller
    pip install pyinstaller
    
    print_success "Dependencies installed"
}

# Build the application with PyInstaller
build_app() {
    print_info "Building application with PyInstaller..."
    
    # Ensure we're in the virtual environment
    source venv/bin/activate
    
    # Build the application
    if [ "$OS" == "macos" ]; then
        pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py
    else
        pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py
    fi
    
    print_success "Application built successfully"
}

# Copy assets folder to dist
copy_assets() {
    print_info "Copying assets folder to dist directory..."
    
    if [ ! -d "dist/Adzanid" ]; then
        print_error "dist/Adzanid directory not found. Build may have failed."
        exit 1
    fi
    
    # Remove existing assets folder in dist if it exists
    if [ -d "dist/Adzanid/assets" ]; then
        rm -rf dist/Adzanid/assets
    fi
    
    # Copy assets folder
    cp -r assets dist/Adzanid/
    
    print_success "Assets copied to dist/Adzanid/"
}

# Install for Linux
install_linux() {
    print_info "Installing Adzanid for Linux..."
    
    # Check if running as root for installation
    if [ "$EUID" -ne 0 ]; then
        print_error "This installation requires root privileges"
        print_info "Please run: sudo ./install.sh"
        exit 1
    fi
    
    # Create installation directory
    INSTALL_DIR="/opt/adzanid"
    print_info "Installing to $INSTALL_DIR"
    
    # Remove old installation if exists
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Removing previous installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Copy application
    mkdir -p "$INSTALL_DIR"
    cp -r dist/Adzanid/* "$INSTALL_DIR/"
    
    # Make executable
    chmod +x "$INSTALL_DIR/Adzanid"
    
    # Create symbolic link in /usr/local/bin
    print_info "Creating symbolic link in /usr/local/bin..."
    ln -sf "$INSTALL_DIR/Adzanid" /usr/local/bin/adzanid
    
    # Create desktop entry
    print_info "Creating desktop entry..."
    cat > /usr/share/applications/adzanid.desktop << EOF
[Desktop Entry]
Version=1.1
Type=Application
Name=Adzanid
Comment=Desktop prayer times application for Indonesian cities
Exec=/opt/adzanid/Adzanid
Icon=/opt/adzanid/assets/icon.png
Terminal=false
Categories=Utility;
Keywords=prayer;islam;adhan;sholat;
EOF
    
    chmod 644 /usr/share/applications/adzanid.desktop
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database /usr/share/applications
    fi
    
    print_success "Adzanid installed successfully!"
    print_info "You can now run 'adzanid' from the command line or find it in your application menu"
}

# Install for macOS
install_macos() {
    print_info "Installing Adzanid for macOS..."
    
    # Check if running as root for installation
    if [ "$EUID" -ne 0 ]; then
        print_error "This installation requires root privileges"
        print_info "Please run: sudo ./install.sh"
        exit 1
    fi
    
    # Create .app bundle structure if not exists
    APP_NAME="Adzanid.app"
    INSTALL_DIR="/Applications/$APP_NAME"
    
    print_info "Installing to $INSTALL_DIR"
    
    # Remove old installation if exists
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Removing previous installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Create app bundle structure
    mkdir -p "$INSTALL_DIR/Contents/MacOS"
    mkdir -p "$INSTALL_DIR/Contents/Resources"
    
    # Copy application files
    cp -r dist/Adzanid/* "$INSTALL_DIR/Contents/MacOS/"
    
    # Copy icon
    if [ -f "assets/icon.png" ]; then
        cp assets/icon.png "$INSTALL_DIR/Contents/Resources/"
    fi
    
    # Create Info.plist
    print_info "Creating Info.plist..."
    cat > "$INSTALL_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Adzanid</string>
    <key>CFBundleIconFile</key>
    <string>icon.png</string>
    <key>CFBundleIdentifier</key>
    <string>com.fikrisyahid.adzanid</string>
    <key>CFBundleName</key>
    <string>Adzanid</string>
    <key>CFBundleDisplayName</key>
    <string>Adzanid</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
    
    # Make executable
    chmod +x "$INSTALL_DIR/Contents/MacOS/Adzanid"
    
    # Set ownership
    chown -R root:wheel "$INSTALL_DIR"
    
    # Create command-line alias
    print_info "Creating command-line alias..."
    ln -sf "$INSTALL_DIR/Contents/MacOS/Adzanid" /usr/local/bin/adzanid
    
    print_success "Adzanid installed successfully!"
    print_info "You can now find Adzanid in your Applications folder or run 'adzanid' from the terminal"
}

# Main installation process
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║        Adzanid Installation Script v1.0               ║"
    echo "║    Prayer Times Application for Indonesian Cities     ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Detect OS
    detect_os
    
    # Check Python
    check_python
    validate_python_version
    
    # Build application
    print_info "Starting build process..."
    create_venv
    install_dependencies
    build_app
    copy_assets
    
    # Deactivate virtual environment
    deactivate 2>/dev/null || true
    
    print_success "Build process completed!"
    echo ""
    
    # Install based on OS
    print_info "Starting system installation..."
    echo ""
    
    if [ "$OS" == "linux" ]; then
        install_linux
    elif [ "$OS" == "macos" ]; then
        install_macos
    fi
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║              Installation Complete! 🎉                ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    print_info "Thank you for installing Adzanid!"
    print_info "Made with ❤️ for the Muslim community in Indonesia"
    echo ""
}

# Check if script is being run from the correct directory
if [ ! -f "main.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "This script must be run from the adzanid project root directory"
    print_info "Please cd to the directory containing main.py and try again"
    exit 1
fi

# Run main installation
main
