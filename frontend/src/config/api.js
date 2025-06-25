// API Configuration - Priority: Production URL first, then localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://wall-street-backend.onrender.com/';

export default API_BASE_URL; 