/**
 * Form Sample Data Generators
 * Provides sample data for form auto-fill functionality
 * Reuses helpers from seedData.js for consistency
 */

// Helper data for realistic sample generation
const FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Jennifer'];
const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
const CITIES = ['Miami', 'Tampa', 'Orlando', 'Atlanta', 'Charlotte', 'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'];
const STATES = ['FL', 'GA', 'NC', 'NY', 'CA', 'IL', 'TX', 'AZ', 'PA'];
const LOSS_TYPES = ['AUTO_COLLISION', 'AUTO_GLASS', 'AUTO_THEFT', 'PROPERTY_DAMAGE', 'WATER_DAMAGE', 'FIRE', 'THEFT', 'VANDALISM'];
const PAYMENT_METHODS = ['CREDIT_CARD', 'ACH', 'CHECK'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const ASSIGNEES = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Miller'];

// Helper functions (duplicated from seedData.js for independence)
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomName = () => `${randomItem(FIRST_NAMES)} ${randomItem(LAST_NAMES)}`;
const randomZip = () => `${randomNumber(10000, 99999)}`;
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
    name: randomName(),
    zip: randomZip(),
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
    holderName: randomName(),
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
    claimantName: randomName(),
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
