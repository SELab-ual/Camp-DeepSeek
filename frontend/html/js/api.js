// API Configuration
const API_BASE_URL = '/api';

// API Service
const ApiService = {
    // Authentication
    auth: {
        async login(username, password) {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            
            const response = await fetch(`${API_BASE_URL}/auth/token`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }
            
            return response.json();
        },
        
        async register(userData) {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Registration failed');
            }
            
            return response.json();
        },
        
        async getCurrentUser() {
            const token = localStorage.getItem('token');
            if (!token) return null;
            
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) return null;
            return response.json();
        }
    },
    
    // Generic request method with auth
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        };
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                window.location.href = '/pages/login.html';
                throw new Error('Session expired');
            }
            
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Request failed');
        }
        
        return response.json();
    },
    
    // Campers
    campers: {
        getAll: (params = '') => ApiService.request(`/campers${params}`),
        getById: (id) => ApiService.request(`/campers/${id}`),
        create: (data) => ApiService.request('/campers', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => ApiService.request(`/campers/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => ApiService.request(`/campers/${id}`, {
            method: 'DELETE'
        }),
        suspend: (id) => ApiService.request(`/campers/${id}/suspend`, {
            method: 'POST'
        }),
        activate: (id) => ApiService.request(`/campers/${id}/activate`, {
            method: 'POST'
        })
    },
    
    // Parents
    parents: {
        getAll: () => ApiService.request('/parents'),
        getById: (id) => ApiService.request(`/parents/${id}`),
        create: (data) => ApiService.request('/parents', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => ApiService.request(`/parents/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => ApiService.request(`/parents/${id}`, {
            method: 'DELETE'
        }),
        getCampers: (id) => ApiService.request(`/parents/${id}/campers`)
    },
    
    // Groups
    groups: {
        getAll: () => ApiService.request('/groups'),
        getById: (id) => ApiService.request(`/groups/${id}`),
        create: (data) => ApiService.request('/groups', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => ApiService.request(`/groups/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => ApiService.request(`/groups/${id}`, {
            method: 'DELETE'
        }),
        getCampers: (id) => ApiService.request(`/groups/${id}/campers`)
    },
    
    // Medical
    medical: {
        getByCamper: (camperId) => ApiService.request(`/medical/camper/${camperId}`),
        create: (data) => ApiService.request('/medical', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => ApiService.request(`/medical/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => ApiService.request(`/medical/${id}`, {
            method: 'DELETE'
        })
    }
};