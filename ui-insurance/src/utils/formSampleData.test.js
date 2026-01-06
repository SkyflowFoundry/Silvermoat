/**
 * Tests for Form Sample Data Generators
 */

import { describe, it, expect } from 'vitest';
import {
  generateQuoteSampleData,
  generatePolicySampleData,
  generateClaimSampleData,
  generatePaymentSampleData,
  generateCaseSampleData,
} from './formSampleData';

describe('formSampleData', () => {
  describe('generateQuoteSampleData', () => {
    it('returns valid quote data structure', () => {
      const data = generateQuoteSampleData();

      expect(data).toHaveProperty('name');
      expect(data).toHaveProperty('zip');
      expect(typeof data.name).toBe('string');
      expect(typeof data.zip).toBe('string');
      expect(data.name.length).toBeGreaterThan(0);
      expect(data.zip).toMatch(/^\d{5}$/);
    });
  });

  describe('generatePolicySampleData', () => {
    it('returns valid policy data structure', () => {
      const data = generatePolicySampleData();

      expect(data).toHaveProperty('policyNumber');
      expect(data).toHaveProperty('holderName');
      expect(data).toHaveProperty('effectiveDate');
      expect(data).toHaveProperty('expirationDate');
      expect(data).toHaveProperty('premium');
      expect(data).toHaveProperty('status');

      expect(typeof data.policyNumber).toBe('string');
      expect(data.policyNumber).toMatch(/^POL-2024-\d{6}$/);
      expect(typeof data.holderName).toBe('string');
      expect(typeof data.effectiveDate).toBe('string');
      expect(typeof data.expirationDate).toBe('string');
      expect(typeof data.premium).toBe('number');
      expect(data.premium).toBeGreaterThan(0);
      expect(data.status).toBe('ACTIVE');
    });

    it('generates expiration date after effective date', () => {
      const data = generatePolicySampleData();
      const effective = new Date(data.effectiveDate);
      const expiration = new Date(data.expirationDate);

      expect(expiration > effective).toBe(true);
    });
  });

  describe('generateClaimSampleData', () => {
    it('returns valid claim data structure', () => {
      const data = generateClaimSampleData();

      expect(data).toHaveProperty('claimNumber');
      expect(data).toHaveProperty('claimantName');
      expect(data).toHaveProperty('incidentDate');
      expect(data).toHaveProperty('description');
      expect(data).toHaveProperty('amount');
      expect(data).toHaveProperty('status');

      expect(typeof data.claimNumber).toBe('string');
      expect(data.claimNumber).toMatch(/^CLM-2024-\d{6}$/);
      expect(typeof data.claimantName).toBe('string');
      expect(typeof data.incidentDate).toBe('string');
      expect(typeof data.description).toBe('string');
      expect(typeof data.amount).toBe('number');
      expect(data.amount).toBeGreaterThan(0);
      expect(data.status).toBe('PENDING');
    });
  });

  describe('generatePaymentSampleData', () => {
    it('returns valid payment data structure', () => {
      const data = generatePaymentSampleData();

      expect(data).toHaveProperty('paymentDate');
      expect(data).toHaveProperty('amount');
      expect(data).toHaveProperty('method');
      expect(data).toHaveProperty('status');
      expect(data).toHaveProperty('policyId');

      expect(typeof data.paymentDate).toBe('string');
      expect(typeof data.amount).toBe('number');
      expect(data.amount).toBeGreaterThan(0);
      expect(typeof data.method).toBe('string');
      expect(['CREDIT_CARD', 'ACH', 'CHECK']).toContain(data.method);
      expect(data.status).toBe('COMPLETED');
      expect(typeof data.policyId).toBe('string');
      expect(data.policyId).toMatch(/^POL-2024-\d{6}$/);
    });
  });

  describe('generateCaseSampleData', () => {
    it('returns valid case data structure', () => {
      const data = generateCaseSampleData();

      expect(data).toHaveProperty('title');
      expect(data).toHaveProperty('description');
      expect(data).toHaveProperty('relatedEntityType');
      expect(data).toHaveProperty('relatedEntityId');
      expect(data).toHaveProperty('assignee');
      expect(data).toHaveProperty('priority');
      expect(data).toHaveProperty('status');

      expect(typeof data.title).toBe('string');
      expect(typeof data.description).toBe('string');
      expect(typeof data.relatedEntityType).toBe('string');
      expect(['quote', 'policy', 'claim']).toContain(data.relatedEntityType);
      expect(typeof data.relatedEntityId).toBe('string');
      expect(typeof data.assignee).toBe('string');
      expect(data.priority).toBe('MEDIUM');
      expect(data.status).toBe('OPEN');
    });
  });
});
