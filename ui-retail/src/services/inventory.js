/**
 * Inventory Service
 * API calls for inventory management
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'inventory';

/**
 * List all inventory items
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listInventory = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single inventory item by ID
 * @param {string} id - Inventory item ID
 * @returns {Promise<Object>} Inventory item data
 */
export const getInventoryItem = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new inventory item
 * @param {Object} data - Inventory item data
 * @returns {Promise<Object>} Created inventory item
 */
export const createInventoryItem = async (data) => {
  return createEntity(DOMAIN, data);
};

export default {
  listInventory,
  getInventoryItem,
  createInventoryItem,
};
