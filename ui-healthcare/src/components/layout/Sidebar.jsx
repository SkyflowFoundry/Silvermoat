/**
 * Application Sidebar - Retail Vertical
 * Secondary navigation and context-specific actions
 */

import { Layout, Menu } from 'antd';
import {
  PlusOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Sider } = Layout;

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Determine which entity we're currently viewing
  const getCurrentEntity = () => {
    const path = location.pathname;
    if (path.startsWith('/products')) return 'products';
    if (path.startsWith('/orders')) return 'orders';
    if (path.startsWith('/inventory')) return 'inventory';
    if (path.startsWith('/payments')) return 'payments';
    if (path.startsWith('/cases')) return 'cases';
    return null;
  };

  const currentEntity = getCurrentEntity();

  // Generate sidebar menu based on current entity
  const getSidebarMenuItems = () => {
    if (!currentEntity) {
      return [];
    }

    const entityLabel = currentEntity.charAt(0).toUpperCase() + currentEntity.slice(1);
    // Handle special cases for singular forms
    let singularEntity = entityLabel;
    if (currentEntity === 'inventory') {
      singularEntity = 'Inventory Item';
    } else {
      singularEntity = entityLabel.slice(0, -1); // Remove trailing 's'
    }

    return [
      {
        key: `${currentEntity}-list`,
        icon: <UnorderedListOutlined />,
        label: `All ${entityLabel}`,
        onClick: () => navigate(`/${currentEntity}`),
      },
      {
        key: `${currentEntity}-new`,
        icon: <PlusOutlined />,
        label: `New ${singularEntity}`,
        onClick: () => navigate(`/${currentEntity}/new`),
      },
    ];
  };

  const menuItems = getSidebarMenuItems();

  // Don't render sidebar on dashboard
  if (!currentEntity) {
    return null;
  }

  return (
    <Sider
      width={220}
      style={{
        background: '#ffffff',
        borderRight: '1px solid #f0f0f0',
      }}
    >
      <Menu
        mode="inline"
        selectedKeys={[location.pathname.includes('/new') ? `${currentEntity}-new` : `${currentEntity}-list`]}
        items={menuItems}
        style={{
          height: '100%',
          borderRight: 0,
          paddingTop: 16,
        }}
      />
    </Sider>
  );
};

export default Sidebar;
