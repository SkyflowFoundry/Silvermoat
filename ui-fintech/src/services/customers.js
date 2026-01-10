/**
 * Customer Service
 * API calls for customer management
 */

import { createEntity, deleteEntity, getEntity, listEntities } from './api';

const DOMAIN = 'customer';

/**
 * List all customers
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listCustomers = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single customer by ID
 * @param {string} id - Customer ID
 * @returns {Promise<Object>} Customer data
 */
export const getCustomer = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new customer
 * @param {Object} data - Customer data
 * @returns {Promise<Object>} Created customer
 */
export const createCustomer = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Delete a customer
 * @param {string} id - Customer ID
 * @returns {Promise<void>}
 */
export const deleteCustomer = async (id) => {
  return deleteEntity(DOMAIN, id);
};

export default {
  listCustomers,
  getCustomer,
  createCustomer,
  deleteCustomer,
};
