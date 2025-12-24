/**
 * Quote Service
 * API methods specific to quotes
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'quote';

/**
 * List all quotes
 * @returns {Promise<object>} Object with items and count
 */
export const listQuotes = async () => {
  return listEntities(DOMAIN);
};

/**
 * Create a new quote
 * @param {object} data - Quote data { name, zip }
 * @returns {Promise<object>} Created quote
 */
export const createQuote = async (data) => {
  return createEntity(DOMAIN, data);
};

/**
 * Get a quote by ID
 * @param {string} id - Quote ID
 * @returns {Promise<object>} Quote data
 */
export const getQuote = async (id) => {
  return getEntity(DOMAIN, id);
};

export default {
  listQuotes,
  createQuote,
  getQuote,
};
