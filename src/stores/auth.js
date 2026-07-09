import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import pako from 'pako';
import { router } from '../router';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);

    // Gzip + Base64 Storage Helpers
    const saveUserToStorage = (userData) => {
        try {
            const jsonStr = JSON.stringify(userData);
            const compressed = pako.gzip(jsonStr);
            // Convert Uint8Array to Binary String -> Base64
            const binaryStr = Array.from(compressed, byte => String.fromCharCode(byte)).join('');
            const base64 = btoa(binaryStr);
            localStorage.setItem('user_data', base64);
        } catch (e) {
            console.error('Failed to save user data', e);
        }
    };

    const loadUserFromStorage = () => {
        try {
            const base64 = localStorage.getItem('user_data');
            if (!base64) return null;

            const binaryStr = atob(base64);
            const compressed = Uint8Array.from(binaryStr, char => char.charCodeAt(0));
            const jsonStr = pako.ungzip(compressed, { to: 'string' });
            return JSON.parse(jsonStr);
        } catch (e) {
            console.error('Failed to load user data', e);
            localStorage.removeItem('user_data');
            return null;
        }
    };

    // Initialize
    user.value = loadUserFromStorage();

    const isAuthenticated = computed(() => !!user.value);

    const hasPermission = (requiredPermissions) => {
        if (!user.value?.userConfig) return false;

        if (Array.isArray(requiredPermissions)) {
            // Check if user has AT LEAST ONE of the required permissions (OR logic)
            return requiredPermissions.some(p => user.value.userConfig.includes(p));
        }
        return user.value.userConfig.includes(requiredPermissions);
    };

    const login = async (userId, password) => {
        // Mock Login (Dev environment only)
        if (import.meta.env.DEV) {
            if (userId === 'dev' && password === 'dev') {
                const mockUser = {
                    userId: 'dev',
                    displayName: 'Developer',
                    email: 'dev@local',
                    userConfig: ['EXAMPLE_OTHER_PERMISSION', 'admin']
                };
                user.value = mockUser;
                saveUserToStorage(mockUser);
                return true;
            }

            if (userId === 'test' && password === 'test') {
                const mockUser = {
                    userId: 'test',
                    displayName: 'Test User',
                    email: 'test@local',
                    userConfig: [] // No Permissions
                };
                user.value = mockUser;
                saveUserToStorage(mockUser);
                return true;
            }
        }

        const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://10.13.227.98:8000';
        // const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://10.13.227.125:8000';
        try {
            const response = await fetch(`${API_URL}/Common/Login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ldapName: "Local", // Default as per request
                    userId: userId,
                    password: password
                })
            });

            console.log(response)
            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();

            // Expected format: { message: "...", user: { ... }, setUserInfoStatus: 0 }
            if (data.user) {
                user.value = data.user;
                saveUserToStorage(data.user);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    };

    const logout = () => {
        user.value = null;
        localStorage.removeItem('user_data');
        router.push('/login');
    };

    return { user, isAuthenticated, login, logout, hasPermission };
});
