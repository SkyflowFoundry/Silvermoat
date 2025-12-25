/**
 * Generic API Client for Silvermoat Insurance
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

// Get API base URL (imported from App.jsx to maintain single source of truth)
import { getApiBase } from '../App';

/**
 * Get the configured API base URL
 * @returns {string} API base URL
 */
export const getApiBaseUrl = () => {
  return getApiBase();
};

/**
 * Generic function to create an entity
 * @param {string} domain - Entity domain (quote, policy, claim, payment, case)
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
 * @param {string} domain - Entity domain (quote, policy, claim, payment, case)
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
 * @param {string} domain - Entity domain (quote, policy, claim, payment, case)
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
 * Update claim status (special endpoint for claims)
 * @param {string} claimId - Claim ID
 * @param {string} status - New status (PENDING, REVIEW, APPROVED, DENIED)
 * @returns {Promise<object>} Updated claim status response
 */
export const updateClaimStatus = async (claimId, status) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/claim/${claimId}/status`;

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
      `Failed to update claim status: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Upload document to claim (special endpoint for claims)
 * @param {string} claimId - Claim ID
 * @param {string} text - Document text content
 * @returns {Promise<object>} Document upload response with S3 key
 */
export const uploadClaimDocument = async (claimId, text) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/claim/${claimId}/doc`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Failed to upload document: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  return response.json();
};

/**
 * Backwards compatibility: Keep old function names for quotes
 */
export const createQuote = (data) => createEntity('quote', data);
export const getQuote = (id) => getEntity('quote', id);

export default {
  createEntity,
  getEntity,
  listEntities,
  deleteEntity,
  deleteAllEntities,
  updateClaimStatus,
  uploadClaimDocument,
  createQuote,
  getQuote,
  ApiError,
};
