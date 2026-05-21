import glob

html_files = glob.glob('*.html')
old_str = '<img src="logo.png" alt="CSM Legacy Logo" class="w-full max-w-[180px] h-auto object-contain bg-white rounded-xl p-2">'
new_str = '<img src="logo.png" alt="CSM Legacy Logo" class="w-full max-w-[180px] h-auto object-contain">'

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
