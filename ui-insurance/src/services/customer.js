/**
 * Customer Portal API Service
 * Demo mode - uses regular API endpoints and filters by customer email
 */

import api from './api';

/**
 * Get customer policies filtered by customer email
 * @param {string} customerEmail - Customer email to filter by
 * @returns {Promise<Object>} - Policies response
 */
export const getCustomerPolicies = async (customerEmail) => {
  // Use backend filtering via query parameter
  const response = await api.get(`/policy?customerEmail=${encodeURIComponent(customerEmail)}`);

  return { policies: response.items, count: response.count };
};

/**
 * Get specific policy detail
 * @param {string} policyId - Policy ID
 * @returns {Promise<Object>} - Policy detail
 */
export const getCustomerPolicy = async (policyId) => {
  const response = await api.get(`/policy/${policyId}`);
  return response;
};

/**
 * Get customer claims filtered by customer (via policies)
 * @param {string} customerEmail - Customer email to filter by
 * @returns {Promise<Object>} - Claims response
 */
export const getCustomerClaims = async (customerEmail) => {
  // Use backend filtering via query parameter
  const response = await api.get(`/claim?customerEmail=${encodeURIComponent(customerEmail)}`);

  return { claims: response.items, count: response.count };
};

/**
 * Submit new claim
 * @param {Object} claimData - Claim data
 * @returns {Promise<Object>} - Created claim
 */
export const submitClaim = async (claimData) => {
  const response = await api.post('/claim', claimData);
  return response;
};

/**
 * Upload claim document
 * @param {string} claimId - Claim ID
 * @param {Object} docData - Document data
 * @returns {Promise<Object>} - Upload response
 */
export const uploadClaimDocument = async (claimId, docData) => {
  const response = await api.post(`/claim/${claimId}/doc`, docData);
  return response;
};

/**
 * Get customer payments filtered by customer (via policies)
 * @param {string} customerEmail - Customer email to filter by
 * @returns {Promise<Object>} - Payments response
 */
export const getCustomerPayments = async (customerEmail) => {
  // Use backend filtering via query parameter
  const response = await api.get(`/payment?customerEmail=${encodeURIComponent(customerEmail)}`);

  return { payments: response.items, count: response.count };
};

/**
 * Get all available customers from database
 * @returns {Promise<Array>} - Array of customer info objects
 */
export const getAvailableCustomers = async () => {
  // Limit to first 10 customers for dropdown
  const response = await api.get('/customer?limit=10');

  if (!response.items || response.items.length === 0) {
    return [{
      name: 'Demo Customer',
      email: 'demo@example.com',
    }];
  }

  // Map customer records to simple format
  return response.items.map(customer => ({
    name: customer.data?.name || 'Unknown',
    email: customer.email || 'unknown@example.com',
  }));
};

/**
 * Get a default demo customer from seeded data
 * @returns {Promise<Object>} - Customer info (name, email)
 */
export const getDefaultCustomer = async () => {
  const customers = await getAvailableCustomers();
  return customers[0];
};
