/**
 * Form Sample Data Generators - Fintech Vertical
 * Provides sample data for form auto-fill functionality
 */

// Helper data for realistic sample generation
const FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Maria'];
const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
const CARD_TYPES = ['CREDIT', 'DEBIT', 'PREPAID'];
const CARD_STATUSES = ['ACTIVE', 'SUSPENDED', 'CLOSED', 'EXPIRED'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const ASSIGNEES = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Miller'];

// Helper functions
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomPrice = (min, max) => (Math.random() * (max - min) + min).toFixed(2);

/**
 * Generate sample data for Card form
 * @returns {Object} Sample card data
 */
export const generateCardSampleData = () => {
  const firstName = randomItem(FIRST_NAMES);
  const lastName = randomItem(LAST_NAMES);
  const customerName = `${firstName} ${lastName}`;
  const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}@example.com`;

  // Generate realistic card number (starting with 4 for Visa)
  const cardNumber = `4${randomNumber(100, 999)}${randomNumber(1000, 9999)}${randomNumber(1000, 9999)}${randomNumber(1000, 9999)}`;

  // Generate expiry date (future date)
  const month = String(randomNumber(1, 12)).padStart(2, '0');
  const year = String(randomNumber(25, 30));
  const expiryDate = `${month}/${year}`;

  return {
    customerName,
    customerEmail: email,
    cardNumber,
    cardType: randomItem(CARD_TYPES),
    creditLimit: randomNumber(1000, 50000),
    expiryDate,
    status: 'ACTIVE',
  };
};

/**
 * Generate sample data for Case form
 * @returns {Object} Sample case data
 */
export const generateCaseSampleData = () => {
  const issueTypes = ['Account Access', 'Card Issue', 'Transaction Dispute', 'Loan Question', 'General Inquiry'];
  const issue = randomItem(issueTypes);

  return {
    subject: `${issue} - Customer Support Request`,
    description: `Customer reported ${issue.toLowerCase()}. This is a sample case for testing purposes. Need to investigate and respond promptly.`,
    priority: randomItem(PRIORITIES),
    assignedTo: randomItem(ASSIGNEES),
    customerEmail: `${randomItem(FIRST_NAMES).toLowerCase()}.${randomItem(LAST_NAMES).toLowerCase()}@example.com`,
  };
};
