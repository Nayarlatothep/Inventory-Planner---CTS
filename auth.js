// auth.js
// Configuración centralizada de Supabase
window.supabaseUrl = 'https://wguzuiifurzpgcrbbntk.supabase.co';
window.supabaseAnonKey = 'sb_publishable_-0EqVIwUnsV_39CO6DMSaA_60KPpgKW';
window.supabaseClient = window.supabase.createClient(window.supabaseUrl, window.supabaseAnonKey);
var supabaseClient = window.supabaseClient; // Make it global so other scripts can access it directly
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
    const isLoginPage = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || window.location.pathname === '';
    
    const { data: { session }, error } = await supabaseClient.auth.getSession();
    
    if (!session) {
        if (!isLoginPage) {
            window.location.href = 'index.html';
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
            window.location.href = 'inicio.html';
        } else {
            applyVisualRestrictions();
        }
    }
}

// Aplicar restricciones visuales (Solo lectura para admin)
function applyVisualRestrictions() {
    if (window.appRole === 'admin') {
        // Permitir acceso total a Reportes y KPIs (kpi_mantenimiento.html)
        if (window.location.pathname.includes('kpi_mantenimiento.html')) {
            return; 
        }

        const applyRestrictions = () => {
            // Deshabilitar inputs, selects y textareas
            const inputs = document.querySelectorAll('input:not([id*="filter"]):not([id*="search"]), select, textarea');
            inputs.forEach(el => {
                el.disabled = true;
                el.classList.add('opacity-50', 'cursor-not-allowed');
            });

            // Ocultar todos los botones excepto Cerrar Sesión y controles de navegación
            const allButtons = document.querySelectorAll('button');
            allButtons.forEach(btn => {
                const onclickAttr = btn.getAttribute('onclick') || '';
                const title = btn.getAttribute('title') || '';
                
                // Mantener botón de Cerrar Sesión
                if (onclickAttr.includes('window.logout') || title.includes('Cerrar Sesión')) {
                    return; 
                }
                
                // Mantener controles de navegación (menú lateral y submenús)
                if (btn.id === 'btnToggle' || btn.id === 'btnMobileToggle' || btn.closest('nav')) {
                    return;
                }

                // Bloquear/ocultar todos los demás botones
                btn.style.display = 'none';
            });
        };

        // Ejecutar inmediatamente si el DOM ya está listo
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            applyRestrictions();
        } else {
            document.addEventListener('DOMContentLoaded', applyRestrictions);
        }
        
        // Ejecutar también periódicamente en caso de que se agreguen botones dinámicamente (ej. en modales o tablas)
        setInterval(applyRestrictions, 1000);
    }
}

// Función global de Logout
window.logout = async function() {
    await supabaseClient.auth.signOut();
    window.location.href = 'index.html';
};

// Iniciar verificación automáticamente
checkAuth();
