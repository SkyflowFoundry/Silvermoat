/**
 * Seed Demo Data Utility
 * Creates realistic demo data across all entity types with relationships
 */

import { createQuote } from '../services/quotes';
import { createPolicy } from '../services/policies';
import { createClaim } from '../services/claims';
import { createPayment } from '../services/payments';
import { createCase } from '../services/cases';
import { deleteAllEntities } from '../services/api';

// Demo data templates
const DEMO_QUOTES = [
  { name: 'John Smith', zip: '10001' },
  { name: 'Sarah Johnson', zip: '90210' },
  { name: 'Michael Chen', zip: '60601' },
  { name: 'Emily Davis', zip: '02108' },
  { name: 'Robert Williams', zip: '33101' },
];

const POLICY_HOLDERS = [
  'John Smith',
  'Sarah Johnson',
  'Michael Chen',
  'Emily Davis',
  'Robert Williams',
];

const CLAIMANT_NAMES = [
  'John Smith',
  'Sarah Johnson',
  'Michael Chen',
  'Emily Davis',
  'Robert Williams',
];

const CLAIM_DESCRIPTIONS = [
  'Vehicle collision on highway. Damage to front bumper and hood.',
  'Water damage from burst pipe in basement. Flooring and drywall affected.',
  'Theft of personal belongings from vehicle. Police report filed.',
  'Storm damage to roof and siding. Significant repair needed.',
  'Kitchen fire from cooking accident. Smoke and fire damage.',
];

const CASE_TITLES = [
  'Policy renewal inquiry',
  'Coverage dispute investigation',
  'Payment processing issue',
  'Documentation request follow-up',
  'Premium adjustment request',
];

const CASE_DESCRIPTIONS = [
  'Customer requesting clarification on renewal terms and premium changes.',
  'Investigating claim denial to ensure proper coverage assessment.',
  'Payment not reflected in system. Verifying transaction details.',
  'Waiting for additional documentation from customer to process claim.',
  'Customer requesting review of premium calculation based on updated risk factors.',
];

const ASSIGNEES = [
  'Alice Thompson',
  'Bob Martinez',
  'Carol Peterson',
  'David Lee',
  'Emma Wilson',
];

// Helper to generate random date within last N days
const randomDateWithinDays = (days) => {
  const now = new Date();
  const past = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  const randomTime = past.getTime() + Math.random() * (now.getTime() - past.getTime());
  return new Date(randomTime).toISOString().split('T')[0];
};

// Helper to generate future date within N days
const futureDateWithinDays = (startDate, days) => {
  const start = new Date(startDate);
  const future = new Date(start.getTime() + days * 24 * 60 * 60 * 1000);
  return future.toISOString().split('T')[0];
};

// Helper to pick random item from array
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

// Helper to generate random number in range
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

/**
 * Seeds demo data across all entities
 * @param {Function} onProgress - Callback for progress updates (message, current, total)
 * @returns {Promise<Object>} Object containing created entities
 */
export const seedDemoData = async (onProgress) => {
  const results = {
    quotes: [],
    policies: [],
    claims: [],
    payments: [],
    cases: [],
  };

  let step = 0;
  const totalSteps = 25; // 5 quotes + 5 policies + 5 claims + 5 payments + 5 cases

  try {
    // Step 1: Create Quotes
    onProgress?.('Creating demo quotes...', step, totalSteps);
    for (const quoteData of DEMO_QUOTES) {
      const result = await createQuote(quoteData);
      results.quotes.push(result.item);
      step++;
      onProgress?.(`Created quote for ${quoteData.name}`, step, totalSteps);
    }

    // Step 2: Create Policies (linked to quotes)
    onProgress?.('Creating demo policies...', step, totalSteps);
    for (let i = 0; i < 5; i++) {
      const effectiveDate = randomDateWithinDays(3650);
      const expirationDate = futureDateWithinDays(effectiveDate, 365);

      const policyData = {
        quoteId: results.quotes[i]?.id,
        policyNumber: `POL-${1000 + i}`,
        holderName: POLICY_HOLDERS[i],
        effectiveDate,
        expirationDate,
        premium: randomNumber(500, 3000),
        status: randomItem(['ACTIVE', 'ACTIVE', 'ACTIVE', 'EXPIRED', 'CANCELLED']), // 60% active
      };

      const result = await createPolicy(policyData);
      results.policies.push(result.item);
      step++;
      onProgress?.(`Created policy ${policyData.policyNumber}`, step, totalSteps);
    }

    // Step 3: Create Claims (linked to policies)
    onProgress?.('Creating demo claims...', step, totalSteps);
    for (let i = 0; i < 5; i++) {
      const claimData = {
        policyId: results.policies[i]?.id,
        claimNumber: `CLM-${2000 + i}`,
        claimantName: CLAIMANT_NAMES[i],
        incidentDate: randomDateWithinDays(3650),
        description: CLAIM_DESCRIPTIONS[i],
        amount: randomNumber(1000, 25000),
        status: randomItem(['PENDING', 'REVIEW', 'APPROVED', 'DENIED']),
      };

      const result = await createClaim(claimData);
      results.claims.push(result.item);
      step++;
      onProgress?.(`Created claim ${claimData.claimNumber}`, step, totalSteps);
    }

    // Step 4: Create Payments (linked to policies)
    onProgress?.('Creating demo payments...', step, totalSteps);
    for (let i = 0; i < 5; i++) {
      const paymentData = {
        policyId: results.policies[i]?.id,
        paymentDate: randomDateWithinDays(3650),
        amount: randomNumber(100, 500),
        method: randomItem(['CARD', 'ACH', 'CHECK']),
        status: randomItem(['PENDING', 'COMPLETED', 'COMPLETED', 'COMPLETED', 'FAILED']), // 60% completed
      };

      const result = await createPayment(paymentData);
      results.payments.push(result.item);
      step++;
      onProgress?.(`Created payment for policy ${i + 1}`, step, totalSteps);
    }

    // Step 5: Create Cases (linked to various entities)
    onProgress?.('Creating demo cases...', step, totalSteps);
    const entityTypes = ['quote', 'policy', 'claim', 'policy', 'claim'];

    for (let i = 0; i < 5; i++) {
      const entityType = entityTypes[i];
      let relatedEntityId;

      if (entityType === 'quote') {
        relatedEntityId = results.quotes[i]?.id;
      } else if (entityType === 'policy') {
        relatedEntityId = results.policies[i % results.policies.length]?.id;
      } else if (entityType === 'claim') {
        relatedEntityId = results.claims[i % results.claims.length]?.id;
      }

      const caseData = {
        title: CASE_TITLES[i],
        description: CASE_DESCRIPTIONS[i],
        relatedEntityType: entityType,
        relatedEntityId,
        assignee: ASSIGNEES[i],
        priority: randomItem(['LOW', 'MEDIUM', 'HIGH']),
        status: randomItem(['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED']),
      };

      const result = await createCase(caseData);
      results.cases.push(result.item);
      step++;
      onProgress?.(`Created case: ${caseData.title}`, step, totalSteps);
    }

    onProgress?.('Demo data seeding complete!', totalSteps, totalSteps);
    return results;
  } catch (error) {
    console.error('Error seeding demo data:', error);
    throw error;
  }
};

/**
 * Returns summary statistics of seeded data
 */
export const getSeedDataSummary = (results) => {
  return {
    total: Object.values(results).reduce((sum, arr) => sum + arr.length, 0),
    quotes: results.quotes.length,
    policies: results.policies.length,
    claims: results.claims.length,
    payments: results.payments.length,
    cases: results.cases.length,
  };
};

/**
 * Clears all data from all entity types
 * @param {Function} onProgress - Callback for progress updates (message, current, total)
 * @returns {Promise<Object>} Object containing deletion counts
 */
export const clearAllData = async (onProgress) => {
  const domains = ['quote', 'policy', 'claim', 'payment', 'case'];
  const results = {
    quotes: 0,
    policies: 0,
    claims: 0,
    payments: 0,
    cases: 0,
  };

  let step = 0;
  const totalSteps = domains.length;

  try {
    for (const domain of domains) {
      onProgress?.(`Clearing ${domain}s...`, step, totalSteps);
      const result = await deleteAllEntities(domain);

      // Map domain to result key
      const key = domain === 'case' ? 'cases' : `${domain}s`;
      results[key] = result.deleted || 0;

      step++;
      onProgress?.(`Cleared ${result.deleted || 0} ${domain}s`, step, totalSteps);
    }

    onProgress?.('All data cleared!', totalSteps, totalSteps);
    return results;
  } catch (error) {
    console.error('Error clearing data:', error);
    throw error;
  }
};
