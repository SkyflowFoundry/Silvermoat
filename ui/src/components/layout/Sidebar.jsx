/**
 * Application Sidebar
 * Secondary navigation and context-specific actions
 */

import { Layout, Menu } from 'antd';
import {
  PlusOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Sider } = Layout;

const Sidebar = ({ collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();

  // Determine which entity we're currently viewing
  const getCurrentEntity = () => {
    const path = location.pathname;
    if (path.startsWith('/quotes')) return 'quotes';
    if (path.startsWith('/policies')) return 'policies';
    if (path.startsWith('/claims')) return 'claims';
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
    const singularEntity = entityLabel.slice(0, -1); // Remove trailing 's'

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
      collapsible
      collapsed={collapsed}
      trigger={null}
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
