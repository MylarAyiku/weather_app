import React, { createContext, useState, useEffect } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    // We can't use useNavigate here directly if AuthProvider is outside Router, 
    // but usually it's inside. Assuming App wraps it.
    // Actually, best to pass navigate or handle redirect in components.
    // Or use a wrapper component.

    useEffect(() => {
        checkUserLoggedIn();
    }, []);

    const checkUserLoggedIn = async () => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const response = await api.get('users/me/');
                setUser(response.data);
            } catch (error) {
                console.error("Failed to fetch user", error);
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                setUser(null);
            }
        }
        setLoading(false);
    };

    const login = async (email, password) => {
        const response = await api.post('token/', { email, password });
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        await checkUserLoggedIn();
        return true;
    };

    const register = async (name, email, password, city) => {
        await api.post('users/', { name, email, password, city });
        return true;
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const updateProfile = async (data) => {
        const response = await api.patch('users/me/', data);
        setUser(response.data);
        return response.data;
    }

    return (
        <AuthContext.Provider value={{ user, login, register, logout, updateProfile, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
