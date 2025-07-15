import { PerplexityNode } from '../../../nodes/Perplexity/PerplexityNode';
import { mockExecuteFunction } from '../../helpers';

describe('PerplexityNode', () => {
  let node: PerplexityNode;
  let mockExecute: any;

  beforeEach(() => {
    node = new PerplexityNode();
    mockExecute = mockExecuteFunction(node);
  });

  it('should have valid properties', () => {
    expect(node.description.properties).toBeDefined();
    expect(node.description.properties.length).toBeGreaterThan(0);
  });

  it('should require API credentials', () => {
    const creds = node.description.credentials;
    expect(creds).toContainEqual({
      name: 'perplexityApi',
      required: true,
    });
  });

  it('should make API call with correct parameters', async () => {
    const mockFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => ({
        choices: [{
          message: {
            content: 'Test response'
          }
        }]
      })
    });
    global.fetch = mockFetch;

    await mockExecute.execute.call({
      getInputData: () => [{}],
      getNodeParameter: (param: string) => {
        if (param === 'query') return 'test query';
        if (param === 'model') return 'pplx-7b-online';
      },
      getCredentials: () => ({ apiKey: 'test-key' })
    });

    expect(mockFetch).toHaveBeenCalledWith(
      'https://api.perplexity.ai/chat/completions',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Authorization': 'Bearer test-key'
        })
      })
    );
  });

  it('should handle API errors', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      statusText: 'Bad Request'
    });

    await expect(mockExecute.execute.call({
      getInputData: () => [{}],
      getNodeParameter: () => 'test',
      getCredentials: () => ({ apiKey: 'test-key' })
    })).rejects.toThrow('Perplexity API error: Bad Request');
  });
});