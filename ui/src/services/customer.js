/**
 * Customer Portal API Service
 * Handles all customer-facing API requests
 */

import api from './api';

/**
 * Get customer policies
 * @param {string} policyNumber - Policy number (optional, fetches all if not provided)
 * @returns {Promise<Object>} - Policies response
 */
export const getCustomerPolicies = async (policyNumber = null) => {
  const url = policyNumber
    ? `/customer/policies?policyNumber=${policyNumber}`
    : '/customer/policies';
  const response = await api.get(url);
  return response;
};

/**
 * Get specific policy detail
 * @param {string} policyId - Policy ID
 * @returns {Promise<Object>} - Policy detail
 */
export const getCustomerPolicy = async (policyId) => {
  const response = await api.get(`/customer/policies/${policyId}`);
  return response;
};

/**
 * Get customer claims
 * @param {string} policyNumber - Policy number (optional, fetches all if not provided)
 * @returns {Promise<Object>} - Claims response
 */
export const getCustomerClaims = async (policyNumber = null) => {
  const url = policyNumber
    ? `/customer/claims?policyNumber=${policyNumber}`
    : '/customer/claims';
  const response = await api.get(url);
  return response;
};

/**
 * Submit new claim
 * @param {Object} claimData - Claim data
 * @returns {Promise<Object>} - Created claim
 */
export const submitClaim = async (claimData) => {
  const response = await api.post('/customer/claims', claimData);
  return response;
};

/**
 * Upload claim document
 * @param {string} claimId - Claim ID
 * @param {Object} docData - Document data
 * @returns {Promise<Object>} - Upload response
 */
export const uploadClaimDocument = async (claimId, docData) => {
  const response = await api.post(`/customer/claims/${claimId}/doc`, docData);
  return response;
};

/**
 * Get customer payments
 * @param {string} policyNumber - Policy number (optional, fetches all if not provided)
 * @returns {Promise<Object>} - Payments response
 */
export const getCustomerPayments = async (policyNumber = null) => {
  const url = policyNumber
    ? `/customer/payments?policyNumber=${policyNumber}`
    : '/customer/payments';
  const response = await api.get(url);
  return response;
};
