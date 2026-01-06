/**
 * Retail Dashboard Page
 * Overview page with demo data seeding functionality
 */

import { useState } from 'react';
import { Typography, Card, Space, Button, Modal, Progress, message, InputNumber, Result } from 'antd';
import {
  ThunderboltOutlined,
  DeleteOutlined,
  ShoppingOutlined,
  ShopOutlined,
  InboxOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons';
import { seedRetailData, clearRetailData } from '../utils/seedData';

const { Title, Paragraph, Text } = Typography;

const Dashboard = () => {
  const [seedModalVisible, setSeedModalVisible] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedProgress, setSeedProgress] = useState({ message: '', current: 0, total: 0 });
  const [recordCount, setRecordCount] = useState(50);
  const [clearModalVisible, setClearModalVisible] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [clearProgress, setClearProgress] = useState({ message: '', current: 0, total: 0 });

  const handleSeedData = async () => {
    setSeeding(true);
    setSeedProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await seedRetailData((msg, current, total) => {
        setSeedProgress({ message: msg, current, total });
      }, recordCount);

      message.success(
        `Successfully created retail demo data! ` +
        `(${results.products.length} products, ${results.orders.length} orders, ` +
        `${results.inventory.length} inventory items, ${results.payments.length} payments, ` +
        `${results.cases.length} cases)`
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
      await clearRetailData((msg, current, total) => {
        setClearProgress({ message: msg, current, total });
      });

      message.success('Successfully cleared all retail data!');
      setClearModalVisible(false);

      // Refresh the page after a short delay
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } catch (error) {
      message.error(`Failed to clear data: ${error.message}`);
    } finally {
      setClearing(false);
    }
  };

  const quickStats = [
    {
      label: 'Products',
      icon: <ShoppingOutlined style={{ fontSize: 32, color: '#722ed1' }} />,
      description: 'Product catalog',
    },
    {
      label: 'Orders',
      icon: <ShopOutlined style={{ fontSize: 32, color: '#52c41a' }} />,
      description: 'Customer orders',
    },
    {
      label: 'Inventory',
      icon: <InboxOutlined style={{ fontSize: 32, color: '#1890ff' }} />,
      description: 'Stock levels',
    },
    {
      label: 'Payments',
      icon: <DollarOutlined style={{ fontSize: 32, color: '#faad14' }} />,
      description: 'Payment records',
    },
    {
      label: 'Cases',
      icon: <CustomerServiceOutlined style={{ fontSize: 32, color: '#f5222d' }} />,
      description: 'Support cases',
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <Space direction="vertical" size="small" style={{ marginBottom: 24, width: '100%' }}>
        <Title level={2} style={{ margin: 0 }}>
          Retail Dashboard
        </Title>
        <Paragraph type="secondary" style={{ margin: 0 }}>
          Welcome to Silvermoat Retail Management System
        </Paragraph>
      </Space>

      {/* Demo Data Tools */}
      <Card
        title={
          <Space>
            <ThunderboltOutlined />
            <span>Demo Data Tools</span>
          </Space>
        }
        extra={
          <Space>
            <Button
              type="primary"
              icon={<ThunderboltOutlined />}
              onClick={() => setSeedModalVisible(true)}
            >
              Seed Demo Data
            </Button>
            <Button
              danger
              icon={<DeleteOutlined />}
              onClick={() => setClearModalVisible(true)}
            >
              Clear All Data
            </Button>
          </Space>
        }
        style={{ marginBottom: 24 }}
      >
        <Paragraph>
          Use the seed data tool to quickly populate the retail system with realistic demo data.
          This creates products, orders, inventory records, payments, and support cases.
        </Paragraph>
      </Card>

      {/* Retail Entity Overview */}
      <Card title="Retail Entities">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {quickStats.map((stat) => (
            <Card
              key={stat.label}
              size="small"
              style={{ background: '#fafafa' }}
            >
              <Space>
                {stat.icon}
                <div>
                  <Text strong>{stat.label}</Text>
                  <br />
                  <Text type="secondary">{stat.description}</Text>
                </div>
              </Space>
            </Card>
          ))}
        </Space>
      </Card>

      {/* Seed Data Modal */}
      <Modal
        title="Seed Retail Demo Data"
        open={seedModalVisible}
        onCancel={() => !seeding && setSeedModalVisible(false)}
        footer={[
          <Button key="cancel" onClick={() => setSeedModalVisible(false)} disabled={seeding}>
            Cancel
          </Button>,
          <Button
            key="seed"
            type="primary"
            loading={seeding}
            onClick={handleSeedData}
            icon={<ThunderboltOutlined />}
          >
            Seed Data
          </Button>,
        ]}
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Paragraph>
            This will create realistic retail demo data including:
          </Paragraph>
          <ul>
            <li>Products with SKUs, prices, and categories</li>
            <li>Customer orders with multiple items</li>
            <li>Inventory records across warehouses</li>
            <li>Payment records for orders</li>
            <li>Support cases</li>
          </ul>

          <div>
            <Text strong>Number of records to create:</Text>
            <InputNumber
              min={10}
              max={1000}
              value={recordCount}
              onChange={(value) => setRecordCount(value)}
              style={{ marginLeft: 12, width: 100 }}
              disabled={seeding}
            />
          </div>

          {seeding && (
            <div>
              <Text type="secondary">{seedProgress.message}</Text>
              <Progress
                percent={
                  seedProgress.total > 0
                    ? Math.round((seedProgress.current / seedProgress.total) * 100)
                    : 0
                }
                status="active"
              />
            </div>
          )}
        </Space>
      </Modal>

      {/* Clear Data Modal */}
      <Modal
        title="Clear All Retail Data"
        open={clearModalVisible}
        onCancel={() => !clearing && setClearModalVisible(false)}
        footer={[
          <Button key="cancel" onClick={() => setClearModalVisible(false)} disabled={clearing}>
            Cancel
          </Button>,
          <Button
            key="clear"
            danger
            type="primary"
            loading={clearing}
            onClick={handleClearData}
            icon={<DeleteOutlined />}
          >
            Clear All Data
          </Button>,
        ]}
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Paragraph type="danger" strong>
            Warning: This action cannot be undone!
          </Paragraph>
          <Paragraph>
            This will permanently delete all retail data including products, orders, inventory,
            payments, and cases.
          </Paragraph>

          {clearing && (
            <div>
              <Text type="secondary">{clearProgress.message}</Text>
              <Progress
                percent={
                  clearProgress.total > 0
                    ? Math.round((clearProgress.current / clearProgress.total) * 100)
                    : 0
                }
                status="active"
              />
            </div>
          )}
        </Space>
      </Modal>
    </div>
  );
};

export default Dashboard;
