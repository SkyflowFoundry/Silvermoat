/**
 * Form Sample Data Generators - Retail Vertical
 * Provides sample data for form auto-fill functionality
 */

// Helper data for realistic sample generation
const PRODUCT_NAMES = [
  'Wireless Headphones',
  'Smart Watch',
  'Laptop Stand',
  'USB-C Cable',
  'Mechanical Keyboard',
  'Gaming Mouse',
  'Webcam HD',
  'Phone Case',
  'Portable Charger',
  'Bluetooth Speaker',
];

const PRODUCT_PREFIXES = ['Premium', 'Pro', 'Ultra', 'Max', 'Elite', 'Basic', 'Standard', 'Advanced'];
const CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors', 'Books', 'Toys & Games', 'Other'];
const WAREHOUSES = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Distribution Center 1', 'Regional Hub'];
const PAYMENT_METHODS = ['CREDIT_CARD', 'ACH', 'CHECK'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const ASSIGNEES = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Miller'];

// Helper functions
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomPrice = (min, max) => (Math.random() * (max - min) + min).toFixed(2);

/**
 * Generate sample data for Product form
 * @returns {Object} Sample product data matching ProductForm fields
 */
export const generateProductSampleData = () => {
  const baseName = randomItem(PRODUCT_NAMES);
  const prefix = Math.random() > 0.5 ? randomItem(PRODUCT_PREFIXES) : '';
  const name = prefix ? `${prefix} ${baseName}` : baseName;
  const sku = `${name.substring(0, 3).toUpperCase()}-${randomNumber(1000, 9999)}`;

  return {
    name,
    sku,
    price: parseFloat(randomPrice(9.99, 999.99)),
    category: randomItem(CATEGORIES),
    description: `High-quality ${name.toLowerCase()} perfect for everyday use. Features modern design and excellent performance. Sample product for testing purposes.`,
    stockLevel: randomNumber(0, 500),
  };
};

/**
 * Generate sample data for Inventory form
 * @returns {Object} Sample inventory data
 */
export const generateInventorySampleData = () => {
  return {
    productId: 'sample-product-id', // Will be replaced by actual product selection
    warehouse: randomItem(WAREHOUSES),
    quantity: randomNumber(0, 1000),
    reorderLevel: randomNumber(10, 100),
    lastRestocked: new Date().toISOString().split('T')[0],
  };
};

/**
 * Generate sample data for Order form
 * @returns {Object} Sample order data
 */
export const generateOrderSampleData = () => {
  const firstName = randomItem(['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily']);
  const lastName = randomItem(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia']);
  const customerName = `${firstName} ${lastName}`;
  const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}@example.com`;

  return {
    customerEmail: email,
    customerName,
    customerPhone: `(${randomNumber(200, 999)}) ${randomNumber(200, 999)}-${randomNumber(1000, 9999)}`,
    shippingAddress: `${randomNumber(100, 9999)} Main St, Apt ${randomNumber(1, 99)}, Springfield, ${randomItem(['FL', 'GA', 'NC', 'NY', 'CA'])} ${randomNumber(10000, 99999)}`,
    items: [
      // Items will be added dynamically based on available products
    ],
  };
};

/**
 * Generate sample data for Payment form
 * @returns {Object} Sample payment data
 */
export const generatePaymentSampleData = () => {
  return {
    orderId: 'sample-order-id', // Will be replaced by actual order selection
    amount: parseFloat(randomPrice(10, 1000)),
    method: randomItem(PAYMENT_METHODS),
    transactionId: `TXN-${randomNumber(100000, 999999)}`,
    notes: 'Sample payment for testing purposes',
  };
};

/**
 * Generate sample data for Case form
 * @returns {Object} Sample case data
 */
export const generateCaseSampleData = () => {
  const issueTypes = ['Product Defect', 'Shipping Issue', 'Billing Question', 'Returns', 'General Inquiry'];
  const issue = randomItem(issueTypes);

  return {
    subject: `${issue} - Customer Support Request`,
    description: `Customer reported ${issue.toLowerCase()}. This is a sample case for testing purposes. Need to investigate and respond promptly.`,
    priority: randomItem(PRIORITIES),
    status: 'OPEN',
    assignee: randomItem(ASSIGNEES),
    customerEmail: `customer${randomNumber(1, 999)}@example.com`,
  };
};

export default {
  generateProductSampleData,
  generateInventorySampleData,
  generateOrderSampleData,
  generatePaymentSampleData,
  generateCaseSampleData,
};
