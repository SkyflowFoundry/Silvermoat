/**
 * Application Header - Healthcare Vertical
 * Top navigation bar with logo, menu, and user actions
 */

import { Layout, Menu, Button, Space, Typography } from 'antd';
import {
  MenuUnfoldOutlined,
  DashboardOutlined,
  UserOutlined,
  CalendarOutlined,
  MedicineBoxOutlined,
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
    if (path.startsWith('/patients')) return 'patients';
    if (path.startsWith('/appointments')) return 'appointments';
    if (path.startsWith('/prescriptions')) return 'prescriptions';
    if (path.startsWith('/billing')) return 'billing';
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
      key: 'patients',
      icon: <UserOutlined />,
      label: 'Patients',
      onClick: () => navigate('/patients'),
    },
    {
      key: 'appointments',
      icon: <CalendarOutlined />,
      label: 'Appointments',
      onClick: () => navigate('/appointments'),
    },
    {
      key: 'prescriptions',
      icon: <MedicineBoxOutlined />,
      label: 'Prescriptions',
      onClick: () => navigate('/prescriptions'),
    },
    {
      key: 'billing',
      icon: <DollarOutlined />,
      label: 'Billing',
      onClick: () => navigate('/billing'),
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
        background: '#13c2c2', // Healthcare theme teal
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
            alt="Silvermoat Healthcare"
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
            Silvermoat Healthcare
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
