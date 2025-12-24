/**
 * Claim Service
 * API methods specific to claims including special endpoints
 */

import { createEntity, getEntity, listEntities, updateClaimStatus, uploadClaimDocument } from './api';

const DOMAIN = 'claim';

/**
 * List all claims
 * @returns {Promise<object>} Object with items and count
 */
export const listClaims = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new claim
 * @param {object} data - Claim data
 * @returns {Promise<object>} Created claim
 */
export const createClaim = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a claim by ID
 * @param {string} id - Claim ID
 * @returns {Promise<object>} Claim data
 */
export const getClaim = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Update claim status
 * @param {string} id - Claim ID
 * @param {string} status - New status
 * @returns {Promise<object>} Updated claim
 */
export const updateStatus = async (id, status) => {
  return updateClaimStatus(id, status);
};

/**
 * Upload document to claim
 * @param {string} id - Claim ID
 * @param {string} text - Document text
 * @returns {Promise<object>} Upload response
 */
export const uploadDocument = async (id, text) => {
  return uploadClaimDocument(id, text);
};

export default {
  listClaims,
  createClaim,
  getClaim,
  updateStatus,
  uploadDocument,
};
