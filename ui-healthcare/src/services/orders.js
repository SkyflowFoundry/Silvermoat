/**
 * Order Service
 * API calls for order management
 */

import { createEntity, getEntity, listEntities, updateOrderStatus as apiUpdateOrderStatus } from './api';

const DOMAIN = 'order';

/**
 * List all orders
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listOrders = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single order by ID
 * @param {string} id - Order ID
 * @returns {Promise<Object>} Order data
 */
export const getOrder = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new order
 * @param {Object} data - Order data
 * @returns {Promise<Object>} Created order
 */
export const createOrder = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Update order status
 * @param {string} orderId - Order ID
 * @param {string} status - New status (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
 * @returns {Promise<Object>} Updated order
 */
export const updateOrderStatus = async (orderId, status) => {
  return apiUpdateOrderStatus(orderId, status);
};

export default {
  listOrders,
  getOrder,
  createOrder,
  updateOrderStatus,
};
