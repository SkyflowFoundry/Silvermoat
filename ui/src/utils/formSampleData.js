/**
 * Form Sample Data Generators
 * Provides sample data for form auto-fill functionality
 * Uses Faker.js and shared helpers from seedData.js
 */

import { faker } from '@faker-js/faker';
import { randomItem, randomNumber } from './seedData';

// Insurance-specific constants
const LOSS_TYPES = ['AUTO_COLLISION', 'AUTO_GLASS', 'AUTO_THEFT', 'PROPERTY_DAMAGE', 'WATER_DAMAGE', 'FIRE', 'THEFT', 'VANDALISM'];
const PAYMENT_METHODS = ['CREDIT_CARD', 'ACH', 'CHECK'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const ASSIGNEES = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Miller'];

// Helper functions
const randomDateWithinDays = (days) => {
  const now = new Date();
  const past = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  const randomTime = past.getTime() + Math.random() * (now.getTime() - past.getTime());
  return new Date(randomTime).toISOString().split('T')[0];
};

const futureDateWithinDays = (startDate, days) => {
  const start = new Date(startDate);
  const future = new Date(start.getTime() + days * 24 * 60 * 60 * 1000);
  return future.toISOString().split('T')[0];
};

/**
 * Generate sample data for Quote form
 * @returns {Object} Sample quote data matching QuoteForm fields
 */
export const generateQuoteSampleData = () => {
  return {
    name: faker.person.fullName(),
    zip: faker.location.zipCode('#####'),
  };
};

/**
 * Generate sample data for Policy form
 * @returns {Object} Sample policy data matching PolicyForm fields
 */
export const generatePolicySampleData = () => {
  const effectiveDate = randomDateWithinDays(30);
  const premium = randomNumber(1000, 4000); // In dollars (form converts to cents)

  return {
    policyNumber: `POL-2024-${randomNumber(100000, 999999)}`,
    holderName: faker.person.fullName(),
    effectiveDate,
    expirationDate: futureDateWithinDays(effectiveDate, 365),
    premium,
    status: 'ACTIVE',
  };
};

/**
 * Generate sample data for Claim form
 * @returns {Object} Sample claim data matching ClaimForm fields
 */
export const generateClaimSampleData = () => {
  const lossType = randomItem(LOSS_TYPES);
  const amount = randomNumber(100, 50000); // In dollars (form converts to cents)

  return {
    claimNumber: `CLM-2024-${randomNumber(100000, 999999)}`,
    claimantName: faker.person.fullName(),
    incidentDate: randomDateWithinDays(90),
    description: `${lossType.replace('_', ' ')} incident - Sample claim for testing purposes. This is a demonstration of the auto-fill functionality.`,
    amount,
    status: 'PENDING',
  };
};

/**
 * Generate sample data for Payment form
 * @returns {Object} Sample payment data matching PaymentForm fields
 */
export const generatePaymentSampleData = () => {
  const amount = randomNumber(100, 1000); // In dollars (form converts to cents)

  return {
    paymentDate: new Date().toISOString().split('T')[0], // Today
    amount,
    method: randomItem(PAYMENT_METHODS),
    status: 'COMPLETED',
    policyId: `POL-2024-${randomNumber(100000, 999999)}`, // Required field
  };
};

/**
 * Generate sample data for Case form
 * @returns {Object} Sample case data matching CaseForm fields
 */
export const generateCaseSampleData = () => {
  const topics = ['Policy Change Request', 'Claim Inquiry', 'Billing Question', 'Coverage Question', 'General Inquiry'];
  const entityTypes = ['quote', 'policy', 'claim'];

  return {
    title: randomItem(topics),
    description: `Sample case for testing purposes. Customer inquiring about ${randomItem(topics).toLowerCase()}. This is a demonstration of the auto-fill functionality.`,
    relatedEntityType: randomItem(entityTypes),
    relatedEntityId: `${randomItem(['Q', 'POL', 'CLM'])}-2024-${randomNumber(100000, 999999)}`,
    assignee: randomItem(ASSIGNEES),
    priority: 'MEDIUM',
    status: 'OPEN',
  };
};
