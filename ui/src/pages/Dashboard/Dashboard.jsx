/**
 * Dashboard Page
 * Overview page with statistics and recent activity
 */

import { useState } from 'react';
import { Typography, Card, Space, Button, Modal, Progress, message, InputNumber } from 'antd';
import {
  PlusOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  ThunderboltOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import DashboardStats from './DashboardStats';
import DashboardCharts from './DashboardCharts';
import RecentActivity from './RecentActivity';
import { seedDemoData, getSeedDataSummary, clearAllData } from '../../utils/seedData';

const { Title, Paragraph, Text } = Typography;

const Dashboard = () => {
  const navigate = useNavigate();
  const [seedModalVisible, setSeedModalVisible] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedProgress, setSeedProgress] = useState({ message: '', current: 0, total: 0 });
  const [recordCount, setRecordCount] = useState(25);
  const [clearModalVisible, setClearModalVisible] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [clearProgress, setClearProgress] = useState({ message: '', current: 0, total: 0 });

  const handleSeedData = async () => {
    setSeeding(true);
    setSeedProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await seedDemoData((msg, current, total) => {
        setSeedProgress({ message: msg, current, total });
      }, recordCount);

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

  const handleClearData = async () => {
    setClearing(true);
    setClearProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await clearAllData((msg, current, total) => {
        setClearProgress({ message: msg, current, total });
      });

      const total = Object.values(results).reduce((sum, count) => sum + count, 0);
      message.success(
        `Successfully cleared ${total} records! ` +
        `(${results.quotes} quotes, ${results.policies} policies, ` +
        `${results.claims} claims, ${results.payments} payments, ${results.cases} cases)`
      );

      setClearModalVisible(false);

      // Refresh the page after a short delay to show cleared data
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } catch (error) {
      message.error(`Failed to clear data: ${error.message}`);
    } finally {
      setClearing(false);
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
          <Button
            type="dashed"
            icon={<DeleteOutlined />}
            onClick={() => setClearModalVisible(true)}
            danger
          >
            Clear All Data
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

      {/* Trend Charts */}
      <Card
        title="Trends & Analytics"
        size="small"
        style={{ marginBottom: 24 }}
        bordered={false}
      >
        <DashboardCharts />
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
          <div>
            <Text strong>Number of records per entity type:</Text>
            <div style={{ marginTop: 8 }}>
              <InputNumber
                min={1}
                max={1000}
                value={recordCount}
                onChange={(value) => setRecordCount(value || 1)}
                disabled={seeding}
                style={{ width: 120 }}
              />
              <Text type="secondary" style={{ marginLeft: 12 }}>
                (1-1000 max)
              </Text>
            </div>
          </div>

          <Text>
            This will create realistic demo data across all entity types:
          </Text>
          <ul style={{ paddingLeft: 20 }}>
            <li>{recordCount} Quotes with full customer details</li>
            <li>{recordCount} Policies linked to quotes with premium data</li>
            <li>{recordCount} Claims linked to policies with estimated/approved amounts</li>
            <li>{recordCount} Payments linked to policies with transaction details</li>
            <li>{recordCount} Cases linked to various entities</li>
          </ul>
          <Text type="secondary">
            All records will have realistic data with proper relationships and 10-year date spread for trend charts.
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

      {/* Clear All Data Modal */}
      <Modal
        title="Clear All Data"
        open={clearModalVisible}
        onCancel={() => !clearing && setClearModalVisible(false)}
        footer={[
          <Button
            key="cancel"
            onClick={() => setClearModalVisible(false)}
            disabled={clearing}
          >
            Cancel
          </Button>,
          <Button
            key="clear"
            type="primary"
            danger
            onClick={handleClearData}
            loading={clearing}
            icon={<DeleteOutlined />}
          >
            {clearing ? 'Clearing...' : 'Clear All Data'}
          </Button>,
        ]}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Text strong style={{ color: '#ff4d4f' }}>
            Warning: This action cannot be undone!
          </Text>
          <Text>
            This will permanently delete all data from all entity types:
          </Text>
          <ul style={{ paddingLeft: 20 }}>
            <li>All Quotes</li>
            <li>All Policies</li>
            <li>All Claims</li>
            <li>All Payments</li>
            <li>All Cases</li>
          </ul>
          <Text type="secondary">
            The data will be permanently removed from the database. You can seed new demo data afterwards.
          </Text>

          {clearing && (
            <Space direction="vertical" style={{ width: '100%' }}>
              <Progress
                percent={Math.round((clearProgress.current / clearProgress.total) * 100)}
                status="active"
              />
              <Text type="secondary">{clearProgress.message}</Text>
            </Space>
          )}
        </Space>
      </Modal>
    </div>
  );
};

export default Dashboard;
