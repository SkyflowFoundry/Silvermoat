/**
 * Main Application Layout - Retail Vertical
 * Provides the overall page structure with header, sidebar, and content area
 */

import { Layout, Drawer, Menu, Button } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  ShoppingOutlined,
  ShoppingCartOutlined,
  InboxOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  MessageOutlined,
} from '@ant-design/icons';
import Header from './Header';
import Sidebar from './Sidebar';
import Breadcrumbs from './Breadcrumbs';
import BottomNav from '../mobile/BottomNav';
import { useAppContext } from '../../contexts/AppContext';

const { Content } = Layout;

const AppLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isMobile, mobileDrawerOpen, closeMobileDrawer, chatDrawerOpen, closeChatDrawer, toggleChatDrawer } = useAppContext();

  // Determine active menu item based on current path
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/dashboard' || path === '/') return 'dashboard';
    if (path.startsWith('/products')) return 'products';
    if (path.startsWith('/orders')) return 'orders';
    if (path.startsWith('/inventory')) return 'inventory';
    if (path.startsWith('/payments')) return 'payments';
    if (path.startsWith('/cases')) return 'cases';
    return 'dashboard';
  };

  // Main navigation menu items for mobile drawer
  const mobileMenuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      onClick: () => {
        navigate('/dashboard');
        closeMobileDrawer();
      },
    },
    {
      key: 'products',
      icon: <ShoppingOutlined />,
      label: 'Products',
      onClick: () => {
        navigate('/products');
        closeMobileDrawer();
      },
    },
    {
      key: 'orders',
      icon: <ShoppingCartOutlined />,
      label: 'Orders',
      onClick: () => {
        navigate('/orders');
        closeMobileDrawer();
      },
    },
    {
      key: 'inventory',
      icon: <InboxOutlined />,
      label: 'Inventory',
      onClick: () => {
        navigate('/inventory');
        closeMobileDrawer();
      },
    },
    {
      key: 'payments',
      icon: <DollarOutlined />,
      label: 'Payments',
      onClick: () => {
        navigate('/payments');
        closeMobileDrawer();
      },
    },
    {
      key: 'cases',
      icon: <CustomerServiceOutlined />,
      label: 'Cases',
      onClick: () => {
        navigate('/cases');
        closeMobileDrawer();
      },
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header />
      <Layout>
        {!isMobile && <Sidebar />}
        <Layout style={{ padding: isMobile ? '0 12px 76px 12px' : '0 24px 24px' }}>
          <Breadcrumbs style={{ margin: '16px 0' }} />
          <Content
            style={{
              padding: isMobile ? 16 : 24,
              margin: 0,
              minHeight: 280,
              background: '#ffffff',
              borderRadius: 8,
            }}
          >
            <Outlet />
          </Content>
        </Layout>
      </Layout>

      {/* Mobile Bottom Navigation */}
      {isMobile && <BottomNav />}

      {/* Floating Chat Button */}
      <Button
        type="primary"
        icon={<MessageOutlined />}
        onClick={toggleChatDrawer}
        style={{
          position: 'fixed',
          bottom: isMobile ? '90px' : '24px',
          right: '24px',
          zIndex: 1000,
          width: isMobile ? '56px' : '60px',
          height: isMobile ? '56px' : '60px',
          borderRadius: '50%',
          fontSize: isMobile ? '20px' : '24px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
        aria-label="Open Chat Assistant"
      />

      {/* Mobile Navigation Drawer */}
      <Drawer
        title="Navigation"
        placement="left"
        onClose={closeMobileDrawer}
        open={mobileDrawerOpen}
        width={280}
        styles={{
          body: { padding: 0 },
        }}
      >
        <Menu
          mode="inline"
          selectedKeys={[getSelectedKey()]}
          items={mobileMenuItems}
          style={{
            border: 'none',
            height: '100%',
          }}
        />
      </Drawer>

      {/* Chat Drawer - Placeholder until Phase 7 */}
      <Drawer
        title="Chat Assistant"
        placement="right"
        onClose={closeChatDrawer}
        open={chatDrawerOpen}
        width={isMobile ? '100%' : 450}
        styles={{
          body: { padding: 24 },
        }}
      >
        <p>Chat interface coming in Phase 7</p>
      </Drawer>
    </Layout>
  );
};

export default AppLayout;
