/**
 * Patient Service
 * API functions for patient entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity } from './api';

const DOMAIN = 'patient';

export const listPatients = () => listEntities(DOMAIN);
export const getPatient = (id) => getEntity(DOMAIN, id);
export const createPatient = (data) => createEntity(DOMAIN, data);
export const deletePatient = (id) => deleteEntity(DOMAIN, id);
