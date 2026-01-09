/**
 * Card Service
 * API calls for card management
 */

import { createEntity, getEntity, listEntities } from './api';

const DOMAIN = 'card';

/**
 * List all cards
 * @returns {Promise<Object>} { items: [], count: number }
 */
export const listCards = async () => {
  return listEntities(DOMAIN);
};

/**
 * Get a single card by ID
 * @param {string} id - Card ID
 * @returns {Promise<Object>} Card data
 */
export const getCard = async (id) => {
  return getEntity(DOMAIN, id);
};

/**
 * Create a new card
 * @param {Object} data - Card data
 * @returns {Promise<Object>} Created card
 */
export const createCard = async (data) => {
  return createEntity(DOMAIN, data);
};

export default {
  listCards,
  getCard,
  createCard,
};
