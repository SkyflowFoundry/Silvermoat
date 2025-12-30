import { createEntity, getEntity, listEntities, deleteEntity } from './api';

const DOMAIN = 'customer';

export const listCustomers = () => listEntities(DOMAIN);
export const createCustomer = (data) => createEntity(DOMAIN, data);
export const getCustomer = (id) => getEntity(DOMAIN, id);
export const deleteCustomer = (id) => deleteEntity(DOMAIN, id);
