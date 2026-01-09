/**
 * Silvermoat Fintech UI - Root Application Component
 */

import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider, Spin } from 'antd';
import { AppProvider } from './contexts/AppContext';
import AppLayout from './components/layout/AppLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import { fintechTheme } from './config/theme';

// Lazy load entity pages
const Landing = lazy(() => import('./pages/Landing/Landing'));
const CustomerList = lazy(() => import('./pages/Customers/CustomerList'));
const CustomerDetail = lazy(() => import('./pages/Customers/CustomerDetail'));
const AccountList = lazy(() => import('./pages/Accounts/AccountList'));
const AccountDetail = lazy(() => import('./pages/Accounts/AccountDetail'));
const TransactionList = lazy(() => import('./pages/Transactions/TransactionList'));
const TransactionDetail = lazy(() => import('./pages/Transactions/TransactionDetail'));
const LoanList = lazy(() => import('./pages/Loans/LoanList'));
const LoanDetail = lazy(() => import('./pages/Loans/LoanDetail'));
const CardList = lazy(() => import('./pages/Cards/CardList'));
const CardDetail = lazy(() => import('./pages/Cards/CardDetail'));
const CaseList = lazy(() => import('./pages/Cases/CaseList'));
const CaseDetail = lazy(() => import('./pages/Cases/CaseDetail'));
const CustomerDashboard = lazy(() => import('./pages/Customer/CustomerDashboard'));
const CustomerAccounts = lazy(() => import('./pages/Customer/CustomerAccounts'));
const CustomerTransactions = lazy(() => import('./pages/Customer/CustomerTransactions'));

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
          <ConfigProvider theme={fintechTheme}>
            <AppProvider>
              <Suspense fallback={<LoadingFallback />}>
                <Routes>
                  {/* Landing page (no layout) */}
                  <Route path="/" element={<Landing />} />

                  {/* Staff routes with layout */}
                  <Route element={<AppLayout />}>
                    <Route path="/dashboard" element={<Dashboard />} />

                    {/* Customers */}
                    <Route path="/customers" element={<CustomerList />} />
                    <Route path="/customers/new" element={<CustomerList />} />
                    <Route path="/customers/:id" element={<CustomerDetail />} />

                    {/* Accounts */}
                    <Route path="/accounts" element={<AccountList />} />
                    <Route path="/accounts/new" element={<AccountList />} />
                    <Route path="/accounts/:id" element={<AccountDetail />} />

                    {/* Transactions */}
                    <Route path="/transactions" element={<TransactionList />} />
                    <Route path="/transactions/new" element={<TransactionList />} />
                    <Route path="/transactions/:id" element={<TransactionDetail />} />

                    {/* Loans */}
                    <Route path="/loans" element={<LoanList />} />
                    <Route path="/loans/new" element={<LoanList />} />
                    <Route path="/loans/:id" element={<LoanDetail />} />

                    {/* Cards */}
                    <Route path="/cards" element={<CardList />} />
                    <Route path="/cards/new" element={<CardList />} />
                    <Route path="/cards/:id" element={<CardDetail />} />

                    {/* Cases */}
                    <Route path="/cases" element={<CaseList />} />
                    <Route path="/cases/new" element={<CaseList />} />
                    <Route path="/cases/:id" element={<CaseDetail />} />
                  </Route>

                  {/* Customer portal routes */}
                  <Route path="/customer/dashboard" element={<CustomerDashboard />} />
                  <Route path="/customer/accounts" element={<CustomerAccounts />} />
                  <Route path="/customer/transactions" element={<CustomerTransactions />} />
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
