/**
 * Policy Service
 * API methods specific to policies
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'policy';

/**
 * List all policies
 * @returns {Promise<object>} Object with items and count
 */
export const listPolicies = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new policy
 * @param {object} data - Policy data
 * @returns {Promise<object>} Created policy
 */
export const createPolicy = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a policy by ID
 * @param {string} id - Policy ID
 * @returns {Promise<object>} Policy data
 */
export const getPolicy = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listPolicies,
  createPolicy,
  getPolicy,
};
