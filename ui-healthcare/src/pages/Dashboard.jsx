/**
 * Healthcare Dashboard Page
 * Overview page with demo data seeding functionality
 */

import { useState } from 'react';
import { Typography, Card, Space, Button, Modal, Progress, message, InputNumber, Result, Row, Col, Statistic, Spin } from 'antd';
import {
  ThunderboltOutlined,
  DeleteOutlined,
  UserOutlined,
  CalendarOutlined,
  MedicineBoxOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { seedRetailData, clearRetailData } from '../utils/seedData';
import { usePatients } from '../hooks/queries/usePatients';
import { useAppointments } from '../hooks/queries/useAppointments';
import { usePrescriptions } from '../hooks/queries/usePrescriptions';
import { usePayments } from '../hooks/queries/usePayments';
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
  const { data: patientsData, isLoading: patientsLoading } = usePatients();
  const { data: appointmentsData, isLoading: appointmentsLoading } = useAppointments();
  const { data: prescriptionsData, isLoading: prescriptionsLoading } = usePrescriptions();
  const { data: paymentsData, isLoading: paymentsLoading } = usePayments();
  const { data: casesData, isLoading: casesLoading } = useCases();

  const isLoadingStats = patientsLoading || appointmentsLoading || prescriptionsLoading || paymentsLoading || casesLoading;

  const handleSeedData = async () => {
    setSeeding(true);
    setSeedProgress({ message: 'Starting...', current: 0, total: 0 });

    try {
      const results = await seedRetailData((msg, current, total) => {
        setSeedProgress({ message: msg, current, total });
      }, recordCount);

      message.success(
        `Successfully created healthcare demo data! ` +
        `(${results.patients?.length || 0} patients, ${results.appointments?.length || 0} appointments, ` +
        `${results.prescriptions?.length || 0} prescriptions, ${results.payments.length} payments, ` +
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

      message.success('Successfully cleared all healthcare data!');
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
      title: 'Patients',
      path: '/patients',
      icon: UserOutlined,
      color: '#531dab',
      background: '#f0f5ff',
      count: patientsData?.items?.length || 0,
      description: 'Manage patient records',
    },
    {
      title: 'Appointments',
      path: '/appointments',
      icon: CalendarOutlined,
      color: '#52c41a',
      background: '#f6ffed',
      count: appointmentsData?.items?.length || 0,
      description: 'Schedule and track appointments',
    },
    {
      title: 'Prescriptions',
      path: '/prescriptions',
      icon: MedicineBoxOutlined,
      color: '#1890ff',
      background: '#e6f7ff',
      count: prescriptionsData?.items?.length || 0,
      description: 'Manage prescriptions',
    },
    {
      title: 'Billing',
      path: '/billing',
      icon: DollarOutlined,
      color: '#faad14',
      background: '#fffbe6',
      count: paymentsData?.items?.length || 0,
      description: 'View billing records',
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
          Healthcare Dashboard
        </Title>
        <Paragraph type="secondary" style={{ margin: 0 }}>
          Welcome to Silvermoat Healthcare System
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
          Use the seed data tool to quickly populate the healthcare system with realistic demo data.
          This creates patients, appointments, prescriptions, payments, and support cases.
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
        title="Seed Healthcare Demo Data"
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
            This will create realistic healthcare demo data including:
          </Paragraph>
          <ul>
            <li>Patient records with demographics and medical history</li>
            <li>Appointments with various providers</li>
            <li>Prescriptions with dosage and refill information</li>
            <li>Billing records and payments</li>
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
        title="Clear All Healthcare Data"
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
            This will permanently delete all healthcare data including patients, appointments,
            prescriptions, payments, and cases.
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
