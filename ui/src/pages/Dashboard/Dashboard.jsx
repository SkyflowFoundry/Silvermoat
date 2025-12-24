/**
 * Dashboard Page
 * Overview page with statistics and recent activity
 */

import { useState } from 'react';
import { Typography, Card, Space, Button, Modal, Progress, message } from 'antd';
import {
  PlusOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import DashboardStats from './DashboardStats';
import RecentActivity from './RecentActivity';
import { seedDemoData, getSeedDataSummary } from '../../utils/seedData';

const { Title, Paragraph, Text } = Typography;

const Dashboard = () => {
  const navigate = useNavigate();
  const [seedModalVisible, setSeedModalVisible] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedProgress, setSeedProgress] = useState({ message: '', current: 0, total: 0 });

  const handleSeedData = async () => {
    setSeeding(true);
    setSeedProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await seedDemoData((msg, current, total) => {
        setSeedProgress({ message: msg, current, total });
      });

      const summary = getSeedDataSummary(results);
      message.success(
        `Successfully created ${summary.total} demo records! ` +
        `(${summary.quotes} quotes, ${summary.policies} policies, ` +
        `${summary.claims} claims, ${summary.payments} payments, ${summary.cases} cases)`
      );

      setSeedModalVisible(false);

      // Refresh the page after a short delay to show new data
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } catch (error) {
      message.error(`Failed to seed demo data: ${error.message}`);
    } finally {
      setSeeding(false);
    }
  };

  const quickActions = [
    {
      label: 'New Quote',
      icon: <FileTextOutlined />,
      path: '/quotes/new',
      type: 'primary',
    },
    {
      label: 'New Policy',
      icon: <SafetyCertificateOutlined />,
      path: '/policies/new',
      type: 'default',
    },
    {
      label: 'New Claim',
      icon: <ExclamationCircleOutlined />,
      path: '/claims/new',
      type: 'default',
    },
    {
      label: 'New Payment',
      icon: <DollarOutlined />,
      path: '/payments/new',
      type: 'default',
    },
    {
      label: 'New Case',
      icon: <CustomerServiceOutlined />,
      path: '/cases/new',
      type: 'default',
    },
  ];

  return (
    <div>
      {/* Header */}
      <Space
        direction="vertical"
        size="small"
        style={{ marginBottom: 24, width: '100%' }}
      >
        <Title level={2} style={{ margin: 0 }}>
          Dashboard
        </Title>
        <Paragraph type="secondary" style={{ margin: 0 }}>
          Welcome to Silvermoat Insurance Management System
        </Paragraph>
      </Space>

      {/* Quick Actions */}
      <Card
        title="Quick Actions"
        size="small"
        style={{ marginBottom: 24 }}
        bordered={false}
      >
        <Space wrap>
          {quickActions.map((action) => (
            <Button
              key={action.path}
              type={action.type}
              icon={action.icon}
              onClick={() => navigate(action.path)}
            >
              {action.label}
            </Button>
          ))}
          <Button
            type="dashed"
            icon={<ThunderboltOutlined />}
            onClick={() => setSeedModalVisible(true)}
            style={{ borderColor: '#722ed1', color: '#722ed1' }}
          >
            Seed Demo Data
          </Button>
        </Space>
      </Card>

      {/* Statistics */}
      <Card
        title="Entity Statistics"
        size="small"
        style={{ marginBottom: 24 }}
        bordered={false}
      >
        <DashboardStats />
      </Card>

      {/* Recent Activity */}
      <Card
        title="Recent Activity"
        size="small"
        bordered={false}
        extra={
          <Space>
            <Button
              size="small"
              onClick={() => navigate('/quotes')}
              icon={<FileTextOutlined />}
            >
              View Quotes
            </Button>
            <Button
              size="small"
              onClick={() => navigate('/policies')}
              icon={<SafetyCertificateOutlined />}
            >
              View Policies
            </Button>
            <Button
              size="small"
              onClick={() => navigate('/claims')}
              icon={<ExclamationCircleOutlined />}
            >
              View Claims
            </Button>
          </Space>
        }
      >
        <RecentActivity />
      </Card>

      {/* Seed Data Modal */}
      <Modal
        title="Seed Demo Data"
        open={seedModalVisible}
        onCancel={() => !seeding && setSeedModalVisible(false)}
        footer={[
          <Button
            key="cancel"
            onClick={() => setSeedModalVisible(false)}
            disabled={seeding}
          >
            Cancel
          </Button>,
          <Button
            key="seed"
            type="primary"
            onClick={handleSeedData}
            loading={seeding}
            icon={<ThunderboltOutlined />}
          >
            {seeding ? 'Seeding...' : 'Start Seeding'}
          </Button>,
        ]}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Text>
            This will create realistic demo data across all entity types:
          </Text>
          <ul style={{ paddingLeft: 20 }}>
            <li>5 Quotes with customer information</li>
            <li>5 Policies linked to quotes</li>
            <li>5 Claims linked to policies</li>
            <li>5 Payments linked to policies</li>
            <li>5 Cases linked to various entities</li>
          </ul>
          <Text type="secondary">
            All records will have realistic data with proper relationships between entities.
          </Text>

          {seeding && (
            <Space direction="vertical" style={{ width: '100%' }}>
              <Progress
                percent={Math.round((seedProgress.current / seedProgress.total) * 100)}
                status="active"
              />
              <Text type="secondary">{seedProgress.message}</Text>
            </Space>
          )}
        </Space>
      </Modal>
    </div>
  );
};

export default Dashboard;
