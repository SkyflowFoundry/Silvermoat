/**
 * Silvermoat Retail UI - Root Application Component
 */

import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider, Spin } from 'antd';
import { AppProvider } from './contexts/AppContext';
import AppLayout from './components/layout/AppLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import { retailTheme } from './config/theme';

// Lazy load entity pages
const ProductList = lazy(() => import('./pages/Products/ProductList'));
const ProductDetail = lazy(() => import('./pages/Products/ProductDetail'));
const InventoryList = lazy(() => import('./pages/Inventory/InventoryList'));
const InventoryDetail = lazy(() => import('./pages/Inventory/InventoryDetail'));
const OrderList = lazy(() => import('./pages/Orders/OrderList'));
const OrderDetail = lazy(() => import('./pages/Orders/OrderDetail'));
const PaymentList = lazy(() => import('./pages/Payments/PaymentList'));
const PaymentDetail = lazy(() => import('./pages/Payments/PaymentDetail'));
const CaseList = lazy(() => import('./pages/Cases/CaseList'));
const CaseDetail = lazy(() => import('./pages/Cases/CaseDetail'));
const CustomerDashboard = lazy(() => import('./pages/Customer/CustomerDashboard'));
const CustomerOrderTracking = lazy(() => import('./pages/Customer/CustomerOrderTracking'));
const CustomerProductBrowser = lazy(() => import('./pages/Customer/CustomerProductBrowser'));

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

// Loading fallback
const LoadingFallback = () => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: '#f5f5f5',
    }}
  >
    <Spin size="large" tip="Loading..." />
  </div>
);

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <ConfigProvider theme={retailTheme}>
            <AppProvider>
              <Suspense fallback={<LoadingFallback />}>
                <Routes>
                  {/* Employee routes with layout */}
                  <Route element={<AppLayout />}>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />

                    {/* Phase 2: Products */}
                    <Route path="/products" element={<ProductList />} />
                    <Route path="/products/new" element={<ProductList />} />
                    <Route path="/products/:id" element={<ProductDetail />} />

                    {/* Phase 3: Inventory */}
                    <Route path="/inventory" element={<InventoryList />} />
                    <Route path="/inventory/new" element={<InventoryList />} />
                    <Route path="/inventory/:id" element={<InventoryDetail />} />

                    {/* Phase 4: Orders */}
                    <Route path="/orders" element={<OrderList />} />
                    <Route path="/orders/new" element={<OrderList />} />
                    <Route path="/orders/:id" element={<OrderDetail />} />

                    {/* Phase 5: Payments */}
                    <Route path="/payments" element={<PaymentList />} />
                    <Route path="/payments/new" element={<PaymentList />} />
                    <Route path="/payments/:id" element={<PaymentDetail />} />

                    {/* Phase 6: Cases */}
                    <Route path="/cases" element={<CaseList />} />
                    <Route path="/cases/new" element={<CaseList />} />
                    <Route path="/cases/:id" element={<CaseDetail />} />
                  </Route>

                  {/* Customer portal routes */}
                  <Route path="/customer/dashboard" element={<CustomerDashboard />} />
                  <Route path="/customer/orders" element={<CustomerOrderTracking />} />
                  <Route path="/customer/products" element={<CustomerProductBrowser />} />
                  <Route path="/customer" element={<Navigate to="/customer/dashboard" replace />} />

                  {/* Catch-all redirect */}
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Suspense>
            </AppProvider>
          </ConfigProvider>
        </QueryClientProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
