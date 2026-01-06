/**
 * Chatbot Service
 * API communication for the AI assistant with streaming support
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
 * Stream a message to the chatbot with real-time status updates
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous conversation messages
 * @param {Object} callbacks - Callbacks for streaming events
 * @param {Function} callbacks.onStatus - Called for each status message: (statusData) => void
 * @param {Function} callbacks.onResponse - Called with final response: (responseData) => void
 * @param {Function} callbacks.onError - Called on error: (error) => void
 */
export const streamChatMessage = async (message, conversationHistory = [], callbacks = {}) => {
  const { onStatus, onResponse, onError } = callbacks;
  const apiBase = getAiApiBaseUrl();
  const url = `${apiBase}/chat`;

  console.log('[STREAM_START] Chatbot stream starting:', url);

  try {
    // Create AbortController for 30-second timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: conversationHistory,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[STREAM_ERROR] Request failed:', response.status, errorText);
      const error = new ApiError(
        `Chat request failed: ${response.statusText}`,
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
    let chunkCount = 0;

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        console.log(`[STREAM_END] Chatbot stream complete - ${chunkCount} chunks processed`);
        break;
      }

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
          chunkCount++;

          switch (chunk.type) {
            case 'status':
              console.log('[STREAM_STATUS]', chunk.data.operation, '-', chunk.data.message);
              if (onStatus) onStatus(chunk.data);
              break;

            case 'response':
              console.log('[STREAM_RESPONSE] Final response received');
              if (onResponse) onResponse(chunk.data);
              break;

            case 'error':
              console.error('[STREAM_ERROR]', chunk.data.error, '-', chunk.data.message);
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
              console.warn('[STREAM_WARN] Unknown chunk type:', chunk.type);
          }
        } catch (parseError) {
          console.error('[STREAM_ERROR] Failed to parse NDJSON chunk:', line, parseError);
          // Continue processing other chunks
        }
      }
    }

    // Process any remaining data in buffer
    if (buffer.trim()) {
      try {
        const chunk = JSON.parse(buffer);
        if (chunk.type === 'response' && onResponse) {
          console.log('[STREAM_RESPONSE] Final response from buffer');
          onResponse(chunk.data);
        }
      } catch (parseError) {
        console.error('[STREAM_ERROR] Failed to parse final chunk:', buffer, parseError);
      }
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('[STREAM_ERROR] Request timeout after 30 seconds');
      if (onError) {
        onError(new ApiError('Request timeout - please try again', 408, 'timeout'));
      }
    } else {
      console.error('[STREAM_ERROR] Streaming chat error:', error);
      if (onError) onError(error);
    }
  }
};
