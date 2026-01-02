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
  const response = await api.get('/policy');

  // Filter policies by customer email
  const policies = response.items.filter(
    policy => policy.data?.customer_email === customerEmail
  );

  return { policies, count: policies.length };
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
  // Get customer's policies first to find policy IDs
  const policiesResponse = await getCustomerPolicies(customerEmail);
  const policyIds = policiesResponse.policies.map(p => p.id);

  // Get all claims
  const response = await api.get('/claim');

  // Filter claims by customer's policy IDs
  const claims = response.items.filter(
    claim => policyIds.includes(claim.data?.policy_id)
  );

  return { claims, count: claims.length };
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
  // Get customer's policies first to find policy IDs
  const policiesResponse = await getCustomerPolicies(customerEmail);
  const policyIds = policiesResponse.policies.map(p => p.id);

  // Get all payments
  const response = await api.get('/payment');

  // Filter payments by customer's policy IDs
  const payments = response.items.filter(
    payment => policyIds.includes(payment.data?.policy_id)
  );

  return { payments, count: payments.length };
};

/**
 * Get a default demo customer from seeded data
 * @returns {Promise<Object>} - Customer info (name, email)
 */
export const getDefaultCustomer = async () => {
  // Get first policy to extract customer info
  const response = await api.get('/policy');

  if (response.items && response.items.length > 0) {
    const firstPolicy = response.items[0];
    return {
      name: firstPolicy.data?.customer_name || 'Demo Customer',
      email: firstPolicy.data?.customer_email || 'demo@example.com',
    };
  }

  // Fallback if no data
  return {
    name: 'Demo Customer',
    email: 'demo@example.com',
  };
};
