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

                    {/* Entity routes will be added in subsequent phases */}
                    {/* Phase 4: /orders, /orders/:id */}
                    {/* Phase 5: /payments, /payments/:id */}
                    {/* Phase 6: /cases, /cases/:id */}
                  </Route>

                  {/* Customer portal routes (Phase 8) */}
                  {/* <Route path="/customer/*" element={<CustomerPortal />} /> */}

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
