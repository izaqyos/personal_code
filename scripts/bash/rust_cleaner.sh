#!/bin/bash

# Rust Cargo Project Cleaner
# Recursively scans for Cargo projects and runs cargo clean
# Usage: ./rust_cleaner.sh <path>

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
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

# Function to check if a directory is a Cargo project
is_cargo_project() {
    local dir="$1"
    [[ -f "$dir/Cargo.toml" ]]
}

# Function to clean a cargo project
clean_cargo_project() {
    local project_path="$1"
    local project_name=$(basename "$project_path")
    
    print_status "Cleaning Cargo project: $project_name ($project_path)"
    
    if cd "$project_path" && cargo clean 2>/dev/null; then
        print_success "Successfully cleaned: $project_name"
        return 0
    else
        print_error "Failed to clean: $project_name"
        return 1
    fi
}

# Main function
main() {
    local search_path="${1:-}"
    
    # Validate input
    if [[ -z "$search_path" ]]; then
        echo "Usage: $0 <path>"
        echo "  <path>: Directory to scan for Rust Cargo projects"
        exit 1
    fi
    
    if [[ ! -d "$search_path" ]]; then
        print_error "Directory '$search_path' does not exist"
        exit 1
    fi
    
    # Check if cargo is installed
    if ! command -v cargo &> /dev/null; then
        print_error "cargo command not found. Please install Rust/Cargo first."
        exit 1
    fi
    
    # Convert to absolute path
    search_path=$(realpath "$search_path")
    
    print_status "Starting scan for Rust Cargo projects in: $search_path"
    echo
    
    # Arrays to store results
    declare -a cleaned_projects=()
    declare -a failed_projects=()
    declare -a all_projects=()
    
    # Store original directory
    original_dir=$(pwd)
    
    # Find all Cargo.toml files and process them
    while IFS= read -r -d '' cargo_file; do
        project_dir=$(dirname "$cargo_file")
        project_name=$(basename "$project_dir")
        
        # Skip if it's a workspace member (has a parent Cargo.toml)
        # This prevents cleaning the same project multiple times
        parent_dir=$(dirname "$project_dir")
        if [[ "$parent_dir" != "$project_dir" ]] && is_cargo_project "$parent_dir"; then
            # Check if parent is a workspace
            if grep -q "^\[workspace\]" "$parent_dir/Cargo.toml" 2>/dev/null; then
                print_warning "Skipping workspace member: $project_name (will be cleaned with workspace)"
                continue
            fi
        fi
        
        all_projects+=("$project_dir")
        
        if clean_cargo_project "$project_dir"; then
            cleaned_projects+=("$project_dir")
        else
            failed_projects+=("$project_dir")
        fi
        
        # Return to original directory
        cd "$original_dir"
        
    done < <(find "$search_path" -name "Cargo.toml" -type f -print0)
    
    # Generate report
    echo
    echo "=================================================="
    echo "              CLEANUP REPORT"
    echo "=================================================="
    echo
    
    if [[ ${#all_projects[@]} -eq 0 ]]; then
        print_warning "No Cargo projects found in $search_path"
    else
        echo "📊 Total Cargo projects found: ${#all_projects[@]}"
        echo "✅ Successfully cleaned: ${#cleaned_projects[@]}"
        echo "❌ Failed to clean: ${#failed_projects[@]}"
        echo
        
        if [[ ${#cleaned_projects[@]} -gt 0 ]]; then
            echo "🧹 Cleaned Projects:"
            for project in "${cleaned_projects[@]}"; do
                echo "  ✓ $(basename "$project") ($project)"
            done
            echo
        fi
        
        if [[ ${#failed_projects[@]} -gt 0 ]]; then
            echo "⚠️  Failed Projects:"
            for project in "${failed_projects[@]}"; do
                echo "  ✗ $(basename "$project") ($project)"
            done
            echo
        fi
    fi
    
    # Calculate and display space savings (approximate)
    echo "💾 Build artifacts cleaned from target/ directories"
    echo "📁 Scan completed for: $search_path"
    
    # Exit with appropriate code
    # Exit 1 only if ALL projects failed or no projects were found and we expected some
    if [[ ${#all_projects[@]} -eq 0 ]]; then
        # No projects found - this is success (nothing to clean)
        exit 0
    elif [[ ${#cleaned_projects[@]} -eq 0 ]]; then
        # All projects failed to clean
        exit 1
    else
        # At least some projects were cleaned successfully
        exit 0
    fi
}

# Run main function with all arguments
main "$@"
