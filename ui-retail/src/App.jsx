/**
 * Silvermoat Retail UI - Root Application Component
 */

import { Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider, Spin, Result, Button } from 'antd';

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

// Retail theme (purple/magenta color scheme)
const retailTheme = {
  token: {
    colorPrimary: '#722ed1',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#f5222d',
    colorInfo: '#1890ff',
    fontSize: 14,
    borderRadius: 6,
  },
};

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

// Placeholder home page
const RetailHome = () => (
  <div style={{ padding: '48px', maxWidth: '1200px', margin: '0 auto' }}>
    <Result
      status="info"
      title="Silvermoat Retail"
      subTitle="Retail vertical UI coming soon. This is a placeholder for the retail platform."
      extra={[
        <Button key="insurance" href="https://insurance.silvermoat.net" type="primary">
          Go to Insurance
        </Button>,
      ]}
    />
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ConfigProvider theme={retailTheme}>
          <Suspense fallback={<LoadingFallback />}>
            <Routes>
              <Route path="*" element={<RetailHome />} />
            </Routes>
          </Suspense>
        </ConfigProvider>
      </QueryClientProvider>
    </BrowserRouter>
  );
}

export default App;
