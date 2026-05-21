// auth.js
// Configuración centralizada de Supabase
const supabaseUrl = 'https://wguzuiifurzpgcrbbntk.supabase.co';
const supabaseAnonKey = 'sb_publishable_-0EqVIwUnsV_39CO6DMSaA_60KPpgKW';
const supabaseClient = window.supabase.createClient(supabaseUrl, supabaseAnonKey);

const DEV_EMAILS = [
    'victor.rojas@nctechsolutionsllc.com',
    'johan.rojas@nctechsolutionsllc.com',
    'luis.machado@nctechsolutionsllc.com',
    'jhons.roks@nctechsolutionsllc.com'
];

window.appUser = null;
window.appRole = 'guest';

// Verificar sesión y proteger rutas
async function checkAuth() {
    const isLoginPage = window.location.pathname.endsWith('login.html');
    
    const { data: { session }, error } = await supabaseClient.auth.getSession();
    
    if (!session) {
        if (!isLoginPage) {
            window.location.href = 'login.html';
        }
    } else {
        window.appUser = session.user;
        const email = session.user.email.toLowerCase();
        
        if (DEV_EMAILS.includes(email)) {
            window.appRole = 'dev';
        } else if (email === 'admin@admin.com') {
            window.appRole = 'admin';
        } else {
            // Por defecto, tratamos a usuarios desconocidos como admin (solo lectura) por seguridad
            window.appRole = 'admin';
        }
        
        if (isLoginPage) {
            window.location.href = 'index.html';
        } else {
            applyVisualRestrictions();
        }
    }
}

// Aplicar restricciones visuales (Solo lectura para admin)
function applyVisualRestrictions() {
    if (window.appRole === 'admin') {
        // Ejecutar después de que el DOM esté listo
        document.addEventListener('DOMContentLoaded', () => {
            // Deshabilitar inputs, selects y textareas
            const inputs = document.querySelectorAll('input, select, textarea');
            inputs.forEach(el => {
                // No deshabilitar el input del filtro de tablas (generalmente no guarda data)
                if(!el.id.toLowerCase().includes('filter') && !el.id.toLowerCase().includes('search')) {
                    el.disabled = true;
                    el.classList.add('opacity-50', 'cursor-not-allowed');
                }
            });

            // Ocultar botones de "Guardar", "Crear", "Eliminar", "Aprobar", "Rechazar"
            const actionButtons = document.querySelectorAll('button');
            actionButtons.forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (text.includes('guardar') || 
                    text.includes('crear') || 
                    text.includes('eliminar') || 
                    text.includes('aprobar') || 
                    text.includes('rechazar') || 
                    text.includes('despachar') || 
                    text.includes('recepcionar')) {
                    btn.style.display = 'none';
                }
            });
            
            console.log('Restricciones de Admin aplicadas.');
        });
        
        // Si el DOM ya cargó antes del check
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            const inputs = document.querySelectorAll('input:not([id*="filter"]):not([id*="search"]), select, textarea');
            inputs.forEach(el => { el.disabled = true; el.classList.add('opacity-50', 'cursor-not-allowed'); });
            
            const actionButtons = document.querySelectorAll('button');
            actionButtons.forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (text.includes('guardar') || text.includes('crear') || text.includes('eliminar') || text.includes('aprobar') || text.includes('rechazar') || text.includes('despachar') || text.includes('recepcionar')) {
                    btn.style.display = 'none';
                }
            });
        }
    }
}

// Función global de Logout
window.logout = async function() {
    await supabaseClient.auth.signOut();
    window.location.href = 'login.html';
};

// Iniciar verificación automáticamente
checkAuth();
