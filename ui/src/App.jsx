/**
 * Root Application Component
 * Sets up all providers and routing for the Silvermoat Insurance application
 */

import { Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider, Spin } from 'antd';
import { AppProvider } from './contexts/AppContext';
import AppLayout from './components/layout/AppLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import theme from './config/theme';
import routes from './config/routes';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Get API base URL from environment or use relative path
export const getApiBase = () => {
  // In production, this will be set via build-time replacement or window config
  // For now, try to get from window or use relative path
  if (window.API_BASE_URL) {
    return window.API_BASE_URL;
  }
  // Try to infer from current location (for S3 website hosting)
  // This is a fallback - ideally set via deploy script
  return import.meta.env.VITE_API_BASE_URL || '';
};

// Loading fallback component
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
          <ConfigProvider theme={theme}>
            <AppProvider>
              <Suspense fallback={<LoadingFallback />}>
                <Routes>
                  {/* Landing + Customer portal routes (no layout) */}
                  {routes
                    .filter(route => route.path.startsWith('/customer') || route.path === '/')
                    .map((route) => (
                      <Route
                        key={route.path}
                        path={route.path}
                        element={route.element}
                      />
                    ))}

                  {/* Employee portal routes (with AppLayout) */}
                  <Route element={<AppLayout />}>
                    {routes
                      .filter(route => !route.path.startsWith('/customer') && route.path !== '/')
                      .map((route) => (
                        <Route
                          key={route.path}
                          path={route.path}
                          element={route.element}
                        />
                      ))}
                  </Route>
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
