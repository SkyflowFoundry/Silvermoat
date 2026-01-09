/**
 * Account Service
 * API functions for account entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity } from './api';

const DOMAIN = 'account';

export const listAccounts = () => listEntities(DOMAIN);
export const getAccount = (id) => getEntity(DOMAIN, id);
export const createAccount = (data) => createEntity(DOMAIN, data);
export const deleteAccount = (id) => deleteEntity(DOMAIN, id);
