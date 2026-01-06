/**
 * Retail API Service
 * Base API configuration and helper functions
 */

/**
 * Get API base URL from environment or use relative path
 */
export const getApiBase = () => {
  // In production, this will be set via build-time replacement or window config
  if (window.API_BASE_URL) {
    return window.API_BASE_URL;
  }
  // Try to infer from environment variable
  return import.meta.env.VITE_API_BASE_URL || '';
};

/**
 * Generic API call helper
 */
export const apiCall = async (endpoint, method = 'GET', body = null) => {
  const apiBase = getApiBase();
  const url = `${apiBase}${endpoint}`;

  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: response.statusText }));
    throw new Error(error.error || error.message || 'API request failed');
  }

  return response.json();
};

/**
 * Delete all entities of a given type
 */
export const deleteAllEntities = async (entityType) => {
  return apiCall(`/${entityType}`, 'DELETE');
};

export default {
  getApiBase,
  apiCall,
  deleteAllEntities,
};
