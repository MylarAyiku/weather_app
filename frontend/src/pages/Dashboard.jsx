import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../api/axios';
import { Cloud, Wind, Thermometer, Newspaper, User, LogOut, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Dashboard = () => {
    const { user, logout, updateProfile } = useContext(AuthContext);
    const [weather, setWeather] = useState(null);
    const [news, setNews] = useState([]);
    const [loadingWeather, setLoadingWeather] = useState(true);
    const [loadingNews, setLoadingNews] = useState(true);
    const [editMode, setEditMode] = useState(false);
    const [newName, setNewName] = useState(user?.name || '');
    const [newCity, setNewCity] = useState(user?.city || '');

    useEffect(() => {
        if (user) {
            fetchWeather();
            fetchNews();
            setNewName(user.name);
            setNewCity(user.city);
        }
    }, [user]);

    const fetchWeather = async () => {
        setLoadingWeather(true);
        try {
            const response = await api.get('dashboard/weather/');
            setWeather(response.data);
        } catch (error) {
            console.error("Error fetching weather", error);
            setWeather(null);
        } finally {
            setLoadingWeather(false);
        }
    };

    const fetchNews = async (category = 'technology') => {
        setLoadingNews(true);
        try {
            const response = await api.get(`dashboard/news/?category=${category}`);
            setNews(response.data.news || []);
        } catch (error) {
            console.error("Error fetching news", error);
            setNews([]);
        } finally {
            setLoadingNews(false);
        }
    };

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        try {
            await updateProfile({ name: newName, city: newCity });
            setEditMode(false);
            fetchWeather(); // Refresh weather for new city
        } catch (error) {
            console.error("Error updating profile", error);
        }
    };

    if (!user) return <div className="flex justify-center items-center h-screen text-white">Loading...</div>;

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { y: 0, opacity: 1 }
    };

    return (
        <div className="min-h-screen p-6">
            <motion.header
                initial={{ y: -50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="flex justify-between items-center mb-8 bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-xl shadow-lg"
            >
                <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                    <Cloud className="text-blue-300" /> Weather & News Dashboard
                </h1>
                <div className="flex items-center gap-4">
                    <span className="text-blue-100">Welcome, {user.name}</span>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={logout}
                        className="flex items-center gap-2 text-red-300 hover:text-red-400 transition-colors"
                    >
                        <LogOut size={18} /> Logout
                    </motion.button>
                </div>
            </motion.header>

            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >
                {/* Weather Section */}
                <div className="md:col-span-1 space-y-6">
                    <motion.div
                        variants={itemVariants}
                        className="bg-gradient-to-br from-blue-500/20 to-purple-500/20 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-xl"
                    >
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-blue-100">
                            <Thermometer className="text-orange-400" /> Current Weather
                        </h2>
                        {loadingWeather ? (
                            <p className="text-blue-200 animate-pulse">Loading weather...</p>
                        ) : weather ? (
                            <div className="text-center">
                                <motion.h3
                                    initial={{ scale: 0.9 }}
                                    animate={{ scale: 1 }}
                                    className="text-3xl font-bold text-white mb-2"
                                >
                                    {weather.city}
                                </motion.h3>
                                <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-white mb-4">{weather.temperature}°C</div>
                                <div className="flex justify-center gap-6 text-blue-100">
                                    <div className="flex items-center gap-1">
                                        <Wind size={18} /> {weather.windspeed} km/h
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <Cloud size={18} /> {weather.description}
                                    </div>
                                </div>
                                {weather.cache_status && (
                                    <span className="inline-block mt-4 px-3 py-1 bg-green-500/20 text-green-300 text-xs rounded-full border border-green-500/30">
                                        Cached
                                    </span>
                                )}
                            </div>
                        ) : (
                            <p className="text-red-400">Could not load weather data.</p>
                        )}
                    </motion.div>

                    {/* Profile Section */}
                    <motion.div
                        variants={itemVariants}
                        className="bg-white/10 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-xl"
                    >
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-semibold flex items-center gap-2 text-blue-100">
                                <User className="text-purple-400" /> Profile
                            </h2>
                            <button
                                onClick={() => setEditMode(!editMode)}
                                className="text-blue-300 text-sm hover:text-white transition-colors"
                            >
                                {editMode ? 'Cancel' : 'Edit'}
                            </button>
                        </div>

                        {editMode ? (
                            <form onSubmit={handleProfileUpdate}>
                                <div className="mb-3">
                                    <label className="block text-sm text-blue-200 mb-1">Name</label>
                                    <input
                                        type="text"
                                        value={newName}
                                        onChange={(e) => setNewName(e.target.value)}
                                        className="w-full bg-black/20 border border-white/10 rounded p-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label className="block text-sm text-blue-200 mb-1">City</label>
                                    <input
                                        type="text"
                                        value={newCity}
                                        onChange={(e) => setNewCity(e.target.value)}
                                        className="w-full bg-black/20 border border-white/10 rounded p-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    />
                                </div>
                                <motion.button
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    type="submit"
                                    className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded transition-colors"
                                >
                                    Save Changes
                                </motion.button>
                            </form>
                        ) : (
                            <div className="space-y-3">
                                <p><span className="font-medium text-blue-300">Name:</span> <span className="text-white">{user.name}</span></p>
                                <p><span className="font-medium text-blue-300">Email:</span> <span className="text-white">{user.email}</span></p>
                                <p><span className="font-medium text-blue-300">City:</span> <span className="text-white">{user.city}</span></p>
                            </div>
                        )}
                    </motion.div>
                </div>

                {/* News Section */}
                <motion.div
                    variants={itemVariants}
                    className="md:col-span-2"
                >
                    <div className="bg-white/10 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-xl h-full">
                        <div className="flex justify-between items-center mb-6 flex-wrap gap-4">
                            <h2 className="text-xl font-semibold flex items-center gap-2 text-blue-100">
                                <Newspaper className="text-green-400" /> Top Headlines
                            </h2>
                            <div className="flex gap-2 flex-wrap">
                                {['technology', 'business', 'sports', 'science'].map(cat => (
                                    <motion.button
                                        key={cat}
                                        whileHover={{ scale: 1.05, backgroundColor: "rgba(255,255,255,0.2)" }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={() => fetchNews(cat)}
                                        className="px-3 py-1 text-xs rounded-full bg-white/10 text-white border border-white/10 transition-all capitalize"
                                    >
                                        {cat}
                                    </motion.button>
                                ))}
                                <motion.button
                                    whileHover={{ rotate: 180 }}
                                    transition={{ duration: 0.3 }}
                                    onClick={() => fetchNews()}
                                    className="p-1 text-blue-300 hover:text-white transition-colors"
                                >
                                    <RefreshCw size={16} />
                                </motion.button>
                            </div>
                        </div>

                        {loadingNews ? (
                            <div className="space-y-4">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="animate-pulse flex space-x-4">
                                        <div className="flex-1 space-y-2 py-1">
                                            <div className="h-4 bg-white/10 rounded w-3/4"></div>
                                            <div className="h-4 bg-white/5 rounded w-1/2"></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : news.length > 0 ? (
                            <motion.div
                                variants={containerVariants}
                                initial="hidden"
                                animate="visible"
                                className="space-y-4"
                            >
                                <AnimatePresence mode='wait'>
                                    {news.map((article, index) => (
                                        <motion.div
                                            key={index}
                                            variants={itemVariants}
                                            whileHover={{ x: 5, backgroundColor: "rgba(255,255,255,0.05)" }}
                                            className="border-b border-white/10 pb-4 last:border-0 last:pb-0 group rounded p-2 transition-colors"
                                        >
                                            <a href={article.url} target="_blank" rel="noopener noreferrer" className="block">
                                                <h3 className="font-medium text-lg text-white group-hover:text-blue-300 transition-colors">
                                                    {article.title}
                                                </h3>
                                            </a>
                                            <p className="text-sm text-blue-200 mt-1">{article.source}</p>
                                        </motion.div>
                                    ))}
                                </AnimatePresence>
                            </motion.div>
                        ) : (
                            <p className="text-blue-200">No news available.</p>
                        )}
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
};

export default Dashboard;
