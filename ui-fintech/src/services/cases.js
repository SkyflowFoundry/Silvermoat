/**
 * Case Service
 * API calls for case/support ticket management
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'case';

/**
 * List all cases
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listCases = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single case by ID
 * @param {string} id - Case ID
 * @returns {Promise<Object>} Case data
 */
export const getCase = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new case
 * @param {Object} data - Case data
 * @returns {Promise<Object>} Created case
 */
export const createCase = async (data) => {
  return createEntity(DOMAIN, data);
};

export default {
  listCases,
  getCase,
  createCase,
};
