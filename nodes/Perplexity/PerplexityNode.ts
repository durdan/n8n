import { IExecuteFunctions } from 'n8n-core';
import { INodeExecutionData, INodeType, INodeTypeDescription } from 'n8n-workflow';

export class PerplexityNode implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Perplexity',
    name: 'perplexity',
    group: ['research'],
    version: 1,
    description: 'Make requests to Perplexity API',
    defaults: {
      name: 'Perplexity',
    },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [
      {
        name: 'perplexityApi',
        required: true,
      },
    ],
    properties: [
      {
        displayName: 'Query',
        name: 'query',
        type: 'string',
        default: '',
        required: true,
        description: 'Research query to send to Perplexity',
      },
      {
        displayName: 'Model',
        name: 'model',
        type: 'options',
        options: [
          {
            name: 'pplx-7b-online',
            value: 'pplx-7b-online'
          },
          {
            name: 'pplx-70b-online',
            value: 'pplx-70b-online'
          }
        ],
        default: 'pplx-7b-online',
        description: 'Model to use for research',
      }
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    for (let i = 0; i < items.length; i++) {
      const query = this.getNodeParameter('query', i) as string;
      const model = this.getNodeParameter('model', i) as string;
      
      const credentials = await this.getCredentials('perplexityApi');
      
      try {
        const response = await fetch('https://api.perplexity.ai/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${credentials.apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model,
            messages: [{ role: 'user', content: query }]
          })
        });

        if (!response.ok) {
          throw new Error(`Perplexity API error: ${response.statusText}`);
        }

        const data = await response.json();
        
        returnData.push({
          json: {
            query,
            result: data.choices[0].message.content,
          }
        });
      } catch (error) {
        throw new Error(`Failed to get research results: ${error.message}`);
      }
    }

    return [returnData];
  }
}