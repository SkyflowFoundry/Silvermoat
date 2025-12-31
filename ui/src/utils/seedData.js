/**
 * Seed Demo Data Utility
 * Creates realistic demo data across all entity types with relationships
 * Uses Faker.js for realistic data generation
 */

import { faker } from '@faker-js/faker';
import { createQuote } from '../services/quotes';
import { createPolicy } from '../services/policies';
import { createClaim, updateStatus as updateClaimStatus } from '../services/claims';
import { createPayment } from '../services/payments';
import { createCase } from '../services/cases';
import { deleteAllEntities } from '../services/api';

// Insurance-specific constants
const COVERAGE_TYPES = ['AUTO', 'HOME', 'LIFE', 'HEALTH'];
const QUOTE_STATUSES = ['PENDING', 'ACCEPTED', 'DECLINED', 'EXPIRED'];
const POLICY_STATUSES = ['ACTIVE', 'EXPIRED', 'CANCELLED', 'SUSPENDED'];
const PAYMENT_SCHEDULES = ['MONTHLY', 'QUARTERLY', 'ANNUAL'];
const CLAIM_STATUSES = ['INTAKE', 'PENDING', 'REVIEW', 'APPROVED', 'DENIED', 'CLOSED'];
const LOSS_TYPES = ['AUTO_COLLISION', 'AUTO_GLASS', 'AUTO_THEFT', 'PROPERTY_DAMAGE', 'WATER_DAMAGE', 'FIRE', 'THEFT', 'VANDALISM'];
const PAYMENT_STATUSES = ['PENDING', 'COMPLETED', 'FAILED', 'REFUNDED'];
const PAYMENT_METHODS = ['CREDIT_CARD', 'ACH', 'CHECK', 'WIRE'];
const PAYMENT_TYPES = ['PREMIUM', 'CLAIM', 'REFUND'];
const CASE_TOPICS = ['POLICY_CHANGE', 'CLAIM_INQUIRY', 'BILLING', 'COMPLAINT', 'COVERAGE_QUESTION', 'CANCELLATION'];
const CASE_STATUSES = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const ASSIGNEES = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Miller'];
const DEPARTMENTS = ['CUSTOMER_SERVICE', 'CLAIMS', 'BILLING', 'UNDERWRITING'];

// Helper functions
export const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
export const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

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
 * Seeds demo data across all entities
 * @param {Function} onProgress - Callback for progress updates (message, current, total)
 * @param {number} count - Number of records to create per entity type (default: 25, max: 1000)
 * @returns {Promise<Object>} Object containing created entities
 */
export const seedDemoData = async (onProgress, count = 25) => {
  const results = {
    quotes: [],
    policies: [],
    claims: [],
    payments: [],
    cases: [],
  };

  let step = 0;
  const totalSteps = count * 5; // count * (quotes + policies + claims + payments + cases)

  try {
    // Step 1: Create Quotes with rich data
    onProgress?.('Creating demo quotes...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      const name = faker.person.fullName();
      const coverage = randomItem(COVERAGE_TYPES);
      const quoteData = {
        name,
        email: faker.internet.email({ firstName: name.split(' ')[0], lastName: name.split(' ')[1] }),
        phone: faker.phone.number('##########'),
        address: faker.location.streetAddress(),
        city: faker.location.city(),
        state: faker.location.state({ abbreviated: true }),
        zip: faker.location.zipCode('#####'),
        dateOfBirth: faker.date.birthdate({ min: 18, max: 75, mode: 'age' }).toISOString().split('T')[0],
        premium_cents: randomNumber(50000, 300000),
        coverageType: coverage,
        coverageLimit_cents: randomNumber(10000000, 100000000),
        deductible_cents: randomItem([50000, 100000, 250000, 500000]),
        quoteNumber: `Q-2024-${(1000 + i).toString().padStart(6, '0')}`,
        status: Math.random() < 0.75 ? 'PENDING' : randomItem(QUOTE_STATUSES),
      };

      if (coverage === 'AUTO') {
        quoteData.vehicleInfo = {
          year: faker.date.past({ years: 10 }).getFullYear() + 10,
          make: faker.vehicle.manufacturer(),
          model: faker.vehicle.model(),
          vin: faker.vehicle.vin()
        };
      }

      const result = await createQuote(quoteData);
      results.quotes.push(result.item);
      step++;
      onProgress?.(`Created quote ${i + 1}/${count}`, step, totalSteps);
    }

    // Step 2: Create Policies
    onProgress?.('Creating demo policies...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      // Use recent dates (last 365 days) for better chart visualization
      const effectiveDate = randomDateWithinDays(365);
      const premium = randomNumber(100000, 400000);
      const policyData = {
        quoteId: results.quotes[i]?.id,
        policyNumber: `POL-2024-${(1000 + i).toString().padStart(6, '0')}`,
        status: Math.random() < 0.8 ? 'ACTIVE' : randomItem(POLICY_STATUSES),
        holderName: faker.person.fullName(),
        effectiveDate,
        expirationDate: futureDateWithinDays(effectiveDate, 365),
        expiryDate: futureDateWithinDays(effectiveDate, 365),
        renewalDate: futureDateWithinDays(effectiveDate, 15),
        premium,
        premium_cents: premium,
        paymentSchedule: randomItem(PAYMENT_SCHEDULES),
        coverageLimit_cents: randomNumber(25000000, 100000000),
        deductible_cents: randomItem([50000, 100000, 250000, 500000]),
        coverageType: randomItem(COVERAGE_TYPES),
        coverageDetails: {
          liability: randomNumber(10000000, 50000000),
          collision: randomNumber(25000000, 100000000),
          comprehensive: randomNumber(25000000, 100000000)
        }
      };

      const result = await createPolicy(policyData);
      results.policies.push(result.item);
      step++;
      onProgress?.(`Created policy ${i + 1}/${count}`, step, totalSteps);
    }

    // Step 3: Create Claims
    onProgress?.('Creating demo claims...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      const statusDist = Math.random();
      let status;
      if (statusDist < 0.3) status = 'INTAKE';
      else if (statusDist < 0.55) status = 'PENDING';
      else if (statusDist < 0.75) status = 'APPROVED';
      else if (statusDist < 0.9) status = 'REVIEW';
      else status = 'DENIED';

      const estimated = randomNumber(10000, 5000000);
      const approved = ['APPROVED', 'CLOSED'].includes(status)
        ? Math.floor(estimated * (0.8 + Math.random() * 0.2))
        : null;
      // For APPROVED claims, set paidAmount equal to approved amount (for dashboard stats)
      const paid = status === 'APPROVED' && approved ? approved : (status === 'CLOSED' && approved ? approved : null);

      // Use recent dates (last 365 days) for better chart visualization
      const incidentDate = randomDateWithinDays(365);
      const claimData = {
        policyId: results.policies[i % results.policies.length]?.id,
        claimNumber: `CLM-2024-${(1000 + i).toString().padStart(6, '0')}`,
        claimantName: faker.person.fullName(),
        loss: `${randomItem(LOSS_TYPES).replace('_', ' ')} incident`,
        lossType: randomItem(LOSS_TYPES),
        incidentDate,
        reportedDate: incidentDate,
        amount: estimated,
        estimatedAmount_cents: estimated,
        approvedAmount_cents: approved,
        deductible_cents: randomItem([0, 50000, 100000, 250000]),
        paidAmount_cents: paid,
        status,
        description: `Claim for ${randomItem(LOSS_TYPES).replace('_', ' ').toLowerCase()} with estimated damage`,
        location: faker.location.streetAddress(),
        adjusterName: randomItem(ASSIGNEES),
        adjusterNotes: ['PENDING', 'REVIEW'].includes(status) ? 'Under review' : 'Claim processed'
      };

      const result = await createClaim(claimData);

      // Update claim status at root level (required for dashboard stats)
      await updateClaimStatus(result.item.id, status);

      results.claims.push(result.item);
      step++;
      onProgress?.(`Created claim ${i + 1}/${count}`, step, totalSteps);
    }

    // Step 4: Create Payments
    onProgress?.('Creating demo payments...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      const amount = randomNumber(5000, 50000);
      // Use recent dates (last 365 days) for better chart visualization
      const paidDate = Math.random() < 0.85 ? randomDateWithinDays(365) : null;
      const paymentData = {
        policyId: results.policies[i % results.policies.length]?.id,
        paymentNumber: `PAY-2024-${(1000 + i).toString().padStart(6, '0')}`,
        amount,
        amount_cents: amount,
        status: Math.random() < 0.85 ? 'COMPLETED' : randomItem(PAYMENT_STATUSES),
        method: randomItem(PAYMENT_METHODS),
        paymentMethod: randomItem(PAYMENT_METHODS),
        paymentDate: paidDate,
        paymentType: Math.random() < 0.9 ? 'PREMIUM' : randomItem(PAYMENT_TYPES),
        transactionId: `txn_${randomNumber(100000, 999999)}`,
        dueDate: randomDateWithinDays(365),
        paidDate,
        description: `Payment for policy ${i + 1}`,
        lastFourDigits: `${randomNumber(1000, 9999)}`
      };

      const result = await createPayment(paymentData);
      results.payments.push(result.item);
      step++;
      onProgress?.(`Created payment ${i + 1}/${count}`, step, totalSteps);
    }

    // Step 5: Create Cases
    onProgress?.('Creating demo cases...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      const topic = randomItem(CASE_TOPICS);
      const hasRelatedEntity = Math.random() < 0.7;
      const relatedType = hasRelatedEntity ? randomItem(['policy', 'claim', 'quote']) : null;
      const caseData = {
        caseNumber: `CS-2024-${(1000 + i).toString().padStart(6, '0')}`,
        title: `${topic.replace('_', ' ')} - Case ${i + 1}`,
        topic,
        status: Math.random() < 0.6 ? 'OPEN' : randomItem(CASE_STATUSES),
        priority: Math.random() < 0.7 ? 'MEDIUM' : randomItem(PRIORITIES),
        assignee: randomItem(ASSIGNEES),
        department: randomItem(DEPARTMENTS),
        customerName: faker.person.fullName(),
        policyId: Math.random() < 0.7 ? results.policies[i % results.policies.length]?.id : null,
        relatedEntityType: relatedType,
        description: `Customer inquiry regarding ${topic.replace('_', ' ').toLowerCase()}`,
        resolution: null,
        dueDate: futureDateWithinDays(new Date().toISOString().split('T')[0], 10),
        // Use recent dates (last 180 days) for consistency
        resolvedDate: Math.random() < 0.3 ? randomDateWithinDays(180) : null
      };

      const result = await createCase(caseData);
      results.cases.push(result.item);
      step++;
      onProgress?.(`Created case ${i + 1}/${count}`, step, totalSteps);
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
