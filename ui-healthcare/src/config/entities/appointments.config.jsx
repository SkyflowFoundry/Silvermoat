/**
 * Appointment Entity Configuration
 * Defines table columns, form fields, and validation for appointments
 */

import { Input, Select, DatePicker, Tag } from 'antd';
import { CalendarOutlined, UserOutlined, MailOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

const { TextArea } = Input;

// Status color mapping
const STATUS_COLORS = {
  SCHEDULED: 'blue',
  CONFIRMED: 'cyan',
  COMPLETED: 'green',
  CANCELLED: 'red',
  NO_SHOW: 'orange',
};

// Table configuration
export const appointmentTableConfig = {
  columns: [
    {
      title: 'Patient Name',
      dataIndex: ['data', 'patientName'],
      key: 'patientName',
      width: 180,
      ellipsis: true,
      render: (name) => name || '-',
    },
    {
      title: 'Patient Email',
      dataIndex: ['data', 'patientEmail'],
      key: 'patientEmail',
      width: 200,
      ellipsis: true,
      render: (email) => email || '-',
    },
    {
      title: 'Date & Time',
      dataIndex: ['data', 'date'],
      key: 'date',
      width: 180,
      render: (date) => date || '-',
    },
    {
      title: 'Provider',
      dataIndex: ['data', 'provider'],
      key: 'provider',
      width: 150,
      ellipsis: true,
      render: (provider) => provider || '-',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'type'],
      key: 'type',
      width: 120,
      render: (type) => type || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status || 'SCHEDULED'}
        </Tag>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 150,
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ],
  rowKey: 'id',
  scroll: { x: 1200 },
};

// Mobile fields for responsive table
export const appointmentMobileFields = [
  { label: 'Patient', key: ['data', 'patientName'] },
  { label: 'Date', key: ['data', 'date'] },
  { label: 'Provider', key: ['data', 'provider'] },
  { label: 'Status', key: 'status' },
];

// Form fields configuration
export const appointmentFormFields = [
  {
    name: 'patientName',
    label: 'Patient Name',
    required: true,
    message: 'Please enter patient name',
    component: <Input prefix={<UserOutlined />} placeholder="John Doe" />,
  },
  {
    name: 'patientEmail',
    label: 'Patient Email',
    required: true,
    message: 'Please enter patient email',
    type: 'email',
    component: <Input prefix={<MailOutlined />} placeholder="patient@example.com" />,
  },
  {
    name: 'date',
    label: 'Appointment Date & Time',
    required: true,
    message: 'Please select appointment date and time',
    component: <Input placeholder="YYYY-MM-DD HH:MM" />,
  },
  {
    name: 'provider',
    label: 'Provider',
    required: false,
    component: <Input placeholder="Dr. Smith" />,
  },
  {
    name: 'type',
    label: 'Appointment Type',
    required: false,
    component: (
      <Select placeholder="Select type">
        <Select.Option value="CHECKUP">Checkup</Select.Option>
        <Select.Option value="CONSULTATION">Consultation</Select.Option>
        <Select.Option value="FOLLOWUP">Follow-up</Select.Option>
        <Select.Option value="EMERGENCY">Emergency</Select.Option>
      </Select>
    ),
  },
  {
    name: 'reason',
    label: 'Reason for Visit',
    required: false,
    component: <TextArea placeholder="Reason for appointment" rows={3} />,
  },
  {
    name: 'notes',
    label: 'Notes',
    required: false,
    component: <TextArea placeholder="Additional notes" rows={2} />,
  },
];
