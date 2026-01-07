/**
 * Silvermoat Healthcare UI - Root Application Component
 */

import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider, Spin } from 'antd';
import { AppProvider } from './contexts/AppContext';
import AppLayout from './components/layout/AppLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import { healthcareTheme } from './config/theme';

// Lazy load entity pages
const Landing = lazy(() => import('./pages/Landing/Landing'));
const PatientList = lazy(() => import('./pages/Patients/PatientList'));
const PatientDetail = lazy(() => import('./pages/Patients/PatientDetail'));
const AppointmentList = lazy(() => import('./pages/Appointments/AppointmentList'));
const AppointmentDetail = lazy(() => import('./pages/Appointments/AppointmentDetail'));
const PrescriptionList = lazy(() => import('./pages/Prescriptions/PrescriptionList'));
const PrescriptionDetail = lazy(() => import('./pages/Prescriptions/PrescriptionDetail'));
const ProviderList = lazy(() => import('./pages/Providers/ProviderList'));
const ProviderDetail = lazy(() => import('./pages/Providers/ProviderDetail'));
const CaseList = lazy(() => import('./pages/Cases/CaseList'));
const CaseDetail = lazy(() => import('./pages/Cases/CaseDetail'));
const CustomerDashboard = lazy(() => import('./pages/Customer/CustomerDashboard'));
const CustomerAppointments = lazy(() => import('./pages/Customer/CustomerAppointments'));
const CustomerRecords = lazy(() => import('./pages/Customer/CustomerRecords'));

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
          <ConfigProvider theme={healthcareTheme}>
            <AppProvider>
              <Suspense fallback={<LoadingFallback />}>
                <Routes>
                  {/* Landing page (no layout) */}
                  <Route path="/" element={<Landing />} />

                  {/* Staff routes with layout */}
                  <Route element={<AppLayout />}>
                    <Route path="/dashboard" element={<Dashboard />} />

                    {/* Patients */}
                    <Route path="/patients" element={<PatientList />} />
                    <Route path="/patients/new" element={<PatientList />} />
                    <Route path="/patients/:id" element={<PatientDetail />} />

                    {/* Appointments */}
                    <Route path="/appointments" element={<AppointmentList />} />
                    <Route path="/appointments/new" element={<AppointmentList />} />
                    <Route path="/appointments/:id" element={<AppointmentDetail />} />

                    {/* Prescriptions */}
                    <Route path="/prescriptions" element={<PrescriptionList />} />
                    <Route path="/prescriptions/new" element={<PrescriptionList />} />
                    <Route path="/prescriptions/:id" element={<PrescriptionDetail />} />

                    {/* Providers */}
                    <Route path="/providers" element={<ProviderList />} />
                    <Route path="/providers/new" element={<ProviderList />} />
                    <Route path="/providers/:id" element={<ProviderDetail />} />

                    {/* Cases */}
                    <Route path="/cases" element={<CaseList />} />
                    <Route path="/cases/new" element={<CaseList />} />
                    <Route path="/cases/:id" element={<CaseDetail />} />
                  </Route>

                  {/* Patient portal routes */}
                  <Route path="/customer/dashboard" element={<CustomerDashboard />} />
                  <Route path="/customer/appointments" element={<CustomerAppointments />} />
                  <Route path="/customer/records" element={<CustomerRecords />} />
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
