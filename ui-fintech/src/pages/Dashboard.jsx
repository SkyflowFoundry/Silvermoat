/**
 * Fintech Dashboard Page
 * Overview page with demo data seeding functionality
 */

import { useState } from 'react';
import { Typography, Card, Space, Button, Modal, Progress, message, InputNumber, Result, Row, Col, Statistic, Spin } from 'antd';
import {
  ThunderboltOutlined,
  DeleteOutlined,
  UserOutlined,
  CalendarOutlined,
  BankOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { seedRetailData, clearRetailData } from '../utils/seedData';
import { useCustomers } from '../hooks/queries/useCustomers';
import { useAccounts } from '../hooks/queries/useAccounts';
import { useLoans } from '../hooks/queries/useLoans';
import { useCards } from '../hooks/queries/useCards';
import { useCases } from '../hooks/queries/useCases';

const { Title, Paragraph, Text } = Typography;

const Dashboard = () => {
  const navigate = useNavigate();
  const [seedModalVisible, setSeedModalVisible] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedProgress, setSeedProgress] = useState({ message: '', current: 0, total: 0 });
  const [recordCount, setRecordCount] = useState(50);
  const [clearModalVisible, setClearModalVisible] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [clearProgress, setClearProgress] = useState({ message: '', current: 0, total: 0 });

  // Fetch entity data for stats
  const { data: customersData, isLoading: customersLoading } = useCustomers();
  const { data: accountsData, isLoading: accountsLoading } = useAccounts();
  const { data: loansData, isLoading: loansLoading } = useLoans();
  const { data: cardsData, isLoading: cardsLoading } = useCards();
  const { data: casesData, isLoading: casesLoading } = useCases();

  const isLoadingStats = customersLoading || accountsLoading || loansLoading || cardsLoading || casesLoading;

  const handleSeedData = async () => {
    setSeeding(true);
    setSeedProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await seedRetailData((msg, current, total) => {
        setSeedProgress({ message: msg, current, total });
      }, recordCount);

      message.success(
        `Successfully created fintech demo data! ` +
        `(${results.customers?.length || 0} customers, ${results.accounts?.length || 0} accounts, ` +
        `${results.loans?.length || 0} loans, ${results.payments.length} payments, ` +
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

      message.success('Successfully cleared all fintech data!');
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

  const entityCards = [
    {
      title: 'Customers',
      path: '/customers',
      icon: UserOutlined,
      color: '#531dab',
      background: '#f0f5ff',
      count: customersData?.items?.length || 0,
      description: 'Manage customer records',
    },
    {
      title: 'Accounts',
      path: '/accounts',
      icon: CalendarOutlined,
      color: '#13c2c2',
      background: '#f6ffed',
      count: accountsData?.items?.length || 0,
      description: 'Schedule and track accounts',
    },
    {
      title: 'Loans',
      path: '/loans',
      icon: BankOutlined,
      color: '#1890ff',
      background: '#e6f7ff',
      count: loansData?.items?.length || 0,
      description: 'Manage loans',
    },
    {
      title: 'Cards',
      path: '/cards',
      icon: DollarOutlined,
      color: '#faad14',
      background: '#fffbe6',
      count: cardsData?.items?.length || 0,
      description: 'View card records',
    },
    {
      title: 'Cases',
      path: '/cases',
      icon: CustomerServiceOutlined,
      color: '#ff4d4f',
      background: '#fff1f0',
      count: casesData?.items?.length || 0,
      description: 'Manage support cases',
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <Space direction="vertical" size="small" style={{ marginBottom: 24, width: '100%' }}>
        <Title level={2} style={{ margin: 0 }}>
          Fintech Dashboard
        </Title>
        <Paragraph type="secondary" style={{ margin: 0 }}>
          Welcome to Silvermoat Fintech System
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
          Use the seed data tool to quickly populate the fintech system with realistic demo data.
          This creates customers, accounts, loans, payments, and support cases.
        </Paragraph>
      </Card>

      {/* Entity Quick Navigation */}
      <Card title="Quick Navigation">
        {isLoadingStats ? (
          <div style={{ textAlign: 'center', padding: '48px' }}>
            <Spin size="large" tip="Loading stats..." />
          </div>
        ) : (
          <Row gutter={[16, 16]}>
            {entityCards.map((entity) => {
              const IconComponent = entity.icon;
              return (
                <Col xs={24} sm={12} md={8} lg={8} xl={8} key={entity.title}>
                  <Card
                    hoverable
                    style={{ background: entity.background, cursor: 'pointer' }}
                    onClick={() => navigate(entity.path)}
                  >
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                        <IconComponent style={{ fontSize: 32, color: entity.color }} />
                        <ArrowRightOutlined style={{ color: entity.color }} />
                      </Space>
                      <Statistic
                        title={entity.title}
                        value={entity.count}
                        valueStyle={{ color: entity.color, fontSize: 24 }}
                      />
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {entity.description}
                      </Text>
                    </Space>
                  </Card>
                </Col>
              );
            })}
          </Row>
        )}
      </Card>

      {/* Seed Data Modal */}
      <Modal
        title="Seed Fintech Demo Data"
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
            This will create realistic fintech demo data including:
          </Paragraph>
          <ul>
            <li>Customer records with demographics and medical history</li>
            <li>Accounts with various providers</li>
            <li>Loans with dosage and refill information</li>
            <li>Card records and payments</li>
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
        title="Clear All Fintech Data"
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
            This will permanently delete all fintech data including customers, accounts,
            loans, payments, and cases.
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
