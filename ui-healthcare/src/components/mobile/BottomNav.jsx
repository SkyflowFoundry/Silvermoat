/**
 * Bottom Tab Navigation for Mobile - Retail Vertical
 * Fixed bottom navigation bar with primary app sections
 */

import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  ShoppingOutlined,
  ShoppingCartOutlined,
  InboxOutlined,
  MenuOutlined,
} from '@ant-design/icons';
import { useAppContext } from '../../contexts/AppContext';
import './BottomNav.css';

const BottomNav = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { toggleMobileDrawer } = useAppContext();

  // Determine active tab based on current path
  const getActiveTab = () => {
    const path = location.pathname;
    if (path === '/dashboard' || path === '/') return 'dashboard';
    if (path.startsWith('/products')) return 'products';
    if (path.startsWith('/orders')) return 'orders';
    if (path.startsWith('/inventory')) return 'inventory';
    return '';
  };

  const activeTab = getActiveTab();

  const navItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      onClick: () => navigate('/dashboard'),
    },
    {
      key: 'products',
      icon: <ShoppingOutlined />,
      label: 'Products',
      onClick: () => navigate('/products'),
    },
    {
      key: 'orders',
      icon: <ShoppingCartOutlined />,
      label: 'Orders',
      onClick: () => navigate('/orders'),
    },
    {
      key: 'inventory',
      icon: <InboxOutlined />,
      label: 'Inventory',
      onClick: () => navigate('/inventory'),
    },
    {
      key: 'more',
      icon: <MenuOutlined />,
      label: 'More',
      onClick: toggleMobileDrawer,
    },
  ];

  return (
    <div className="bottom-nav">
      {navItems.map((item) => (
        <button
          key={item.key}
          className={`bottom-nav-item ${activeTab === item.key ? 'active' : ''}`}
          onClick={item.onClick}
          aria-label={item.label}
        >
          <span className="bottom-nav-icon">{item.icon}</span>
          <span className="bottom-nav-label">{item.label}</span>
        </button>
      ))}
    </div>
  );
};

export default BottomNav;
