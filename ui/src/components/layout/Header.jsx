/**
 * Application Header
 * Top navigation bar with logo, menu, and user actions
 */

import { Layout, Menu, Button, Space, Typography } from 'antd';
import {
  MenuUnfoldOutlined,
  DashboardOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  MessageOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../../contexts/AppContext';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isMobile, toggleMobileDrawer, toggleChatDrawer } = useAppContext();

  // Determine active menu item based on current path
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/') return 'dashboard';
    if (path.startsWith('/quotes')) return 'quotes';
    if (path.startsWith('/policies')) return 'policies';
    if (path.startsWith('/claims')) return 'claims';
    if (path.startsWith('/payments')) return 'payments';
    if (path.startsWith('/cases')) return 'cases';
    return 'dashboard';
  };

  // Main navigation menu items
  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      onClick: () => navigate('/'),
    },
    {
      key: 'quotes',
      icon: <FileTextOutlined />,
      label: 'Quotes',
      onClick: () => navigate('/quotes'),
    },
    {
      key: 'policies',
      icon: <SafetyCertificateOutlined />,
      label: 'Policies',
      onClick: () => navigate('/policies'),
    },
    {
      key: 'claims',
      icon: <ExclamationCircleOutlined />,
      label: 'Claims',
      onClick: () => navigate('/claims'),
    },
    {
      key: 'payments',
      icon: <DollarOutlined />,
      label: 'Payments',
      onClick: () => navigate('/payments'),
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
        background: '#002855',
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
            alt="Silvermoat Insurance"
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
            Silvermoat Insurance
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

      <Space size="middle">
        <Button
          type="text"
          icon={<MessageOutlined />}
          onClick={toggleChatDrawer}
          style={{
            fontSize: '18px',
            width: isMobile ? 40 : 48,
            height: isMobile ? 40 : 48,
            color: '#ffffff',
          }}
          title="Open Chat Assistant"
        />
      </Space>
    </AntHeader>
  );
};

export default Header;
