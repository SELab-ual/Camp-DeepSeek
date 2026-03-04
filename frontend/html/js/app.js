// Main Application Router
const App = {
    currentPage: 'dashboard',
    
    init() {
        this.loadPage();
        this.setupEventListeners();
    },
    
    loadPage() {
        const path = window.location.pathname;
        
        if (path === '/' || path === '/index.html') {
            this.renderHome();
        } else if (path.includes('/pages/')) {
            // Pages are loaded as separate HTML files
            this.initializePage(path);
        }
    },
    
    renderHome() {
        const content = document.getElementById('mainContent');
        if (!content) return;
        
        content.innerHTML = `
            <div class="hero">
                <h1>Welcome to Camp Management System</h1>
                <p>The complete solution for managing your camp operations</p>
                <div class="hero-buttons">
                    ${!Auth.isAuthenticated() ? `
                        <button class="btn btn-primary" onclick="window.location.href='/pages/login.html'">Login</button>
                        <button class="btn btn-secondary" onclick="window.location.href='/pages/register.html'">Register</button>
                    ` : `
                        <button class="btn btn-primary" onclick="window.location.href='/pages/dashboard.html'">Go to Dashboard</button>
                    `}
                </div>
            </div>
            
            <div class="features">
                <h2>Features in Sprint 1</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>👥 Camper Management</h3>
                        <p>Add, edit, and manage camper profiles with ease</p>
                    </div>
                    <div class="feature-card">
                        <h3>👪 Parent Accounts</h3>
                        <p>Parents can create accounts and enroll their children</p>
                    </div>
                    <div class="feature-card">
                        <h3>🏷️ Group Organization</h3>
                        <p>Create groups and organize campers effectively</p>
                    </div>
                    <div class="feature-card">
                        <h3>🏥 Medical Information</h3>
                        <p>Store and access critical medical information</p>
                    </div>
                </div>
            </div>
        `;
    },
    
    initializePage(path) {
        // Page-specific initialization
        if (path.includes('dashboard')) {
            Dashboard.init();
        } else if (path.includes('campers')) {
            CampersPage.init();
        } else if (path.includes('parents')) {
            ParentsPage.init();
        } else if (path.includes('groups')) {
            GroupsPage.init();
        } else if (path.includes('medical')) {
            MedicalPage.init();
        } else if (path.includes('login')) {
            LoginPage.init();
        } else if (path.includes('register')) {
            RegisterPage.init();
        }
    },
    
    setupEventListeners() {
        // Global event listeners
        document.addEventListener('click', (e) => {
            // Handle modal close on outside click
            if (e.target.classList.contains('modal')) {
                e.target.classList.remove('active');
            }
        });
    }
};

// Page Controllers
const Dashboard = {
    async init() {
        if (!Auth.requireAuth()) return;
        
        try {
            // Load dashboard data
            const [campers, parents, groups] = await Promise.all([
                ApiService.campers.getAll(),
                ApiService.parents.getAll(),
                ApiService.groups.getAll()
            ]);
            
            this.renderDashboard(campers, parents, groups);
        } catch (error) {
            Toast.error('Failed to load dashboard data');
        }
    },
    
    renderDashboard(campers, parents, groups) {
        const content = document.getElementById('mainContent');
        if (!content) return;
        
        const activeCampers = campers.filter(c => c.is_active).length;
        const suspendedCampers = campers.filter(c => c.is_suspended).length;
        
        content.innerHTML = `
            <h2>Dashboard</h2>
            
            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <h3>Total Campers</h3>
                    <div class="number">${campers.length}</div>
                    <p>Active: ${activeCampers} | Suspended: ${suspendedCampers}</p>
                </div>
                
                <div class="dashboard-card">
                    <h3>Total Parents</h3>
                    <div class="number">${parents.length}</div>
                </div>
                
                <div class="dashboard-card">
                    <h3>Total Groups</h3>
                    <div class="number">${groups.length}</div>
                </div>
                
                <div class="dashboard-card">
                    <h3>Medical Records</h3>
                    <div class="number">${campers.filter(c => c.medical_info).length}</div>
                    <p>Campers with medical info</p>
                </div>
            </div>
            
            <div class="recent-activity">
                <h3>Recent Campers</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Age</th>
                                <th>Group</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${campers.slice(0, 5).map(camper => `
                                <tr>
                                    <td>${camper.first_name} ${camper.last_name}</td>
                                    <td>${camper.age || 'N/A'}</td>
                                    <td>${camper.group?.name || 'Unassigned'}</td>
                                    <td>
                                        ${camper.is_suspended ? 
                                            '<span style="color: #ef4444">Suspended</span>' : 
                                            camper.is_active ? 
                                            '<span style="color: #10b981">Active</span>' : 
                                            '<span style="color: #6b7280">Inactive</span>'}
                                    </td>
                                    <td>
                                        <button class="action-btn view-btn" onclick="CampersPage.viewCamper(${camper.id})">View</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }
};

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});