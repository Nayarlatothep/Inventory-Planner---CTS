
const { createClient } = require('@supabase/supabase-js');
const supabaseUrl = 'https://wguzuiifurzpgcrbbntk.supabase.co';
const supabaseAnonKey = 'sb_publishable_-0EqVIwUnsV_39CO6DMSaA_60KPpgKW';
const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkSchema() {
    const { data, error } = await supabase.from('detalle_solicitud_ot').select('*').limit(1);
    if (error) {
        console.error(error);
    } else {
        console.log(JSON.stringify(Object.keys(data[0])));
    }
}
checkSchema();
