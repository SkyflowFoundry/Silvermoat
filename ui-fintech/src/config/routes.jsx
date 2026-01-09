/**
 * Application Routes Configuration - Fintech Vertical
 * Lazy-loaded routes for optimal performance
 */

import { lazy } from 'react';

// Lazy load page components
const Dashboard = lazy(() => import('../pages/Dashboard'));

// Entity routes will be added in subsequent phases
// Phase 2: Products routes
// Phase 3: Inventory routes
// Phase 4: Orders routes
// Phase 5: Payments routes
// Phase 6: Cases routes
// Phase 8: Customer portal routes

export const routes = {
  // Main app routes
  dashboard: {
    path: '/dashboard',
    element: Dashboard,
  },

  // Entity routes to be added:
  // products: { path: '/products', element: ProductList },
  // productDetail: { path: '/products/:id', element: ProductDetail },
  // ... etc
};

export default routes;
