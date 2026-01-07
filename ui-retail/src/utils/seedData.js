/**
 * Seed Demo Data Utility for Retail Vertical
 * Creates realistic retail demo data (products, orders, inventory, etc.)
 */

import { getApiBaseUrl } from '../services/api';

// Helper data for realistic retail demo generation
const FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Jennifer'];
const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
const PRODUCT_CATEGORIES = ['Electronics', 'Apparel', 'Home & Garden', 'Sports & Outdoors', 'Books', 'Toys & Games', 'Health & Beauty', 'Automotive'];
const PRODUCT_ADJECTIVES = ['Premium', 'Deluxe', 'Classic', 'Modern', 'Eco-Friendly', 'Smart', 'Pro', 'Essential'];
const PRODUCT_NOUNS = ['Widget', 'Gadget', 'Tool', 'Device', 'Kit', 'Set', 'System', 'Solution'];
const ORDER_STATUSES = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'];
const INVENTORY_STATUSES = ['IN_STOCK', 'LOW_STOCK', 'OUT_OF_STOCK'];
const PAYMENT_STATUSES = ['PENDING', 'COMPLETED', 'FAILED', 'REFUNDED'];
const PAYMENT_METHODS = ['CREDIT_CARD', 'DEBIT_CARD', 'PAYPAL', 'GIFT_CARD'];
const WAREHOUSES = ['NYC-01', 'LA-02', 'CHI-03', 'DAL-04', 'ATL-05'];

// Helper functions
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomName = () => `${randomItem(FIRST_NAMES)} ${randomItem(LAST_NAMES)}`;
const randomEmail = (name) => {
  const domains = ['gmail.com', 'yahoo.com', 'outlook.com'];
  const safeName = name.toLowerCase().replace(' ', '.');
  return `${safeName}${randomNumber(1, 999)}@${randomItem(domains)}`;
};
const randomPhone = () => `${randomNumber(200, 999)}-${randomNumber(200, 999)}-${randomNumber(1000, 9999)}`;
const randomAddress = () => {
  const streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Park Blvd'];
  const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'];
  return `${randomNumber(100, 9999)} ${randomItem(streets)}, ${randomItem(cities)}`;
};
const randomSKU = () => `SKU-${randomNumber(10000, 99999)}`;
const randomDateWithinDays = (days) => {
  const now = new Date();
  const past = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  const randomTime = past.getTime() + Math.random() * (now.getTime() - past.getTime());
  return new Date(randomTime).toISOString().split('T')[0];
};

// API helper functions
const apiCall = async (endpoint, method = 'GET', body = null) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}${endpoint}`;
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }
  return response.json();
};

const createProduct = (data) => apiCall('/product', 'POST', data);
const createOrder = (data) => apiCall('/order', 'POST', data);
const createInventory = (data) => apiCall('/inventory', 'POST', data);
const createPayment = (data) => apiCall('/payment', 'POST', data);
const createCase = (data) => apiCall('/case', 'POST', data);
const deleteAllEntities = (entity) => apiCall(`/${entity}`, 'DELETE');

/**
 * Seeds retail demo data
 * @param {Function} onProgress - Callback for progress updates (message, current, total)
 * @param {number} count - Number of records to create (default: 50)
 * @returns {Promise<Object>} Object containing created entities
 */
export const seedRetailData = async (onProgress, count = 50) => {
  const results = {
    products: [],
    orders: [],
    inventory: [],
    payments: [],
    cases: [],
  };

  let step = 0;
  const totalSteps = count * 2.5; // Approximate steps

  try {
    // Step 1: Create Products
    onProgress?.('Creating demo products...', step, totalSteps);
    for (let i = 0; i < count; i++) {
      const category = randomItem(PRODUCT_CATEGORIES);
      const productName = `${randomItem(PRODUCT_ADJECTIVES)} ${randomItem(PRODUCT_NOUNS)}`;
      const price = randomNumber(10, 500);

      const productData = {
        sku: randomSKU(),
        name: productName,
        description: `High-quality ${productName.toLowerCase()} for ${category.toLowerCase()}`,
        price,
        category,
        stockQuantity: randomNumber(0, 500),
        manufacturer: randomItem(['BrandCo', 'TechCorp', 'QualityGoods', 'PremiumMfg']),
        weight: randomNumber(1, 50),
      };

      const product = await createProduct(productData);
      results.products.push(product);
      step++;
      onProgress?.('Creating demo products...', step, totalSteps);
    }

    // Step 2: Create Orders (with 30 orders for variety)
    onProgress?.('Creating demo orders...', step, totalSteps);
    const orderCount = Math.min(30, count);
    for (let i = 0; i < orderCount; i++) {
      const customerName = randomName();
      const numItems = randomNumber(1, 5);
      const orderItems = [];
      let totalAmount = 0;

      // Select random products for this order
      for (let j = 0; j < numItems; j++) {
        const product = randomItem(results.products);
        const quantity = randomNumber(1, 3);
        const itemTotal = product?.item?.data?.price * quantity || 0;
        totalAmount += itemTotal;

        orderItems.push({
          productId: product?.item?.id,
          productName: product?.item?.data?.name,
          quantity,
          price: product?.item?.data?.price,
          total: itemTotal,
        });
      }

      const orderData = {
        orderNumber: `ORD-${randomNumber(100000, 999999)}`,
        customerName,
        customerEmail: randomEmail(customerName),
        customerPhone: randomPhone(),
        shippingAddress: randomAddress(),
        items: orderItems,
        totalAmount,
        orderDate: randomDateWithinDays(90),
        status: randomItem(ORDER_STATUSES),
      };

      const order = await createOrder(orderData);
      results.orders.push(order);
      step++;
      onProgress?.('Creating demo orders...', step, totalSteps);
    }

    // Step 3: Create Inventory records for products
    onProgress?.('Creating inventory records...', step, totalSteps);
    for (let i = 0; i < Math.min(count, results.products.length); i++) {
      const product = results.products[i];
      const quantity = product?.item?.data?.stockQuantity || randomNumber(0, 500);

      const inventoryData = {
        productId: product?.item?.id,
        productName: product?.item?.data?.name,
        sku: product?.item?.data?.sku,
        location: randomItem(WAREHOUSES),
        quantity,
        reorderPoint: randomNumber(10, 50),
        lastRestocked: randomDateWithinDays(30),
      };

      const inventory = await createInventory(inventoryData);
      results.inventory.push(inventory);
      step++;
      onProgress?.('Creating inventory records...', step, totalSteps);
    }

    // Step 4: Create Payments for orders
    onProgress?.('Creating demo payments...', step, totalSteps);
    for (let i = 0; i < results.orders.length; i++) {
      const order = results.orders[i];

      const paymentData = {
        orderId: order?.item?.id,
        orderNumber: order?.item?.data?.orderNumber,
        amount: order?.item?.data?.totalAmount,
        paymentMethod: randomItem(PAYMENT_METHODS),
        transactionId: `TXN-${randomNumber(1000000, 9999999)}`,
        paymentDate: order?.item?.data?.orderDate,
      };

      const payment = await createPayment(paymentData);
      results.payments.push(payment);
      step++;
      onProgress?.('Creating demo payments...', step, totalSteps);
    }

    // Step 5: Create Support Cases
    onProgress?.('Creating support cases...', step, totalSteps);
    const caseTopics = ['ORDER_INQUIRY', 'PRODUCT_DEFECT', 'SHIPPING_DELAY', 'REFUND_REQUEST', 'PRODUCT_QUESTION'];
    const casePriorities = ['LOW', 'MEDIUM', 'HIGH'];
    const caseCount = Math.min(15, count);

    for (let i = 0; i < caseCount; i++) {
      const customerName = randomName();
      const topic = randomItem(caseTopics);

      const caseData = {
        title: `${topic.replace('_', ' ')} - ${customerName}`,
        description: `Customer ${customerName} has reported an issue regarding ${topic.toLowerCase().replace('_', ' ')}.`,
        customerName,
        customerEmail: randomEmail(customerName),
        topic,
        priority: randomItem(casePriorities),
        assignee: randomItem(['Support Team', 'Sales Team', 'Fulfillment']),
        createdDate: randomDateWithinDays(60),
      };

      const supportCase = await createCase(caseData);
      results.cases.push(supportCase);
      step++;
      onProgress?.('Creating support cases...', step, totalSteps);
    }

    onProgress?.('Seeding complete!', totalSteps, totalSteps);
    return results;

  } catch (error) {
    console.error('Seeding error:', error);
    throw new Error(`Failed to seed data: ${error.message}`);
  }
};

/**
 * Clears all retail demo data
 * @param {Function} onProgress - Callback for progress updates
 */
export const clearRetailData = async (onProgress) => {
  const entities = ['product', 'order', 'inventory', 'payment', 'case', 'customer'];
  let step = 0;

  for (const entity of entities) {
    onProgress?.(`Clearing ${entity}s...`, step, entities.length);
    try {
      await deleteAllEntities(entity);
    } catch (error) {
      console.warn(`Failed to clear ${entity}s:`, error);
    }
    step++;
  }

  onProgress?.('Data cleared!', entities.length, entities.length);
};

export default {
  seedRetailData,
  clearRetailData,
};
