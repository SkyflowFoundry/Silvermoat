/**
 * Breadcrumb Navigation
 * Shows the current page hierarchy and navigation path
 */

import { Breadcrumb } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { useLocation, Link } from 'react-router-dom';

const Breadcrumbs = ({ style }) => {
  const location = useLocation();
  const pathSnippets = location.pathname.split('/').filter((i) => i);

  // Generate breadcrumb items from path
  const breadcrumbItems = [
    {
      title: (
        <Link to="/">
          <HomeOutlined />
        </Link>
      ),
    },
  ];

  // Map path segments to readable labels
  const getLabel = (segment, index) => {
    // If it's a UUID-like ID, show "Detail"
    if (segment.match(/^[a-f0-9-]{36}$/i)) {
      return 'Detail';
    }

    // Capitalize first letter
    const label = segment.charAt(0).toUpperCase() + segment.slice(1);

    // Check if it's "new"
    if (segment === 'new') {
      return `New ${pathSnippets[index - 1].charAt(0).toUpperCase() + pathSnippets[index - 1].slice(1, -1)}`;
    }

    return label;
  };

  pathSnippets.forEach((snippet, index) => {
    const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
    const isLast = index === pathSnippets.length - 1;
    const label = getLabel(snippet, index);

    // Skip adding UUID segments as separate breadcrumb items
    if (snippet.match(/^[a-f0-9-]{36}$/i)) {
      breadcrumbItems.push({
        title: isLast ? label : <Link to={url}>{label}</Link>,
      });
    } else if (snippet !== 'new') {
      // Add regular segments
      breadcrumbItems.push({
        title: isLast ? label : <Link to={url}>{label}</Link>,
      });
    }
  });

  // Don't show breadcrumbs on home page
  if (pathSnippets.length === 0) {
    return null;
  }

  return <Breadcrumb items={breadcrumbItems} style={style} />;
};

export default Breadcrumbs;
