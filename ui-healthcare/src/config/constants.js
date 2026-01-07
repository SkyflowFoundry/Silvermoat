/**
 * Application Constants - Retail Vertical
 * Defines entity types, status values, and other app-wide constants
 */

// Entity Types (Domain Objects)
export const ENTITIES = {
  PRODUCT: 'product',
  ORDER: 'order',
  INVENTORY: 'inventory',
  PAYMENT: 'payment',
  CASE: 'case',
};

// Entity Labels (for display)
export const ENTITY_LABELS = {
  [ENTITIES.PRODUCT]: 'Product',
  [ENTITIES.ORDER]: 'Order',
  [ENTITIES.INVENTORY]: 'Inventory',
  [ENTITIES.PAYMENT]: 'Payment',
  [ENTITIES.CASE]: 'Case',
};

// Product Statuses
export const PRODUCT_STATUSES = {
  ACTIVE: 'ACTIVE',
  DISCONTINUED: 'DISCONTINUED',
  OUT_OF_STOCK: 'OUT_OF_STOCK',
};

export const PRODUCT_STATUS_OPTIONS = [
  { label: 'Active', value: PRODUCT_STATUSES.ACTIVE, color: 'success' },
  { label: 'Discontinued', value: PRODUCT_STATUSES.DISCONTINUED, color: 'default' },
  { label: 'Out of Stock', value: PRODUCT_STATUSES.OUT_OF_STOCK, color: 'warning' },
];

// Order Statuses
export const ORDER_STATUSES = {
  PENDING: 'PENDING',
  PROCESSING: 'PROCESSING',
  SHIPPED: 'SHIPPED',
  DELIVERED: 'DELIVERED',
  CANCELLED: 'CANCELLED',
};

export const ORDER_STATUS_OPTIONS = [
  { label: 'Pending', value: ORDER_STATUSES.PENDING, color: 'default' },
  { label: 'Processing', value: ORDER_STATUSES.PROCESSING, color: 'processing' },
  { label: 'Shipped', value: ORDER_STATUSES.SHIPPED, color: 'warning' },
  { label: 'Delivered', value: ORDER_STATUSES.DELIVERED, color: 'success' },
  { label: 'Cancelled', value: ORDER_STATUSES.CANCELLED, color: 'error' },
];

// Inventory Statuses
export const INVENTORY_STATUSES = {
  IN_STOCK: 'IN_STOCK',
  LOW_STOCK: 'LOW_STOCK',
  OUT_OF_STOCK: 'OUT_OF_STOCK',
};

export const INVENTORY_STATUS_OPTIONS = [
  { label: 'In Stock', value: INVENTORY_STATUSES.IN_STOCK, color: 'success' },
  { label: 'Low Stock', value: INVENTORY_STATUSES.LOW_STOCK, color: 'warning' },
  { label: 'Out of Stock', value: INVENTORY_STATUSES.OUT_OF_STOCK, color: 'error' },
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
    key: 'products',
    label: 'Products',
    path: '/products',
    icon: 'ShoppingOutlined',
  },
  {
    key: 'orders',
    label: 'Orders',
    path: '/orders',
    icon: 'ShoppingCartOutlined',
  },
  {
    key: 'inventory',
    label: 'Inventory',
    path: '/inventory',
    icon: 'InboxOutlined',
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
  PRODUCT_STATUSES,
  PRODUCT_STATUS_OPTIONS,
  ORDER_STATUSES,
  ORDER_STATUS_OPTIONS,
  INVENTORY_STATUSES,
  INVENTORY_STATUS_OPTIONS,
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
