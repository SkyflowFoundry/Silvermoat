/**
 * Dashboard Charts Component
 * Displays time-based trend charts for key metrics
 */

import { Row, Col, Card, Typography, Spin, Empty } from 'antd';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import dayjs from 'dayjs';
import { useQuotes } from '../../hooks/queries/useQuotes';
import { usePolicies } from '../../hooks/queries/usePolicies';
import { useClaims } from '../../hooks/queries/useClaims';
import { usePayments } from '../../hooks/queries/usePayments';
import { formatCurrencyFromCents } from '../../utils/formatters';

const { Text } = Typography;

const DashboardCharts = () => {
  // Fetch all entity data
  const { data: quotesData, isLoading: quotesLoading } = useQuotes();
  const { data: policiesData, isLoading: policiesLoading } = usePolicies();
  const { data: claimsData, isLoading: claimsLoading } = useClaims();
  const { data: paymentsData, isLoading: paymentsLoading } = usePayments();

  const isLoading = quotesLoading || policiesLoading || claimsLoading || paymentsLoading;

  // Aggregate data by month
  const quotes = quotesData?.items || [];
  const policies = policiesData?.items || [];
  const claims = claimsData?.items || [];
  const payments = paymentsData?.items || [];

  // Group by month helper - uses specific date field from data object
  const groupByMonth = (items, dateExtractor, valueExtractor) => {
    const grouped = {};
    items.forEach(item => {
      const date = dateExtractor(item);
      if (!date) return;
      const month = dayjs(date).format('YYYY-MM');
      if (!grouped[month]) {
        grouped[month] = { month, value: 0, count: 0 };
      }
      grouped[month].value += valueExtractor ? valueExtractor(item) : 0;
      grouped[month].count += 1;
    });
    return Object.values(grouped).sort((a, b) => a.month.localeCompare(b.month));
  };

  // Claims per month - by incident date
  const claimsPerMonth = groupByMonth(
    claims,
    (c) => c.data?.incidentDate || c.data?.reportedDate || (c.createdAt ? dayjs(c.createdAt * 1000).format('YYYY-MM-DD') : null)
  );

  // Policies per month - by effective date
  const policiesPerMonth = groupByMonth(
    policies,
    (p) => p.data?.effectiveDate || (p.createdAt ? dayjs(p.createdAt * 1000).format('YYYY-MM-DD') : null)
  );

  // Premium revenue per month (from policies) - by effective date
  const revenuePerMonth = groupByMonth(
    policies,
    (p) => p.data?.effectiveDate || (p.createdAt ? dayjs(p.createdAt * 1000).format('YYYY-MM-DD') : null),
    (p) => p.data?.premium_cents || 0
  );

  // Claims paid per month (only approved claims) - by incident date
  const claimsPaidPerMonth = groupByMonth(
    claims.filter(c => c.status === 'APPROVED'),
    (c) => c.data?.incidentDate || c.data?.reportedDate || (c.createdAt ? dayjs(c.createdAt * 1000).format('YYYY-MM-DD') : null),
    (c) => c.data?.paidAmount_cents || c.data?.approvedAmount_cents || 0
  );

  // Custom tooltip formatter
  const CustomTooltip = ({ active, payload, label, isCurrency }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          background: 'white',
          border: '1px solid #d9d9d9',
          padding: '8px 12px',
          borderRadius: '4px'
        }}>
          <Text strong style={{ display: 'block', marginBottom: 4 }}>
            {dayjs(label).format('MMM YYYY')}
          </Text>
          {payload.map((entry, index) => (
            <Text key={index} style={{ color: entry.color, display: 'block' }}>
              {entry.name}: {isCurrency ? formatCurrencyFromCents(entry.value) : entry.value}
            </Text>
          ))}
        </div>
      );
    }
    return null;
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading charts..." />
      </div>
    );
  }

  if (quotes.length === 0 && policies.length === 0 && claims.length === 0) {
    return (
      <Empty
        description="No data available. Create some entities to see trends."
        style={{ padding: '40px 0' }}
      />
    );
  }

  return (
    <Row gutter={[24, 24]}>
      {/* Claims per Month */}
      <Col xs={24} lg={12}>
        <Card
          title="Claims Over Time"
          bordered={false}
          size="small"
        >
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={claimsPerMonth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="month"
                tickFormatter={(month) => dayjs(month).format('MMM YY')}
                style={{ fontSize: 12 }}
              />
              <YAxis style={{ fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="count"
                name="Claims"
                stroke="#faad14"
                fill="#faad14"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </Col>

      {/* Policies per Month */}
      <Col xs={24} lg={12}>
        <Card
          title="New Policies Over Time"
          bordered={false}
          size="small"
        >
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={policiesPerMonth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="month"
                tickFormatter={(month) => dayjs(month).format('MMM YY')}
                style={{ fontSize: 12 }}
              />
              <YAxis style={{ fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="count"
                name="Policies"
                stroke="#52c41a"
                fill="#52c41a"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </Col>

      {/* Premium Revenue per Month */}
      <Col xs={24} lg={12}>
        <Card
          title="Premium Revenue Over Time"
          bordered={false}
          size="small"
        >
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={revenuePerMonth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="month"
                tickFormatter={(month) => dayjs(month).format('MMM YY')}
                style={{ fontSize: 12 }}
              />
              <YAxis
                style={{ fontSize: 12 }}
                tickFormatter={(value) => `$${(value / 100000).toFixed(0)}k`}
              />
              <Tooltip content={<CustomTooltip isCurrency />} />
              <Line
                type="monotone"
                dataKey="value"
                name="Revenue"
                stroke="#1890ff"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </Col>

      {/* Claims Paid per Month */}
      <Col xs={24} lg={12}>
        <Card
          title="Claims Paid Over Time"
          bordered={false}
          size="small"
        >
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={claimsPaidPerMonth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="month"
                tickFormatter={(month) => dayjs(month).format('MMM YY')}
                style={{ fontSize: 12 }}
              />
              <YAxis
                style={{ fontSize: 12 }}
                tickFormatter={(value) => `$${(value / 100000).toFixed(0)}k`}
              />
              <Tooltip content={<CustomTooltip isCurrency />} />
              <Line
                type="monotone"
                dataKey="value"
                name="Claims Paid"
                stroke="#cf1322"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </Col>
    </Row>
  );
};

export default DashboardCharts;
