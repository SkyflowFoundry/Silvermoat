/**
 * Application Header - Fintech Vertical
 * Top navigation bar with logo, menu, and user actions
 */

import { Layout, Menu, Button, Space, Typography } from 'antd';
import {
  MenuUnfoldOutlined,
  DashboardOutlined,
  UserOutlined,
  CalendarOutlined,
  BankOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../../contexts/AppContext';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isMobile, toggleMobileDrawer } = useAppContext();

  // Determine active menu item based on current path
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/dashboard' || path === '/') return 'dashboard';
    if (path.startsWith('/customers')) return 'customers';
    if (path.startsWith('/accounts')) return 'accounts';
    if (path.startsWith('/loans')) return 'loans';
    if (path.startsWith('/card')) return 'card';
    if (path.startsWith('/cases')) return 'cases';
    return 'dashboard';
  };

  // Main navigation menu items
  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      onClick: () => navigate('/dashboard'),
    },
    {
      key: 'customers',
      icon: <UserOutlined />,
      label: 'Customers',
      onClick: () => navigate('/customers'),
    },
    {
      key: 'accounts',
      icon: <CalendarOutlined />,
      label: 'Accounts',
      onClick: () => navigate('/accounts'),
    },
    {
      key: 'loans',
      icon: <BankOutlined />,
      label: 'Loans',
      onClick: () => navigate('/loans'),
    },
    {
      key: 'card',
      icon: <DollarOutlined />,
      label: 'Card',
      onClick: () => navigate('/card'),
    },
    {
      key: 'cases',
      icon: <CustomerServiceOutlined />,
      label: 'Cases',
      onClick: () => navigate('/cases'),
    },
  ];

  return (
    <AntHeader
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: isMobile ? '0 12px' : '0 24px',
        background: '#13c2c2', // Fintech theme teal
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
      }}
    >
      <Space align="center" size={isMobile ? 'small' : 'large'}>
        {isMobile && (
          <Button
            type="text"
            icon={<MenuUnfoldOutlined />}
            onClick={toggleMobileDrawer}
            style={{
              fontSize: '18px',
              width: 40,
              height: 40,
              color: '#ffffff',
            }}
          />
        )}
        <div
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          <img
            src="/silvermoat-logo.png"
            alt="Silvermoat Fintech"
            style={{
              height: isMobile ? 28 : 36,
              width: 'auto',
              objectFit: 'contain',
            }}
          />
          <Text
            strong
            style={{
              color: '#ffffff',
              fontSize: isMobile ? '16px' : '20px',
              fontWeight: 600,
              letterSpacing: '-0.5px',
            }}
          >
            Silvermoat Fintech
          </Text>
        </div>
      </Space>

      {!isMobile && (
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[getSelectedKey()]}
          items={menuItems}
          style={{
            flex: 1,
            marginLeft: 48,
            background: 'transparent',
            borderBottom: 'none',
            color: '#ffffff',
          }}
        />
      )}

      {/* Chat moved to floating button in bottom-right */}
    </AntHeader>
  );
};

export default Header;
