import { useState, useEffect, useRef } from 'react';
import { Modal, Spin, Alert } from 'antd';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import mermaid from 'mermaid';

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'monospace',
});

const ReadmeViewer = ({ open, onClose }) => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const contentRef = useRef(null);

  useEffect(() => {
    if (open) {
      fetchReadme();
    }
  }, [open]);

  useEffect(() => {
    if (content && open && contentRef.current) {
      // Render mermaid diagrams after content is set
      const renderMermaid = async () => {
        let attempts = 0;
        const maxAttempts = 10;
        const retryInterval = 50;

        const tryRender = async () => {
          try {
            const mermaidElements = document.querySelectorAll('.mermaid');

            if (mermaidElements.length === 0 && attempts < maxAttempts) {
              attempts++;
              setTimeout(tryRender, retryInterval);
              return;
            }

            for (const element of mermaidElements) {
              if (element.getAttribute('data-processed') !== 'true') {
                const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
                element.setAttribute('data-processed', 'true');
                const { svg } = await mermaid.render(id, element.textContent);
                element.innerHTML = svg;
              }
            }
          } catch (err) {
            console.error('Mermaid rendering error:', err);
          }
        };

        requestAnimationFrame(() => {
          requestAnimationFrame(tryRender);
        });
      };

      renderMermaid();
    }
  }, [content, open]);

  const fetchReadme = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/README.md');
      if (!response.ok) {
        throw new Error(`Failed to fetch README: ${response.statusText}`);
      }
      const text = await response.text();
      setContent(text);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="Project Documentation"
      open={open}
      onCancel={onClose}
      footer={null}
      width="90%"
      style={{ top: 20 }}
      bodyStyle={{
        maxHeight: 'calc(100vh - 200px)',
        overflow: 'auto',
        padding: '24px',
      }}
    >
      {loading && (
        <div style={{ textAlign: 'center', padding: '48px 0' }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>Loading documentation...</div>
        </div>
      )}

      {error && (
        <Alert
          message="Error Loading Documentation"
          description={error}
          type="error"
          showIcon
        />
      )}

      {!loading && !error && content && (
        <div className="readme-content" ref={contentRef}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                const isMermaid = match && match[1] === 'mermaid';

                if (isMermaid) {
                  return (
                    <div className="mermaid" style={{ marginBottom: 16 }}>
                      {String(children).replace(/\n$/, '')}
                    </div>
                  );
                }

                return inline ? (
                  <code className={className} {...props}>
                    {children}
                  </code>
                ) : (
                  <pre style={{
                    background: '#f6f8fa',
                    padding: '16px',
                    borderRadius: '6px',
                    overflow: 'auto',
                  }}>
                    <code className={className} {...props}>
                      {children}
                    </code>
                  </pre>
                );
              },
              h1: ({ children }) => (
                <h1 style={{ borderBottom: '1px solid #d0d7de', paddingBottom: 8, marginTop: 24 }}>
                  {children}
                </h1>
              ),
              h2: ({ children }) => (
                <h2 style={{ borderBottom: '1px solid #d0d7de', paddingBottom: 8, marginTop: 24 }}>
                  {children}
                </h2>
              ),
              h3: ({ children }) => (
                <h3 style={{ marginTop: 20 }}>{children}</h3>
              ),
              table: ({ children }) => (
                <div style={{ overflowX: 'auto', marginBottom: 16 }}>
                  <table style={{
                    borderCollapse: 'collapse',
                    width: '100%',
                    border: '1px solid #d0d7de',
                  }}>
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => (
                <th style={{
                  border: '1px solid #d0d7de',
                  padding: '8px 16px',
                  background: '#f6f8fa',
                  textAlign: 'left',
                }}>
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td style={{
                  border: '1px solid #d0d7de',
                  padding: '8px 16px',
                }}>
                  {children}
                </td>
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      )}
    </Modal>
  );
};

export default ReadmeViewer;
