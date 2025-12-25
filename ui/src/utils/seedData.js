/**
 * Seed Demo Data Utility
 * Creates realistic demo data across all entity types with relationships
 */

import { createQuote } from '../services/quotes';
import { createPolicy } from '../services/policies';
import { createClaim, updateStatus as updateClaimStatus } from '../services/claims';
import { createPayment } from '../services/payments';
import { createCase } from '../services/cases';
import { deleteAllEntities } from '../services/api';

// Helper data for realistic demo generation
const FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Jennifer', 'James', 'Linda', 'Richard', 'Patricia', 'Joseph', 'Mary', 'Thomas', 'Barbara', 'Charles', 'Elizabeth', 'Daniel', 'Susan', 'Matthew', 'Karen', 'Christopher'];
const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Clark'];
const CITIES = ['Miami', 'Tampa', 'Orlando', 'Atlanta', 'Charlotte', 'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin'];
const STATES = ['FL', 'GA', 'NC', 'NY', 'CA', 'IL', 'TX', 'AZ', 'PA'];
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
const VEHICLE_MAKES = ['Honda', 'Toyota', 'Ford', 'Chevrolet', 'Nissan', 'BMW', 'Mercedes', 'Audi', 'Lexus', 'Mazda'];
const VEHICLE_MODELS = ['Civic', 'Accord', 'Camry', 'Corolla', 'F-150', 'Silverado', 'Altima', 'Maxima', '3 Series', 'C-Class'];

// Helper functions
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomName = () => `${randomItem(FIRST_NAMES)} ${randomItem(LAST_NAMES)}`;
const randomEmail = (name) => {
  const domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com'];
  const safeName = name.toLowerCase().replace(' ', '.');
  return `${safeName}${randomNumber(1, 999)}@${randomItem(domains)}`;
};
const randomPhone = () => `${randomNumber(200, 999)}${randomNumber(200, 999)}${randomNumber(1000, 9999)}`;
const randomAddress = () => {
  const streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Park Blvd', 'Lake Rd', 'Hill Ct', 'Pine St', 'Cedar Ln'];
  return `${randomNumber(100, 9999)} ${randomItem(streets)}`;
};
const randomZip = () => `${randomNumber(10000, 99999)}`;
const randomDOB = () => {
  const year = randomNumber(1950, 2000);
  const month = randomNumber(1, 12);
  const day = randomNumber(1, 28);
  return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
};
const randomVIN = () => {
  const chars = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789';
  return Array.from({ length: 17 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
};
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
      const name = randomName();
      const coverage = randomItem(COVERAGE_TYPES);
      const quoteData = {
        name,
        email: randomEmail(name),
        phone: randomPhone(),
        address: randomAddress(),
        city: randomItem(CITIES),
        state: randomItem(STATES),
        zip: randomZip(),
        dateOfBirth: randomDOB(),
        premium_cents: randomNumber(50000, 300000),
        coverageType: coverage,
        coverageLimit_cents: randomNumber(10000000, 100000000),
        deductible_cents: randomItem([50000, 100000, 250000, 500000]),
        quoteNumber: `Q-2024-${(1000 + i).toString().padStart(6, '0')}`,
        status: Math.random() < 0.75 ? 'PENDING' : randomItem(QUOTE_STATUSES),
      };

      if (coverage === 'AUTO') {
        quoteData.vehicleInfo = {
          year: randomNumber(2015, 2024),
          make: randomItem(VEHICLE_MAKES),
          model: randomItem(VEHICLE_MODELS),
          vin: randomVIN()
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
      const effectiveDate = randomDateWithinDays(3650);
      const policyData = {
        quoteId: results.quotes[i]?.id,
        policyNumber: `POL-2024-${(1000 + i).toString().padStart(6, '0')}`,
        status: Math.random() < 0.8 ? 'ACTIVE' : randomItem(POLICY_STATUSES),
        holderName: randomName(),
        effectiveDate,
        expiryDate: futureDateWithinDays(effectiveDate, 365),
        renewalDate: futureDateWithinDays(effectiveDate, 15),
        premium_cents: randomNumber(100000, 400000),
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

      const claimData = {
        policyId: results.policies[i % results.policies.length]?.id,
        claimNumber: `CLM-2024-${(1000 + i).toString().padStart(6, '0')}`,
        claimantName: randomName(),
        loss: `${randomItem(LOSS_TYPES).replace('_', ' ')} incident`,
        lossType: randomItem(LOSS_TYPES),
        incidentDate: randomDateWithinDays(3650),
        reportedDate: randomDateWithinDays(3650),
        estimatedAmount_cents: estimated,
        approvedAmount_cents: approved,
        deductible_cents: randomItem([0, 50000, 100000, 250000]),
        paidAmount_cents: paid,
        description: `Claim for ${randomItem(LOSS_TYPES).replace('_', ' ').toLowerCase()} with estimated damage`,
        location: randomItem(['I-95 northbound', 'I-75 southbound', 'US-1', 'Downtown', 'Residential area', 'Parking lot']),
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
      const paymentData = {
        policyId: results.policies[i % results.policies.length]?.id,
        paymentNumber: `PAY-2024-${(1000 + i).toString().padStart(6, '0')}`,
        amount_cents: randomNumber(5000, 50000),
        status: Math.random() < 0.85 ? 'COMPLETED' : randomItem(PAYMENT_STATUSES),
        paymentMethod: randomItem(PAYMENT_METHODS),
        paymentType: Math.random() < 0.9 ? 'PREMIUM' : randomItem(PAYMENT_TYPES),
        transactionId: `txn_${randomNumber(100000, 999999)}`,
        dueDate: randomDateWithinDays(3650),
        paidDate: Math.random() < 0.85 ? randomDateWithinDays(3650) : null,
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
      const caseData = {
        caseNumber: `CS-2024-${(1000 + i).toString().padStart(6, '0')}`,
        title: `${topic.replace('_', ' ')} - Case ${i + 1}`,
        topic,
        status: Math.random() < 0.6 ? 'OPEN' : randomItem(CASE_STATUSES),
        priority: Math.random() < 0.7 ? 'MEDIUM' : randomItem(PRIORITIES),
        assignee: randomItem(ASSIGNEES),
        department: randomItem(DEPARTMENTS),
        customerName: randomName(),
        policyId: Math.random() < 0.7 ? results.policies[i % results.policies.length]?.id : null,
        description: `Customer inquiry regarding ${topic.replace('_', ' ').toLowerCase()}`,
        resolution: null,
        dueDate: futureDateWithinDays(new Date().toISOString().split('T')[0], 10),
        resolvedDate: Math.random() < 0.3 ? randomDateWithinDays(3650) : null
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
