/**
 * Customer Chatbot Service
 * API communication for the customer AI assistant with streaming support
 */

import { ApiError } from './api';

/**
 * Get AI API base URL (Function URL for streaming)
 * Falls back to regular API base URL if not configured
 */
const getAiApiBaseUrl = () => {
  return import.meta.env.VITE_AI_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;
};

/**
 * Stream a message to the customer chatbot with real-time status updates
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous conversation messages
 * @param {string} customerEmail - Customer email for data filtering
 * @param {Object} callbacks - Callbacks for streaming events
 * @param {Function} callbacks.onStatus - Called for each status message: (statusData) => void
 * @param {Function} callbacks.onResponse - Called with final response: (responseData) => void
 * @param {Function} callbacks.onError - Called on error: (error) => void
 */
export const streamCustomerChatMessage = async (
  message,
  conversationHistory = [],
  customerEmail,
  callbacks = {}
) => {
  const { onStatus, onResponse, onError } = callbacks;
  const apiBase = getAiApiBaseUrl();
  const url = `${apiBase}/customer-chat`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: conversationHistory,
        customerEmail,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      const error = new ApiError(
        `Customer chat request failed: ${response.statusText}`,
        response.status,
        errorText
      );
      if (onError) onError(error);
      return;
    }

    // Parse NDJSON streaming response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      // Append to buffer and process complete lines
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');

      // Keep last incomplete line in buffer
      buffer = lines.pop() || '';

      // Process complete lines
      for (const line of lines) {
        if (!line.trim()) continue;

        try {
          const chunk = JSON.parse(line);

          switch (chunk.type) {
            case 'status':
              if (onStatus) onStatus(chunk.data);
              break;

            case 'response':
              if (onResponse) onResponse(chunk.data);
              break;

            case 'error':
              if (onError) {
                onError(
                  new ApiError(
                    chunk.data.message || 'Unknown error',
                    500,
                    chunk.data.error
                  )
                );
              }
              break;

            default:
              console.warn('Unknown chunk type:', chunk.type);
          }
        } catch (parseError) {
          console.error('Failed to parse NDJSON chunk:', line, parseError);
          // Continue processing other chunks
        }
      }
    }

    // Process any remaining data in buffer
    if (buffer.trim()) {
      try {
        const chunk = JSON.parse(buffer);
        if (chunk.type === 'response' && onResponse) {
          onResponse(chunk.data);
        }
      } catch (parseError) {
        console.error('Failed to parse final chunk:', buffer, parseError);
      }
    }
  } catch (error) {
    console.error('Streaming customer chat error:', error);
    if (onError) onError(error);
  }
};
