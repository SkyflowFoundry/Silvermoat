/**
 * Application Constants - Fintech Vertical
 * Defines entity types, status values, and other app-wide constants
 */

// Entity Types (Domain Objects)
export const ENTITIES = {
  PATIENT: 'customer',
  APPOINTMENT: 'account',
  PRESCRIPTION: 'loan',
  MEDICAL_RECORD: 'transaction',
  BILLING: 'card',
  CASE: 'case',
};

// Entity Labels (for display)
export const ENTITY_LABELS = {
  [ENTITIES.PATIENT]: 'Customer',
  [ENTITIES.APPOINTMENT]: 'Account',
  [ENTITIES.PRESCRIPTION]: 'Loan',
  [ENTITIES.MEDICAL_RECORD]: 'Medical Record',
  [ENTITIES.BILLING]: 'Card',
  [ENTITIES.CASE]: 'Case',
};

// Customer Statuses
export const PATIENT_STATUSES = {
  ACTIVE: 'ACTIVE',
  INACTIVE: 'INACTIVE',
  DECEASED: 'DECEASED',
};

export const PATIENT_STATUS_OPTIONS = [
  { label: 'Active', value: PATIENT_STATUSES.ACTIVE, color: 'success' },
  { label: 'Inactive', value: PATIENT_STATUSES.INACTIVE, color: 'default' },
  { label: 'Deceased', value: PATIENT_STATUSES.DECEASED, color: 'error' },
];

// Account Statuses
export const APPOINTMENT_STATUSES = {
  SCHEDULED: 'SCHEDULED',
  CONFIRMED: 'CONFIRMED',
  IN_PROGRESS: 'IN_PROGRESS',
  COMPLETED: 'COMPLETED',
  CANCELLED: 'CANCELLED',
  NO_SHOW: 'NO_SHOW',
};

export const APPOINTMENT_STATUS_OPTIONS = [
  { label: 'Scheduled', value: APPOINTMENT_STATUSES.SCHEDULED, color: 'default' },
  { label: 'Confirmed', value: APPOINTMENT_STATUSES.CONFIRMED, color: 'processing' },
  { label: 'In Progress', value: APPOINTMENT_STATUSES.IN_PROGRESS, color: 'warning' },
  { label: 'Completed', value: APPOINTMENT_STATUSES.COMPLETED, color: 'success' },
  { label: 'Cancelled', value: APPOINTMENT_STATUSES.CANCELLED, color: 'error' },
  { label: 'No Show', value: APPOINTMENT_STATUSES.NO_SHOW, color: 'error' },
];

// Loan Statuses
export const PRESCRIPTION_STATUSES = {
  ACTIVE: 'ACTIVE',
  FILLED: 'FILLED',
  EXPIRED: 'EXPIRED',
  CANCELLED: 'CANCELLED',
};

export const PRESCRIPTION_STATUS_OPTIONS = [
  { label: 'Active', value: PRESCRIPTION_STATUSES.ACTIVE, color: 'success' },
  { label: 'Filled', value: PRESCRIPTION_STATUSES.FILLED, color: 'processing' },
  { label: 'Expired', value: PRESCRIPTION_STATUSES.EXPIRED, color: 'default' },
  { label: 'Cancelled', value: PRESCRIPTION_STATUSES.CANCELLED, color: 'error' },
];

// Payment Methods
export const PAYMENT_METHODS = {
  CREDIT_CARD: 'CREDIT_CARD',
  ACH: 'ACH',
  CHECK: 'CHECK',
};

export const PAYMENT_METHOD_OPTIONS = [
  { label: 'Credit Card', value: PAYMENT_METHODS.CREDIT_CARD },
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
  URGENT: 'URGENT',
};

export const CASE_PRIORITY_OPTIONS = [
  { label: 'Low', value: CASE_PRIORITIES.LOW, color: 'default' },
  { label: 'Medium', value: CASE_PRIORITIES.MEDIUM, color: 'processing' },
  { label: 'High', value: CASE_PRIORITIES.HIGH, color: 'warning' },
  { label: 'Urgent', value: CASE_PRIORITIES.URGENT, color: 'error' },
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

// Navigation Menu Items
export const NAV_ITEMS = [
  {
    key: 'dashboard',
    label: 'Dashboard',
    path: '/dashboard',
    icon: 'DashboardOutlined',
  },
  {
    key: 'customers',
    label: 'Customers',
    path: '/customers',
    icon: 'UserOutlined',
  },
  {
    key: 'accounts',
    label: 'Accounts',
    path: '/accounts',
    icon: 'CalendarOutlined',
  },
  {
    key: 'loans',
    label: 'Loans',
    path: '/loans',
    icon: 'BankOutlined',
  },
  {
    key: 'card',
    label: 'Card',
    path: '/card',
    icon: 'DollarOutlined',
  },
  {
    key: 'cases',
    label: 'Cases',
    path: '/cases',
    icon: 'CustomerServiceOutlined',
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
  PATIENT_STATUSES,
  PATIENT_STATUS_OPTIONS,
  APPOINTMENT_STATUSES,
  APPOINTMENT_STATUS_OPTIONS,
  PRESCRIPTION_STATUSES,
  PRESCRIPTION_STATUS_OPTIONS,
  PAYMENT_METHODS,
  PAYMENT_METHOD_OPTIONS,
  PAYMENT_STATUSES,
  PAYMENT_STATUS_OPTIONS,
  CASE_PRIORITIES,
  CASE_PRIORITY_OPTIONS,
  CASE_STATUSES,
  CASE_STATUS_OPTIONS,
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
