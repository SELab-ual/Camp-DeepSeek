// Auth State Management
const Auth = {
    user: null,
    token: localStorage.getItem('token'),
    
    async init() {
        if (this.token) {
            try {
                this.user = await ApiService.auth.getCurrentUser();
                this.updateUI();
            } catch (error) {
                this.logout();
            }
        }
        this.updateUI();
    },
    
    async login(username, password) {
        try {
            const data = await ApiService.auth.login(username, password);
            this.token = data.access_token;
            this.user = await ApiService.auth.getCurrentUser();
            
            localStorage.setItem('token', this.token);
            this.updateUI();
            
            Toast.success('Login successful');
            return true;
        } catch (error) {
            Toast.error(error.message);
            return false;
        }
    },
    
    async register(userData) {
        try {
            const user = await ApiService.auth.register(userData);
            Toast.success('Registration successful! Please login.');
            return true;
        } catch (error) {
            Toast.error(error.message);
            return false;
        }
    },
    
    logout() {
        this.user = null;
        this.token = null;
        localStorage.removeItem('token');
        this.updateUI();
        window.location.href = '/pages/login.html';
    },
    
    updateUI() {
        const navMenu = document.getElementById('navMenu');
        const navUser = document.getElementById('navUser');
        
        if (!navMenu || !navUser) return;
        
        if (this.user) {
            // Show authenticated menu
            navMenu.innerHTML = `
                <a href="/pages/dashboard.html" class="${this.isActive('/dashboard')}">Dashboard</a>
                <a href="/pages/campers.html" class="${this.isActive('/campers')}">Campers</a>
                <a href="/pages/parents.html" class="${this.isActive('/parents')}">Parents</a>
                <a href="/pages/groups.html" class="${this.isActive('/groups')}">Groups</a>
                <a href="/pages/medical.html" class="${this.isActive('/medical')}">Medical</a>
            `;
            
            navUser.innerHTML = `
                <span class="user-info">${this.user.full_name} (${this.user.role})</span>
                <button class="logout-btn" onclick="Auth.logout()">Logout</button>
            `;
        } else {
            navMenu.innerHTML = `
                <a href="/index.html">Home</a>
                <a href="/pages/login.html">Login</a>
                <a href="/pages/register.html">Register</a>
            `;
            navUser.innerHTML = '';
        }
    },
    
    isActive(page) {
        return window.location.pathname.includes(page) ? 'active' : '';
    },
    
    isAuthenticated() {
        return !!this.user;
    },
    
    hasRole(role) {
        return this.user && (this.user.role === role || this.user.role === 'admin');
    },
    
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/pages/login.html';
            return false;
        }
        return true;
    },
    
    requireRole(role) {
        if (!this.requireAuth()) return false;
        if (!this.hasRole(role)) {
            Toast.error('You do not have permission to access this page');
            window.location.href = '/pages/dashboard.html';
            return false;
        }
        return true;
    }
};

// Toast Notification System
const Toast = {
    show(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    },
    
    success(message) {
        this.show(message, 'success');
    },
    
    error(message) {
        this.show(message, 'error');
    },
    
    info(message) {
        this.show(message, 'info');
    }
};

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => {
    Auth.init();
});