import os
import re
import glob

def add_unidades_mantenimiento():
    # Link to add
    link_html = '''
                        <a href="unidades_mantenimiento.html" class="nav-link flex items-center gap-2 py-2 text-sm text-slate-400 hover:text-amber-400 hover:translate-x-1 transition-all group">
                            <span class="material-symbols-outlined text-[16px] group-hover:text-amber-400 transition-colors">engineering</span>Unidades en Mantenimiento
                        </a>'''

    # Regular expression to find the flota link in different formats
    flota_regex = re.compile(r'([ \t]*<a href="flota\.html"[^>]*>.*?Estado de Flota.*?</a>)', re.DOTALL)

    for file_path in glob.glob('*.html'):
        if file_path == 'unidades_mantenimiento.html':
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'href="unidades_mantenimiento.html"' not in content:
            # Check if flota link exists
            if 'href="flota.html"' in content:
                # Find the flota link and insert our link right before it
                match = flota_regex.search(content)
                if match:
                    flota_link = match.group(1)
                    # Get the leading whitespace for indentation
                    leading_ws = match.group(1)[:len(match.group(1)) - len(match.group(1).lstrip())]
                    
                    # Ensure the new link uses the same leading whitespace or we just prepend it
                    # But our link_html has fixed indentation. We can adjust it based on leading_ws if needed, 
                    # but simple string replace is fine.
                    
                    new_link = f'\n{leading_ws}<a href="unidades_mantenimiento.html" class="nav-link flex items-center gap-2 py-2 text-sm text-slate-400 hover:text-amber-400 hover:translate-x-1 transition-all group">\n{leading_ws}    <span class="material-symbols-outlined text-[16px] group-hover:text-amber-400 transition-colors">engineering</span>Unidades en Mantenimiento\n{leading_ws}</a>\n{leading_ws}'

                    content = content.replace(flota_link, new_link + flota_link.lstrip())
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Added link to {file_path}")

if __name__ == '__main__':
    add_unidades_mantenimiento()
