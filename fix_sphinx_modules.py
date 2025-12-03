"""
Script to fix module names in Sphinx-generated .rst files.
Removes the directory name prefix from module references.
"""
import os
import re
import glob

# Directory containing the .rst files
source_dir = "docs/source"

# Pattern to match: Bus-Transportation-Management-System-main.module_name
pattern = r'Bus-Transportation-Management-System-main\.'
replacement = ''

# Find all .rst files
rst_files = glob.glob(os.path.join(source_dir, "*.rst"))

for rst_file in rst_files:
    # Skip index.rst and our custom files
    if os.path.basename(rst_file) in ['index.rst', 'modules.rst', 'controllers.rst', 'models.rst', 'routes.rst']:
        continue
    
    with open(rst_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace module references
    new_content = re.sub(pattern, replacement, content)
    
    # Also fix the title/header if it contains the prefix
    lines = new_content.split('\n')
    if lines and 'Bus-Transportation-Management-System-main' in lines[0]:
        # Extract the module name from the file path
        basename = os.path.basename(rst_file).replace('.rst', '')
        module_name = basename.replace('Bus-Transportation-Management-System-main.', '')
        # Create a cleaner title
        title = module_name.replace('_', ' ').replace('.', ' ').title()
        lines[0] = title
        lines[1] = '=' * len(title)
        new_content = '\n'.join(lines)
    
    if content != new_content:
        with open(rst_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {rst_file}")

print("Done fixing module references!")

