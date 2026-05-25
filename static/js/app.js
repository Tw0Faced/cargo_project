const API_BASE = 'http://127.0.0.1:8000/api/v1';

// ===== Инициализация =====
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            loadSection(item.dataset.section, item);
        });
    });
    loadDashboardStats();
});

// ===== Навигация =====
function loadSection(sectionId, navElement) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId)?.classList.add('active');
    if (navElement) {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        navElement.classList.add('active');
    }
    const loaders = {
        'cargo': loadCargo, 'clients': loadClients, 'transports': loadTransports,
        'routes': loadRoutes, 'shipments': loadShipments
    };
    if (loaders[sectionId]) loaders[sectionId]();
}

// ===== Статистика дашборда =====
async function loadDashboardStats() {
    const endpoints = {
        'cargo-count': '/cargo/', 'clients-count': '/clients/',
        'transports-count': '/transports/', 'shipments-count': '/shipments/'
    };
    for (const [id, ep] of Object.entries(endpoints)) {
        try {
            const res = await fetch(`${API_BASE}${ep}`);
            if (res.ok) {
                const data = await res.json();
                document.getElementById(id).textContent = Array.isArray(data) ? data.length : '—';
            }
        } catch (e) { console.warn(e); }
    }
    loadRecentShipments();
    loadPopularRoutes();
}

async function fetchData(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) { console.error(err); return null; }
}

function renderTable(containerId, data, columns) {
    const container = document.getElementById(containerId);
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty">Нет данных</div>';
        return;
    }
    const headers = columns.map(c => `<th>${c.label}</th>`).join('');
    const rows = data.map(item => 
        `<tr>${columns.map(c => `<td>${formatValue(item[c.field])}</td>`).join('')}</tr>`
    ).join('');
    container.innerHTML = `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
}

function formatValue(v) {
    if (v === null || v === undefined) return '—';
    return typeof v === 'object' ? JSON.stringify(v) : String(v);
}

// ===== Загрузчики разделов =====
async function loadCargo() { renderTable('cargo-table', await fetchData('/cargo/'), [
    {field:'g_id',label:'ID'}, {field:'g_name',label:'Название'}, {field:'g_weight',label:'Вес'}, {field:'g_volume',label:'Объём'}, {field:'g_type',label:'Тип'}
]);}
async function loadClients() { renderTable('clients-table', await fetchData('/clients/'), [
    {field:'c_id',label:'ID'}, {field:'c_type',label:'Тип'}, {field:'c_name',label:'Наименование'}
]);}
async function loadTransports() { renderTable('transports-table', await fetchData('/transports/'), [
    {field:'t_id',label:'ID'}, {field:'t_mark',label:'Марка'}, {field:'t_model',label:'Модель'}, {field:'t_number',label:'Номер'}, {field:'t_cap',label:'Грузоподъёмность'}
]);}
async function loadRoutes() { renderTable('routes-table', await fetchData('/routes/'), [
    {field:'r_id',label:'ID'}, {field:'r_from',label:'Откуда'}, {field:'r_to',label:'Куда'}, {field:'r_dist',label:'Расстояние'}, {field:'r_time',label:'Время'}
]);}
async function loadShipments() { renderTable('shipments-table', await fetchData('/shipments/'), [
    {field:'tr_id',label:'ID'}, {field:'cargo',label:'Груз'}, {field:'transport',label:'Транспорт'}, {field:'route',label:'Маршрут'}, {field:'tr_date_start',label:'Дата'}, {field:'tr_status',label:'Статус'}
]);}

// ===== Последние перевозки и маршруты =====
async function loadRecentShipments() {
    const c = document.getElementById('recent-shipments-list');
    const data = await fetchData('/shipments/');
    if (!data?.length) { c.innerHTML = '<div class="empty">Нет перевозок</div>'; return; }
    c.innerHTML = data.slice(-5).reverse().map(i => `
        <div class="recent-item">
            <div class="recent-info"><h4>Перевозка #${i.tr_id}</h4><p>${formatValue(i.cargo)} → ${formatValue(i.route)}</p></div>
            <span class="status-badge ${getStatusClass(i.tr_status)}">${formatValue(i.tr_status)}</span>
        </div>`).join('');
}
function getStatusClass(s) {
    if (!s) return 'status-pending';
    const l = s.toLowerCase();
    if (l.includes('актив') || l.includes('в пути')) return 'status-active';
    if (l.includes('заверш')) return 'status-completed';
    return 'status-pending';
}
async function loadPopularRoutes() {
    const c = document.getElementById('popular-routes-list');
    const data = await fetchData('/routes/');
    if (!data?.length) { c.innerHTML = '<div class="empty">Нет маршрутов</div>'; return; }
    c.innerHTML = data.slice(0,5).map(i => `
        <div class="route-item">
            <div class="recent-info"><h4><i class="fas fa-map-marker-alt"></i> ${formatValue(i.r_from)} → ${formatValue(i.r_to)}</h4><p>${formatValue(i.r_dist)} км | ${formatValue(i.r_time)} ч</p></div>
        </div>`).join('');
}

// ===== МОДАЛЬНОЕ ОКНО И СОЗДАНИЕ =====
const createFields = {
    cargo: [
        {id:'g_name',label:'Название груза',type:'text',req:true},
        {id:'g_weight',label:'Вес (кг)',type:'number',req:true},
        {id:'g_volume',label:'Объём (м³)',type:'number'},
        {id:'g_type',label:'Тип груза',type:'text'}
    ],
    clients: [
        {id:'c_name',label:'ФИО / Организация',type:'text',req:true},
        {id:'c_type',label:'Тип (FL/YL)',type:'text',req:true}
    ],
    transports: [
        {id:'t_mark',label:'Марка',type:'text',req:true},
        {id:'t_model',label:'Модель',type:'text',req:true},
        {id:'t_number',label:'Гос. номер',type:'text',req:true},
        {id:'t_cap',label:'Грузоподъёмность',type:'number',req:true}
    ],
    routes: [
        {id:'r_from',label:'Откуда',type:'text',req:true},
        {id:'r_to',label:'Куда',type:'text',req:true},
        {id:'r_dist',label:'Расстояние (км)',type:'number'},
        {id:'r_time',label:'Время (ч)',type:'number'}
    ],
    shipments: [
        {id:'tr_date_start',label:'Дата отправки (YYYY-MM-DD)',type:'date',req:true},
        {id:'tr_date_end',label:'Дата прибытия (YYYY-MM-DD)',type:'date'},
        {id:'tr_status',label:'Статус',type:'text',value:'IN_PROGRESS'},
        {id:'cargo',label:'ID Груза',type:'number',req:true,ph:'Введите ID груза'},
        {id:'transport',label:'ID Транспорта',type:'number',req:true,ph:'Введите ID транспорта'},
        {id:'route',label:'ID Маршрута',type:'number',req:true,ph:'Введите ID маршрута'},
        {id:'client',label:'ID Диспетчера (необязательно)',type:'number',ph:'Введите ID диспетчера'}  // Убрал req:true
    ]
};
let currentSection = '';

function openCreateModal(section) {
    currentSection = section;
    const modal = document.getElementById('createModal');
    const fields = document.getElementById('modal-fields');
    document.getElementById('modal-title').innerText = `Создание: ${{cargo:'Груз',clients:'Клиент',transports:'Транспорт',routes:'Маршрут',shipments:'Перевозка'}[section]}`;
    fields.innerHTML = '';
    createFields[section].forEach(f => {
        const wrap = document.createElement('div');
        const lbl = document.createElement('label');
        lbl.innerText = f.label;
        lbl.style.cssText = 'font-size:12px;color:#666;margin-bottom:4px;display:block';
        const inp = document.createElement('input');
        inp.type = f.type||'text'; inp.id = f.id; inp.name = f.id; inp.className = 'modal-input';
        if(f.req) inp.required = true;
        if(f.ph) inp.placeholder = f.ph;
        if(f.value) inp.value = f.value;
        wrap.appendChild(lbl); wrap.appendChild(inp); fields.appendChild(wrap);
    });
    modal.style.display = 'flex';
}
function closeCreateModal() { document.getElementById('createModal').style.display = 'none'; }

document.getElementById('createForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {};
    const fields = createFields[currentSection];
    
    fields.forEach(f => {
        let v = document.getElementById(f.id).value;
        
        // 1. Если поле пустое — отправляем null (чтобы база приняла)
        if (v === "") {
            data[f.id] = null;
            return;
        }
        
        // 2. Если это число — преобразуем
        if (f.type === 'number') {
            data[f.id] = Number(v);
        }
        // 3. Если это дата — убеждаемся, что формат YYYY-MM-DD
        else if (f.type === 'date') {
            // Если пользователь ввел dd.mm.yyyy, превращаем в yyyy-mm-dd
            if (v.includes('.')) {
                const parts = v.split('.');
                v = `${parts[2]}-${parts[1]}-${parts[0]}`;
            }
            data[f.id] = v;
        }
        else {
            data[f.id] = v;
        }
    });
    
    try {
        const res = await fetch(`${API_BASE}/${currentSection}/`, {
            method:'POST', 
            headers:{'Content-Type':'application/json'}, 
            body:JSON.stringify(data)
        });
        
        if(res.ok) {
            alert('Успешно создано!');
            closeCreateModal();
            loadSection(currentSection); // Обновляем таблицу
            loadDashboardStats(); // Обновляем счетчики
        } else {
            const err = await res.json();
            alert(`Ошибка: ${JSON.stringify(err)}`);
        }
    } catch(e) { 
        alert(`Ошибка сети: ${e.message}`); 
    }
});

// ===== ТЕМА =====
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDark?'dark':'light');
    document.querySelector('.theme-toggle i').className = isDark?'fas fa-sun':'fas fa-moon';
}
document.addEventListener('DOMContentLoaded', () => {
    if(localStorage.getItem('theme')==='dark') {
        document.body.classList.add('dark-theme');
        document.querySelector('.theme-toggle i').className = 'fas fa-sun';
    }
});