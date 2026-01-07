/**
 * Prescription Service
 * API functions for prescription entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity, updateEntityStatus } from './api';

const DOMAIN = 'prescription';

export const listPrescriptions = () => listEntities(DOMAIN);
export const getPrescription = (id) => getEntity(DOMAIN, id);
export const createPrescription = (data) => createEntity(DOMAIN, data);
export const deletePrescription = (id) => deleteEntity(DOMAIN, id);
export const updatePrescriptionStatus = (id, status) => updateEntityStatus(DOMAIN, id, status);
