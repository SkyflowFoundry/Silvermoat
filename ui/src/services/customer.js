/**
 * Customer Portal API Service
 * Handles all customer-facing API requests
 */

import api from './api';

/**
 * Authenticate customer with policy number and ZIP code
 * @param {string} policyNumber - Policy number
 * @param {string} zip - ZIP code
 * @returns {Promise<Object>} - Authentication response
 */
export const authenticateCustomer = async (policyNumber, zip) => {
  const response = await api.post('/customer/auth', {
    policyNumber,
    zip,
  });
  return response;
};

/**
 * Get customer policies
 * @param {string} policyNumber - Policy number
 * @returns {Promise<Object>} - Policies response
 */
export const getCustomerPolicies = async (policyNumber) => {
  const response = await api.get(`/customer/policies?policyNumber=${policyNumber}`);
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
 * @param {string} policyNumber - Policy number
 * @returns {Promise<Object>} - Claims response
 */
export const getCustomerClaims = async (policyNumber) => {
  const response = await api.get(`/customer/claims?policyNumber=${policyNumber}`);
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
 * @param {string} policyNumber - Policy number
 * @returns {Promise<Object>} - Payments response
 */
export const getCustomerPayments = async (policyNumber) => {
  const response = await api.get(`/customer/payments?policyNumber=${policyNumber}`);
  return response;
};
