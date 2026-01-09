/**
 * Generic API Client for Silvermoat Retail
 * Provides base methods for interacting with all entity domains
 */

// Custom error class for API errors
export class ApiError extends Error {
  constructor(message, status, response) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.response = response;
  }
}

/**
 * Get the configured API base URL
 * @returns {string} API base URL
 */
export const getApiBaseUrl = () => {
  // In production, this will be set via build-time replacement or window config
  // For now, try to get from window or use env variable
  if (window.API_BASE_URL) {
    return window.API_BASE_URL;
  }
  // Try to infer from env variable (set during deploy)
  return import.meta.env.VITE_API_BASE_URL || '';
};

/**
 * Generic function to create an entity
 * @param {string} domain - Entity domain (product, order, inventory, payment, case)
 * @param {object} data - Entity data
 * @returns {Promise<object>} Created entity response
 */
export const createEntity = async (domain, data) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/${domain}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to create ${domain}: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Generic function to get an entity by ID
 * @param {string} domain - Entity domain (product, order, inventory, payment, case)
 * @param {string} id - Entity ID
 * @returns {Promise<object>} Entity data
 */
export const getEntity = async (domain, id) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/${domain}/${id}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to get ${domain}: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Generic function to list all entities of a type
 * @param {string} domain - Entity domain
 * @returns {Promise<object>} Object with items array and count
 */
export const listEntities = async (domain) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/${domain}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to list ${domain}: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  const data = await response.json();
  return data; // Returns { items: [], count: number }
};

/**
 * Generic function to delete an entity by ID
 * @param {string} domain - Entity domain (product, order, inventory, payment, case)
 * @param {string} id - Entity ID
 * @returns {Promise<object>} Deletion confirmation
 */
export const deleteEntity = async (domain, id) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/${domain}/${id}`;

  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to delete ${domain}: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Generic function to delete all entities of a type (bulk delete)
 * @param {string} domain - Entity domain
 * @returns {Promise<object>} Object with deleted count
 */
export const deleteAllEntities = async (domain) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/${domain}`;

  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to delete all ${domain}: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Update order status (special endpoint for orders)
 * @param {string} orderId - Order ID
 * @param {string} status - New status (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
 * @returns {Promise<object>} Updated order status response
 */
export const updateOrderStatus = async (orderId, status) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/order/${orderId}/status`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to update order status: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Generic POST request
 * @param {string} path - API path (e.g., '/product', '/order')
 * @param {object} data - Request body
 * @returns {Promise<object>} Response data
 */
export const post = async (path, data) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}${path}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = `Request failed: ${response.statusText}`;
    try {
      const errorData = JSON.parse(errorText);
      errorMessage = errorData.message || errorData.error || errorMessage;
    } catch (e) {
      // Use default error message
    }
    throw new ApiError(errorMessage, response.status, errorText);
  }

  return response.json();
};

/**
 * Generic GET request
 * @param {string} path - API path (e.g., '/customer/orders?email=XXX')
 * @returns {Promise<object>} Response data
 */
export const get = async (path) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}${path}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = `Request failed: ${response.statusText}`;
    try {
      const errorData = JSON.parse(errorText);
      errorMessage = errorData.message || errorData.error || errorMessage;
    } catch (e) {
      // Use default error message
    }
    throw new ApiError(errorMessage, response.status, errorText);
  }

  return response.json();
};

export default {
  createEntity,
  getEntity,
  listEntities,
  deleteEntity,
  deleteAllEntities,
  updateOrderStatus,
  post,
  get,
  ApiError,
  getApiBaseUrl,
};
