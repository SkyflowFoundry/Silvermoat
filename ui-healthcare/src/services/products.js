/**
 * Product Service
 * API methods specific to products
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'product';

/**
 * List all products
 * @returns {Promise<object>} Object with items and count
 */
export const listProducts = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new product
 * @param {object} data - Product data { name, sku, price, category, description, stockLevel }
 * @returns {Promise<object>} Created product
 */
export const createProduct = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a product by ID
 * @param {string} id - Product ID
 * @returns {Promise<object>} Product data
 */
export const getProduct = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listProducts,
  createProduct,
  getProduct,
};
