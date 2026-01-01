/**
 * Application Route Configuration
 * Defines all routes for the Silvermoat Insurance application
 */

import { lazy } from 'react';
import { Navigate } from 'react-router-dom';

// Lazy load page components for better performance
// We'll create placeholder components initially and implement them in phases

// Landing
const Landing = lazy(() => import('../pages/Landing/Landing'));

// Dashboard
const Dashboard = lazy(() => import('../pages/Dashboard/Dashboard'));

// Quotes
const QuoteList = lazy(() => import('../pages/Quotes/QuoteList'));
const QuoteDetail = lazy(() => import('../pages/Quotes/QuoteDetail'));

// Policies
const PolicyList = lazy(() => import('../pages/Policies/PolicyList'));
const PolicyDetail = lazy(() => import('../pages/Policies/PolicyDetail'));

// Claims
const ClaimList = lazy(() => import('../pages/Claims/ClaimList'));
const ClaimDetail = lazy(() => import('../pages/Claims/ClaimDetail'));

// Payments
const PaymentList = lazy(() => import('../pages/Payments/PaymentList'));
const PaymentDetail = lazy(() => import('../pages/Payments/PaymentDetail'));

// Cases
const CaseList = lazy(() => import('../pages/Cases/CaseList'));
const CaseDetail = lazy(() => import('../pages/Cases/CaseDetail'));

// Customer Portal
const CustomerDashboard = lazy(() => import('../pages/Customer/CustomerDashboard'));
const CustomerClaimForm = lazy(() => import('../pages/Customer/CustomerClaimForm'));

/**
 * Route Configuration Array
 * Each route can have:
 * - path: URL path
 * - element: Component to render
 * - breadcrumb: Breadcrumb label
 * - children: Nested routes
 */
export const routes = [
  {
    path: '/',
    element: <Landing />,
    breadcrumb: 'Home',
  },
  {
    path: '/dashboard',
    element: <Dashboard />,
    breadcrumb: 'Dashboard',
  },
  {
    path: '/quotes',
    element: <QuoteList />,
    breadcrumb: 'Quotes',
  },
  {
    path: '/quotes/new',
    element: <QuoteList />,  // List page handles "new" state
    breadcrumb: 'New Quote',
  },
  {
    path: '/quotes/:id',
    element: <QuoteDetail />,
    breadcrumb: 'Quote Detail',
  },
  {
    path: '/policies',
    element: <PolicyList />,
    breadcrumb: 'Policies',
  },
  {
    path: '/policies/new',
    element: <PolicyList />,  // List page handles "new" state
    breadcrumb: 'New Policy',
  },
  {
    path: '/policies/:id',
    element: <PolicyDetail />,
    breadcrumb: 'Policy Detail',
  },
  {
    path: '/claims',
    element: <ClaimList />,
    breadcrumb: 'Claims',
  },
  {
    path: '/claims/new',
    element: <ClaimList />,  // List page handles "new" state
    breadcrumb: 'New Claim',
  },
  {
    path: '/claims/:id',
    element: <ClaimDetail />,
    breadcrumb: 'Claim Detail',
  },
  {
    path: '/payments',
    element: <PaymentList />,
    breadcrumb: 'Payments',
  },
  {
    path: '/payments/new',
    element: <PaymentList />,  // List page handles "new" state
    breadcrumb: 'New Payment',
  },
  {
    path: '/payments/:id',
    element: <PaymentDetail />,
    breadcrumb: 'Payment Detail',
  },
  {
    path: '/cases',
    element: <CaseList />,
    breadcrumb: 'Cases',
  },
  {
    path: '/cases/new',
    element: <CaseList />,  // List page handles "new" state
    breadcrumb: 'New Case',
  },
  {
    path: '/cases/:id',
    element: <CaseDetail />,
    breadcrumb: 'Case Detail',
  },
  {
    path: '/customer/dashboard',
    element: <CustomerDashboard />,
    breadcrumb: 'Customer Dashboard',
  },
  {
    path: '/customer/claims/new',
    element: <CustomerClaimForm />,
    breadcrumb: 'Submit Claim',
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
];

export default routes;
