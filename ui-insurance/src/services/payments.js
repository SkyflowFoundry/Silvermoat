/**
 * Payment Service
 * API methods specific to payments
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'payment';

/**
 * List all payments
 * @returns {Promise<object>} Object with items and count
 */
export const listPayments = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new payment
 * @param {object} data - Payment data
 * @returns {Promise<object>} Created payment
 */
export const createPayment = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a payment by ID
 * @param {string} id - Payment ID
 * @returns {Promise<object>} Payment data
 */
export const getPayment = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listPayments,
  createPayment,
  getPayment,
};
