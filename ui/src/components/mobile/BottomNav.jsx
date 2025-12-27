/**
 * Bottom Tab Navigation for Mobile
 * Fixed bottom navigation bar with primary app sections
 */

import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
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
    if (path === '/') return 'dashboard';
    if (path.startsWith('/quotes')) return 'quotes';
    if (path.startsWith('/policies')) return 'policies';
    if (path.startsWith('/claims')) return 'claims';
    return '';
  };

  const activeTab = getActiveTab();

  const navItems = [
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
