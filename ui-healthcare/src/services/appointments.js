/**
 * Appointment Service
 * API functions for appointment entity operations
 */

import { listEntities, getEntity, createEntity, deleteEntity, updateEntityStatus } from './api';

const DOMAIN = 'appointment';

export const listAppointments = () => listEntities(DOMAIN);
export const getAppointment = (id) => getEntity(DOMAIN, id);
export const createAppointment = (data) => createEntity(DOMAIN, data);
export const deleteAppointment = (id) => deleteEntity(DOMAIN, id);
export const updateAppointmentStatus = (id, status) => updateEntityStatus(DOMAIN, id, status);
