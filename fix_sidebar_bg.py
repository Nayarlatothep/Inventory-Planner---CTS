import glob
import re

html_files = glob.glob('*.html')

# We want to replace `<div class="p-6 border-b border-white/5 flex justify-center items-center bg-[#000d1a]">`
# with `<div class="p-6 border-b border-white/5 flex justify-center items-center">`
# Alternatively we can just use regex to remove `bg-[#000d1a]` from the div directly under <!-- Brand Logo -->

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for <!-- Brand Logo --> and the following div
    pattern = re.compile(r'(<!-- Brand Logo -->\s*<div class="[^"]*)bg-\[#000d1a\]([^"]*">)')
    
    # We will replace it
    if pattern.search(content):
        new_content = pattern.sub(r'\1\2', content)
        # clean up any double spaces that might be left
        new_content = new_content.replace('  ">', '">').replace('   ', ' ')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        # Also check if it's already removed or has different spacing
        pass

print("Done removing bg-[#000d1a] from Brand Logo containers.")
