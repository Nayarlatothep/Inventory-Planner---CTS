import glob
import re

html_files = glob.glob('*.html')

for filepath in html_files:
    if filepath == 'login.html':
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert auth.js in head (after Supabase CDN if it exists, or just before </head>)
    if 'auth.js' not in content:
        if '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>' in content:
            content = content.replace(
                '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>',
                '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n    <script src="auth.js"></script>'
            )
        else:
            content = content.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n    <script src="auth.js"></script>\n</head>')
    
    # 2. Fix duplicated constant declarations to prevent errors
    # Replace "const supabaseUrl =" with "var supabaseUrl ="
    content = content.replace('const supabaseUrl =', '// const supabaseUrl =')
    content = content.replace('const supabaseAnonKey =', '// const supabaseAnonKey =')
    # Some files use "const supabaseClient =" and some "let supabaseClient =". We comment them out if they are global scope in script tags.
    # Actually, it's safer to just replace them with window.supabaseClient usage, or just remove "const/let" if it's already declared in auth.js.
    # To avoid syntax errors, I'll change them to use the global ones.
    content = re.sub(r'const\s+supabaseClient\s*=\s*supabase\.createClient', '// const supabaseClient = supabase.createClient', content)
    content = re.sub(r'let\s+supabaseClient\s*=\s*null;', '// let supabaseClient = null;', content)
    content = re.sub(r'supabaseClient\s*=\s*window\.supabase\.createClient[^;]+;', '// supabaseClient already created', content)

    # 3. Add a logout button to the user profile section
    # Search for: <span class="text-[9px] text-slate-300 font-bold">Sistema Online</span>
    # And add a logout button right after the user info div
    logout_html = '''
                    <button onclick="window.logout()" class="ml-auto text-slate-400 hover:text-red-400 transition-colors p-1" title="Cerrar Sesión">
                        <span class="material-symbols-outlined text-[18px]">logout</span>
                    </button>'''
    if 'logout()' not in content and 'Sistema Online</span>' in content:
        content = content.replace('Sistema Online</span>\n                    </div>', 'Sistema Online</span>\n                    </div>' + logout_html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
