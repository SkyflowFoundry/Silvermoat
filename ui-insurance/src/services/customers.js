/**
 * Customer Service
 * API methods specific to customers (employee side)
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'customer';

/**
 * List all customers
 * @returns {Promise<object>} Object with items and count
 */
export const listCustomers = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new customer
 * @param {object} data - Customer data { name, email, address, phone }
 * @returns {Promise<object>} Created customer
 */
export const createCustomer = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a customer by ID
 * @param {string} id - Customer ID
 * @returns {Promise<object>} Customer data
 */
export const getCustomer = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listCustomers,
  createCustomer,
  getCustomer,
};
