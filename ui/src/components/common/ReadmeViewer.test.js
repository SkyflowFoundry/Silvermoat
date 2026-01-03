import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ReadmeViewer from './ReadmeViewer';

// Mock mermaid
vi.mock('mermaid', () => ({
  default: {
    initialize: vi.fn(),
    render: vi.fn().mockResolvedValue({ svg: '<svg></svg>' }),
  },
}));

describe('ReadmeViewer', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    mockOnClose.mockClear();
    global.fetch = vi.fn();
  });

  it('renders modal when open', () => {
    render(<ReadmeViewer open={true} onClose={mockOnClose} />);
    expect(screen.getByText('Project Documentation')).toBeInTheDocument();
  });

  it('does not render modal when closed', () => {
    render(<ReadmeViewer open={false} onClose={mockOnClose} />);
    expect(screen.queryByText('Project Documentation')).not.toBeInTheDocument();
  });

  it('fetches and displays README content', async () => {
    const mockContent = '# Test README\n\nThis is a test.';
    global.fetch.mockResolvedValueOnce({
      ok: true,
      text: async () => mockContent,
    });

    render(<ReadmeViewer open={true} onClose={mockOnClose} />);

    // Should show loading initially
    expect(screen.getByText('Loading documentation...')).toBeInTheDocument();

    // Wait for content to load
    await waitFor(() => {
      expect(screen.getByText('Test README')).toBeInTheDocument();
    });

    expect(screen.getByText('This is a test.')).toBeInTheDocument();
  });

  it('handles fetch errors', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<ReadmeViewer open={true} onClose={mockOnClose} />);

    await waitFor(() => {
      expect(screen.getByText('Error Loading Documentation')).toBeInTheDocument();
    });

    expect(screen.getByText(/Network error/i)).toBeInTheDocument();
  });

  it('handles HTTP errors', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      statusText: 'Not Found',
    });

    render(<ReadmeViewer open={true} onClose={mockOnClose} />);

    await waitFor(() => {
      expect(screen.getByText('Error Loading Documentation')).toBeInTheDocument();
    });
  });

  it('calls onClose when modal is closed', async () => {
    const mockContent = '# Test';
    global.fetch.mockResolvedValueOnce({
      ok: true,
      text: async () => mockContent,
    });

    const { container } = render(<ReadmeViewer open={true} onClose={mockOnClose} />);

    await waitFor(() => {
      expect(screen.getByText('Test')).toBeInTheDocument();
    });

    // Find and click the close button (X icon in modal)
    const closeButton = container.querySelector('.ant-modal-close');
    if (closeButton) {
      await userEvent.click(closeButton);
      expect(mockOnClose).toHaveBeenCalledTimes(1);
    }
  });

  it('fetches README when modal opens', async () => {
    const mockContent = '# Initial';
    global.fetch.mockResolvedValue({
      ok: true,
      text: async () => mockContent,
    });

    const { rerender } = render(<ReadmeViewer open={false} onClose={mockOnClose} />);

    expect(global.fetch).not.toHaveBeenCalled();

    rerender(<ReadmeViewer open={true} onClose={mockOnClose} />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/README.md');
    });
  });
});
