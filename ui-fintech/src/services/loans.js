/**
 * Loan Service
 * API functions for loan entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity } from './api';

const DOMAIN = 'loan';

export const listLoans = () => listEntities(DOMAIN);
export const getLoan = (id) => getEntity(DOMAIN, id);
export const createLoan = (data) => createEntity(DOMAIN, data);
export const deleteLoan = (id) => deleteEntity(DOMAIN, id);
