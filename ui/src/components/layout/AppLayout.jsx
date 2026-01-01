/**
 * Main Application Layout
 * Provides the overall page structure with header, sidebar, and content area
 */

import { Layout, Drawer, Menu } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons';
import Header from './Header';
import Sidebar from './Sidebar';
import Breadcrumbs from './Breadcrumbs';
import ChatInterface from '../chat/ChatInterface';
import BottomNav from '../mobile/BottomNav';
import { useAppContext } from '../../contexts/AppContext';

const { Content } = Layout;

const AppLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isMobile, mobileDrawerOpen, closeMobileDrawer, chatDrawerOpen, closeChatDrawer } = useAppContext();

  // Determine active menu item based on current path
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/dashboard' || path === '/') return 'dashboard';
    if (path.startsWith('/quotes')) return 'quotes';
    if (path.startsWith('/policies')) return 'policies';
    if (path.startsWith('/claims')) return 'claims';
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
      key: 'quotes',
      icon: <FileTextOutlined />,
      label: 'Quotes',
      onClick: () => {
        navigate('/quotes');
        closeMobileDrawer();
      },
    },
    {
      key: 'policies',
      icon: <SafetyCertificateOutlined />,
      label: 'Policies',
      onClick: () => {
        navigate('/policies');
        closeMobileDrawer();
      },
    },
    {
      key: 'claims',
      icon: <ExclamationCircleOutlined />,
      label: 'Claims',
      onClick: () => {
        navigate('/claims');
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

      {/* Chat Drawer */}
      <Drawer
        title={null}
        placement="right"
        onClose={closeChatDrawer}
        open={chatDrawerOpen}
        width={isMobile ? '100%' : 450}
        closable={false}
        styles={{
          body: { padding: 0, height: '100%', display: 'flex', flexDirection: 'column' },
          header: { display: 'none' },
        }}
      >
        <ChatInterface />
      </Drawer>
    </Layout>
  );
};

export default AppLayout;
