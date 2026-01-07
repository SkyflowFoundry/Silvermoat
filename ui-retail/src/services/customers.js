/**
 * Customer Service
 * API calls for customer management
 */

import { get } from './api';

/**
 * Get customer orders by email
 * @param {string} email - Customer email
 * @returns {Promise<Object>} { orders: [] }
 */
export const getCustomerOrders = async (email) => {
  return get(`/customer/orders?email=${encodeURIComponent(email)}`);
};

export default {
  getCustomerOrders,
};
