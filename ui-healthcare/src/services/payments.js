/**
 * Payment Service
 * API calls for payment management
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'payment';

/**
 * List all payments
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listPayments = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single payment by ID
 * @param {string} id - Payment ID
 * @returns {Promise<Object>} Payment data
 */
export const getPayment = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new payment
 * @param {Object} data - Payment data
 * @returns {Promise<Object>} Created payment
 */
export const createPayment = async (data) => {
  return createEntity(DOMAIN, data);
};

export default {
  listPayments,
  getPayment,
  createPayment,
};
