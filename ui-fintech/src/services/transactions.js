/**
 * Transaction Service
 * API functions for transaction entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity } from './api';

const DOMAIN = 'transaction';

export const listTransactions = () => listEntities(DOMAIN);
export const getTransaction = (id) => getEntity(DOMAIN, id);
export const createTransaction = (data) => createEntity(DOMAIN, data);
export const deleteTransaction = (id) => deleteEntity(DOMAIN, id);
