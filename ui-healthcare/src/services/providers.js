/**
 * Provider Service
 * API functions for provider entity operations (note: providers are stored as "case" in the backend)
 */

import { listEntities, getEntity, createEntity, deleteEntity } from './api';

const DOMAIN = 'case';  // Providers use the case table in backend

export const listProviders = () => listEntities(DOMAIN);
export const getProvider = (id) => getEntity(DOMAIN, id);
export const createProvider = (data) => createEntity(DOMAIN, data);
export const deleteProvider = (id) => deleteEntity(DOMAIN, id);
