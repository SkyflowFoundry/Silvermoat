/**
 * Case Service
 * API methods specific to cases
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'case';

/**
 * List all cases
 * @returns {Promise<object>} Object with items and count
 */
export const listCases = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new case
 * @param {object} data - Case data
 * @returns {Promise<object>} Created case
 */
export const createCase = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a case by ID
 * @param {string} id - Case ID
 * @returns {Promise<object>} Case data
 */
export const getCase = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listCases,
  createCase,
  getCase,
};
