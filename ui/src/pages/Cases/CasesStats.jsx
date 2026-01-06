/**
 * Cases Statistics Component
 * Mini-dashboard showing case-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { FolderOpenOutlined, CheckCircleOutlined, ClockCircleOutlined, WarningOutlined, TeamOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { useCases } from '../../hooks/queries/useCases';

const { Text } = Typography;

const CasesStats = () => {
  const { data: casesData, isLoading } = useCases();
  const cases = casesData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalCases = cases.length;
  const openCases = cases.filter(c => c.data?.status === 'OPEN').length;
  const inProgressCases = cases.filter(c => c.data?.status === 'IN_PROGRESS').length;
  const resolvedCases = cases.filter(c => c.data?.status === 'RESOLVED').length;
  const closedCases = cases.filter(c => c.data?.status === 'CLOSED').length;

  const activeCases = openCases + inProgressCases;
  const resolutionRate = totalCases > 0 ? ((resolvedCases + closedCases) / totalCases) * 100 : 0;

  // Priority distribution
  const urgentCases = cases.filter(c => c.data?.priority === 'URGENT').length;
  const highCases = cases.filter(c => c.data?.priority === 'HIGH').length;
  const mediumCases = cases.filter(c => c.data?.priority === 'MEDIUM').length;
  const lowCases = cases.filter(c => c.data?.priority === 'LOW').length;

  // Overdue cases (dueDate in past and not resolved/closed)
  const now = dayjs();
  const overdueCases = cases.filter(c => {
    const status = c.data?.status;
    const dueDate = c.data?.dueDate;
    if (!dueDate || status === 'RESOLVED' || status === 'CLOSED') return false;
    return dayjs(dueDate).isBefore(now);
  }).length;

  // Average resolution time (for resolved/closed cases)
  const resolvedWithDates = cases.filter(c => {
    const status = c.data?.status;
    const resolvedDate = c.data?.resolvedDate;
    const createdAt = c.createdAt;
    return (status === 'RESOLVED' || status === 'CLOSED') && resolvedDate && createdAt;
  });

  let avgResolutionDays = 0;
  if (resolvedWithDates.length > 0) {
    const totalDays = resolvedWithDates.reduce((sum, c) => {
      const resolved = dayjs(c.data.resolvedDate);
      const created = dayjs(c.createdAt * 1000);
      return sum + resolved.diff(created, 'day');
    }, 0);
    avgResolutionDays = totalDays / resolvedWithDates.length;
  }

  // Topic distribution
  const topics = {};
  cases.forEach(c => {
    const topic = c.data?.topic || 'UNKNOWN';
    topics[topic] = (topics[topic] || 0) + 1;
  });
  const topTopic = Object.entries(topics).sort((a, b) => b[1] - a[1])[0];

  // Department distribution
  const departments = {};
  cases.forEach(c => {
    const dept = c.data?.department || 'UNKNOWN';
    departments[dept] = (departments[dept] || 0) + 1;
  });
  const topDepartment = Object.entries(departments).sort((a, b) => b[1] - a[1])[0];

  // Assignee workload
  const assignees = {};
  cases.filter(c => c.data?.status === 'OPEN' || c.data?.status === 'IN_PROGRESS').forEach(c => {
    const assignee = c.data?.assignee || 'UNASSIGNED';
    assignees[assignee] = (assignees[assignee] || 0) + 1;
  });
  const busiestAssignee = Object.entries(assignees).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Cases</Text>}
              value={totalCases}
              prefix={<FolderOpenOutlined style={{ color: '#0052A3' }} />}
              valueStyle={{ color: '#0052A3' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#faad14' }}>●</span> {openCases} Open
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#0052A3' }}>●</span> {inProgressCases} In Progress
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Active Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Active Cases</Text>}
              value={activeCases}
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Open + In Progress
            </Text>
          </Card>
        </Col>

        {/* Resolved Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Resolved</Text>}
              value={resolvedCases + closedCases}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {resolutionRate.toFixed(1)}% resolution rate
            </Text>
          </Card>
        </Col>

        {/* Overdue Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Overdue</Text>}
              value={overdueCases}
              prefix={<WarningOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Past due date
            </Text>
          </Card>
        </Col>

        {/* Urgent Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Urgent Priority</Text>}
              value={urgentCases}
              prefix={<WarningOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#ff7a45' }}>●</span> {highCases} High
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#faad14' }}>●</span> {mediumCases} Medium
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Average Resolution Time */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6fffb' }}>
            <Statistic
              title={<Text strong>Avg Resolution Time</Text>}
              value={avgResolutionDays.toFixed(1)}
              suffix="days"
              valueStyle={{ color: '#13c2c2', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {resolvedWithDates.length} resolved cases
            </Text>
          </Card>
        </Col>

        {/* Top Topic */}
        {topTopic && (
          <Col xs={24} sm={12} lg={6}>
            <Card size="small" bordered={false} style={{ background: '#f9f0ff' }}>
              <Statistic
                title={<Text strong>Top Topic</Text>}
                value={topTopic[0].replace(/_/g, ' ')}
                valueStyle={{ fontSize: 16, color: '#722ed1' }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                {topTopic[1]} cases ({totalCases > 0 ? ((topTopic[1] / totalCases) * 100).toFixed(1) : 0}%)
              </Text>
            </Card>
          </Col>
        )}

        {/* Top Department */}
        {topDepartment && (
          <Col xs={24} sm={12} lg={6}>
            <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
              <Statistic
                title={<Text strong>Busiest Department</Text>}
                value={topDepartment[0].replace(/_/g, ' ')}
                prefix={<TeamOutlined style={{ color: '#0052A3' }} />}
                valueStyle={{ fontSize: 16, color: '#0052A3' }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                {topDepartment[1]} cases ({totalCases > 0 ? ((topDepartment[1] / totalCases) * 100).toFixed(1) : 0}%)
              </Text>
            </Card>
          </Col>
        )}

        {/* Busiest Assignee */}
        {busiestAssignee && (
          <Col xs={24} sm={12} lg={6}>
            <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
              <Statistic
                title={<Text strong>Busiest Assignee</Text>}
                value={busiestAssignee[0]}
                valueStyle={{ fontSize: 16, color: '#fa8c16' }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                {busiestAssignee[1]} active cases
              </Text>
            </Card>
          </Col>
        )}
      </Row>
    </div>
  );
};

export default CasesStats;
