/**
 * Application Constants
 * Defines entity types, status values, and other app-wide constants
 */

// Entity Types (Domain Objects)
export const ENTITIES = {
  QUOTE: 'quote',
  POLICY: 'policy',
  CLAIM: 'claim',
  PAYMENT: 'payment',
  CASE: 'case',
};

// Entity Labels (for display)
export const ENTITY_LABELS = {
  [ENTITIES.QUOTE]: 'Quote',
  [ENTITIES.POLICY]: 'Policy',
  [ENTITIES.CLAIM]: 'Claim',
  [ENTITIES.PAYMENT]: 'Payment',
  [ENTITIES.CASE]: 'Case',
};

// Policy Statuses
export const POLICY_STATUSES = {
  ACTIVE: 'ACTIVE',
  EXPIRED: 'EXPIRED',
  CANCELLED: 'CANCELLED',
};

export const POLICY_STATUS_OPTIONS = [
  { label: 'Active', value: POLICY_STATUSES.ACTIVE, color: 'success' },
  { label: 'Expired', value: POLICY_STATUSES.EXPIRED, color: 'default' },
  { label: 'Cancelled', value: POLICY_STATUSES.CANCELLED, color: 'error' },
];

// Claim Statuses
export const CLAIM_STATUSES = {
  PENDING: 'PENDING',
  REVIEW: 'REVIEW',
  APPROVED: 'APPROVED',
  DENIED: 'DENIED',
};

export const CLAIM_STATUS_OPTIONS = [
  { label: 'Pending', value: CLAIM_STATUSES.PENDING, color: 'default' },
  { label: 'Review', value: CLAIM_STATUSES.REVIEW, color: 'processing' },
  { label: 'Approved', value: CLAIM_STATUSES.APPROVED, color: 'success' },
  { label: 'Denied', value: CLAIM_STATUSES.DENIED, color: 'error' },
];

// Payment Methods
export const PAYMENT_METHODS = {
  CARD: 'CARD',
  ACH: 'ACH',
  CHECK: 'CHECK',
};

export const PAYMENT_METHOD_OPTIONS = [
  { label: 'Credit Card', value: PAYMENT_METHODS.CARD },
  { label: 'ACH Transfer', value: PAYMENT_METHODS.ACH },
  { label: 'Check', value: PAYMENT_METHODS.CHECK },
];

// Payment Statuses
export const PAYMENT_STATUSES = {
  PENDING: 'PENDING',
  COMPLETED: 'COMPLETED',
  FAILED: 'FAILED',
};

export const PAYMENT_STATUS_OPTIONS = [
  { label: 'Pending', value: PAYMENT_STATUSES.PENDING, color: 'warning' },
  { label: 'Completed', value: PAYMENT_STATUSES.COMPLETED, color: 'success' },
  { label: 'Failed', value: PAYMENT_STATUSES.FAILED, color: 'error' },
];

// Case Priorities
export const CASE_PRIORITIES = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
};

export const CASE_PRIORITY_OPTIONS = [
  { label: 'Low', value: CASE_PRIORITIES.LOW, color: 'default' },
  { label: 'Medium', value: CASE_PRIORITIES.MEDIUM, color: 'warning' },
  { label: 'High', value: CASE_PRIORITIES.HIGH, color: 'error' },
];

// Case Statuses
export const CASE_STATUSES = {
  OPEN: 'OPEN',
  IN_PROGRESS: 'IN_PROGRESS',
  RESOLVED: 'RESOLVED',
  CLOSED: 'CLOSED',
};

export const CASE_STATUS_OPTIONS = [
  { label: 'Open', value: CASE_STATUSES.OPEN, color: 'processing' },
  { label: 'In Progress', value: CASE_STATUSES.IN_PROGRESS, color: 'warning' },
  { label: 'Resolved', value: CASE_STATUSES.RESOLVED, color: 'success' },
  { label: 'Closed', value: CASE_STATUSES.CLOSED, color: 'default' },
];

// Related Entity Types for Cases
export const RELATED_ENTITY_TYPES = [
  { label: 'Quote', value: ENTITIES.QUOTE },
  { label: 'Policy', value: ENTITIES.POLICY },
  { label: 'Claim', value: ENTITIES.CLAIM },
];

// Navigation Menu Items
export const NAV_ITEMS = [
  {
    key: 'dashboard',
    label: 'Dashboard',
    path: '/',
    icon: 'DashboardOutlined',
  },
  {
    key: 'quotes',
    label: 'Quotes',
    path: '/quotes',
    icon: 'FileTextOutlined',
  },
  {
    key: 'policies',
    label: 'Policies',
    path: '/policies',
    icon: 'SafetyCertificateOutlined',
  },
  {
    key: 'claims',
    label: 'Claims',
    path: '/claims',
    icon: 'ExclamationCircleOutlined',
  },
  {
    key: 'payments',
    label: 'Payments',
    path: '/payments',
    icon: 'DollarOutlined',
  },
  {
    key: 'cases',
    label: 'Cases',
    path: '/cases',
    icon: 'CustomerServiceOutlined',
  },
  {
    key: 'customers',
    label: 'Customers',
    path: '/customers',
    icon: 'UserOutlined',
  },
];

// Date Formats
export const DATE_FORMAT = 'MM/DD/YYYY';
export const DATETIME_FORMAT = 'MM/DD/YYYY hh:mm A';
export const TIME_FORMAT = 'hh:mm A';

// Currency Format
export const CURRENCY_SYMBOL = '$';
export const CURRENCY_DECIMAL_PLACES = 2;

// Pagination Defaults
export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

// API Configuration
export const API_TIMEOUT = 30000; // 30 seconds

// Table Size Options
export const TABLE_SIZES = {
  SMALL: 'small',
  MIDDLE: 'middle',
  LARGE: 'large',
};

export default {
  ENTITIES,
  ENTITY_LABELS,
  POLICY_STATUSES,
  POLICY_STATUS_OPTIONS,
  CLAIM_STATUSES,
  CLAIM_STATUS_OPTIONS,
  PAYMENT_METHODS,
  PAYMENT_METHOD_OPTIONS,
  PAYMENT_STATUSES,
  PAYMENT_STATUS_OPTIONS,
  CASE_PRIORITIES,
  CASE_PRIORITY_OPTIONS,
  CASE_STATUSES,
  CASE_STATUS_OPTIONS,
  RELATED_ENTITY_TYPES,
  NAV_ITEMS,
  DATE_FORMAT,
  DATETIME_FORMAT,
  TIME_FORMAT,
  CURRENCY_SYMBOL,
  CURRENCY_DECIMAL_PLACES,
  DEFAULT_PAGE_SIZE,
  PAGE_SIZE_OPTIONS,
  API_TIMEOUT,
  TABLE_SIZES,
};
