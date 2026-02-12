#!/bin/bash

# Adzanid Installation Script for macOS and Linux
# This script automates the build and installation process

set -e  # Exit on any error

# Check for silent mode flag
SILENT_MODE=false
if [ "$1" = "--silent" ]; then
    SILENT_MODE=true
fi

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
    
    # Prioritize conda/virtual environment Python if active
    if [ -n "$CONDA_DEFAULT_ENV" ] || [ -n "$VIRTUAL_ENV" ]; then
        print_info "Detected active Python environment: ${CONDA_DEFAULT_ENV:-$VIRTUAL_ENV}"
        # Check 'python' command first (common in conda envs)
        if command -v python &> /dev/null; then
            PYTHON_CMD="python"
        elif command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        else
            print_error "Python is not found in the current environment"
            exit 1
        fi
    else
        # No active environment, check system Python
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
    fi
    
    print_success "Python found: $PYTHON_CMD"
    print_info "Python location: $(which $PYTHON_CMD)"
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

# Check and install python3-venv if needed (Linux only)
check_and_install_venv() {
    if [ "$OS" != "linux" ]; then
        return 0
    fi
    
    print_info "Checking for python3-venv package..."
    
    # Try to import venv module
    if $PYTHON_CMD -c "import venv" 2>/dev/null; then
        print_success "python3-venv is already installed"
        return 0
    fi
    
    print_warning "python3-venv is not installed"
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        print_error "python3-venv is required but not installed"
        print_info "Please run this script with sudo, or manually install:"
        print_info "  sudo apt install python3-venv    (Debian/Ubuntu)"
        print_info "  sudo dnf install python3-venv    (Fedora/RHEL)"
        print_info "  sudo pacman -S python            (Arch Linux)"
        exit 1
    fi
    
    # Detect package manager and install
    print_info "Attempting to install python3-venv automatically..."
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        print_info "Detected apt package manager (Debian/Ubuntu)"
        VENV_PACKAGE="python${PYTHON_VERSION}-venv"
        print_info "Installing $VENV_PACKAGE..."
        apt-get update -qq > /dev/null 2>&1
        apt-get install -y "$VENV_PACKAGE" > /dev/null 2>&1 || {
            print_error "Failed to install $VENV_PACKAGE"
            print_info "Run manually: sudo apt-get install $VENV_PACKAGE"
            exit 1
        }
        print_success "Successfully installed $VENV_PACKAGE"
        
    elif command -v dnf &> /dev/null; then
        # Fedora/RHEL
        print_info "Detected dnf package manager (Fedora/RHEL)"
        print_info "Installing python3-venv..."
        dnf install -y python3-venv -q > /dev/null 2>&1 || {
            print_error "Failed to install python3-venv"
            print_info "Run manually: sudo dnf install python3-venv"
            exit 1
        }
        print_success "Successfully installed python3-venv"
        
    elif command -v yum &> /dev/null; then
        # Older RHEL/CentOS
        print_info "Detected yum package manager (RHEL/CentOS)"
        print_info "Installing python3-venv..."
        yum install -y python3-venv -q > /dev/null 2>&1 || {
            print_error "Failed to install python3-venv"
            print_info "Run manually: sudo yum install python3-venv"
            exit 1
        }
        print_success "Successfully installed python3-venv"
        
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        print_info "Detected pacman package manager (Arch Linux)"
        print_info "Installing python..."
        pacman -S --noconfirm python > /dev/null 2>&1 || {
            print_error "Failed to install python"
            print_info "Run manually: sudo pacman -S python"
            exit 1
        }
        print_success "Successfully installed python (includes venv)"
        
    elif command -v zypper &> /dev/null; then
        # openSUSE
        print_info "Detected zypper package manager (openSUSE)"
        print_info "Installing python3-venv..."
        zypper install -y python3-venv > /dev/null 2>&1 || {
            print_error "Failed to install python3-venv"
            print_info "Run manually: sudo zypper install python3-venv"
            exit 1
        }
        print_success "Successfully installed python3-venv"
        
    else
        print_error "Could not detect package manager"
        print_info "Please manually install python3-venv for your distribution"
        exit 1
    fi
    
    # Verify installation
    if $PYTHON_CMD -c "import venv" 2>/dev/null; then
        print_success "python3-venv is now available"
    else
        print_error "Failed to install python3-venv"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists, removing old one..."
        rm -rf venv || {
            print_error "Failed to remove old virtual environment"
            print_info "Please manually delete the 'venv' folder and try again"
            exit 1
        }
    fi
    
    $PYTHON_CMD -m venv venv || {
        print_error "Failed to create virtual environment"
        print_info "This usually means python3-venv is not properly installed"
        if [ "$OS" == "linux" ]; then
            print_info "Try manually running: sudo apt install python${PYTHON_VERSION}-venv"
        fi
        exit 1
    }
    
    print_success "Virtual environment created"
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip -q > /dev/null 2>&1
    
    # Install requirements
    print_info "Installing Python packages (this may take a moment)..."
    pip install -r requirements.txt -q > /dev/null 2>&1 || {
        print_error "Failed to install dependencies from requirements.txt"
        print_info "Check requirements.txt for issues"
        exit 1
    }
    
    # Install PyInstaller
    print_info "Installing PyInstaller..."
    pip install pyinstaller -q > /dev/null 2>&1 || {
        print_error "Failed to install PyInstaller"
        exit 1
    }
    
    print_success "Dependencies installed"
}

# Clean build directories
clean_build_dirs() {
    print_info "Cleaning previous build artifacts..."
    
    # Remove dist folder if it exists
    if [ -d "dist" ]; then
        print_info "Removing dist/ folder..."
        rm -rf dist
    fi
    
    # Remove build folder if it exists
    if [ -d "build" ]; then
        print_info "Removing build/ folder..."
        rm -rf build
    fi
    
    # Remove spec file if it exists
    if [ -f "Adzanid.spec" ]; then
        print_info "Removing old spec file..."
        rm -f Adzanid.spec
    fi
    
    print_success "Build directories cleaned"
}

# Build the application with PyInstaller
build_app() {
    print_info "Building application with PyInstaller (this may take a few minutes)..."
    
    # Ensure we're in the virtual environment
    source venv/bin/activate
    
    # Build the application
    if [ "$OS" == "macos" ]; then
        pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py > /dev/null 2>&1 || {
            print_error "PyInstaller build failed"
            print_info "Re-run without redirection to see detailed errors:"
            print_info "  pyinstaller --name Adzanid --windowed --icon=assets/icon.png --add-data assets:assets main.py"
            exit 1
        }
    else
        pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py > /dev/null 2>&1 || {
            print_error "PyInstaller build failed"
            print_info "Re-run without redirection to see detailed errors:"
            print_info "  pyinstaller --name Adzanid --windowed --icon=assets/icon.png --add-data assets:assets main.py"
            exit 1
        }
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
        print_error "System installation requires root privileges"
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
    
    # Create wrapper script in /usr/local/bin (instead of symlink to fix asset paths)
    print_info "Creating launcher script in /usr/local/bin..."
    cat > /usr/local/bin/adzanid << 'EOF'
#!/bin/bash
# Adzanid launcher wrapper
# This ensures the app runs from its installation directory to correctly resolve asset paths
cd /opt/adzanid
exec ./Adzanid "$@"
EOF
    chmod +x /usr/local/bin/adzanid
    
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
        print_info "Updating desktop database..."
        update-desktop-database /usr/share/applications > /dev/null 2>&1
    fi
    
    print_success "Adzanid installed successfully!"
    print_info "You can now run 'adzanid' from the command line or find it in your application menu"
}

# Install for macOS
install_macos() {
    print_info "Installing Adzanid for macOS..."
    
    # Check if running as root for installation
    if [ "$EUID" -ne 0 ]; then
        print_error "System installation requires root privileges"
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
    
    # Create wrapper script for command-line access (instead of symlink to fix asset paths)
    print_info "Creating launcher script in /usr/local/bin..."
    cat > /usr/local/bin/adzanid << 'EOF'
#!/bin/bash
# Adzanid launcher wrapper for macOS
# This ensures the app runs from its bundle directory to correctly resolve asset paths
cd "/Applications/Adzanid.app/Contents/MacOS"
exec ./Adzanid "$@"
EOF
    chmod +x /usr/local/bin/adzanid
    
    print_success "Adzanid installed successfully!"
    print_info "You can now find Adzanid in your Applications folder or run 'adzanid' from the terminal"
}

# Main installation process
main() {
    if [ "$SILENT_MODE" = false ]; then
        echo ""
        echo "╔═══════════════════════════════════════════════════════╗"
        echo "║        Adzanid Installation Script v1.0               ║"
        echo "║    Prayer Times Application for Indonesian Cities     ║"
        echo "╚═══════════════════════════════════════════════════════╝"
        echo ""
    fi
    
    # Detect OS
    detect_os
    
    # Check for root privileges early
    if [ "$EUID" -ne 0 ]; then
        print_warning "This script should be run with sudo for full installation"
        print_info "Running: sudo ./install.sh"
        print_info "This ensures:"
        print_info "  - Automatic installation of system dependencies (python3-venv)"
        print_info "  - Proper system-wide installation to /opt or /Applications"
        print_info "  - Creation of desktop entries and command-line shortcuts"
        echo ""
        print_error "Please run: sudo ./install.sh"
        exit 1
    fi
    
    # Check Python
    check_python
    validate_python_version
    check_and_install_venv
    
    # Build application
    print_info "Starting build process..."
    create_venv
    install_dependencies
    clean_build_dirs
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
    
    if [ "$SILENT_MODE" = false ]; then
        echo ""
        echo "╔═══════════════════════════════════════════════════════╗"
        echo "║              Installation Complete! 🎉                ║"
        echo "╚═══════════════════════════════════════════════════════╝"
        echo ""
        print_info "Thank you for installing Adzanid!"
        print_info "Made with ❤️ for the Muslim community in Indonesia"
        echo ""
    fi
}

# Check if script is being run from the correct directory
if [ ! -f "main.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "This script must be run from the adzanid project root directory"
    print_info "Please cd to the directory containing main.py and try again"
    exit 1
fi

# Run main installation
main
