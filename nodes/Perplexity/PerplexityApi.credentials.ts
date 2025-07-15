import { ICredentialType, INodeProperties } from 'n8n-workflow';

export class PerplexityApi implements ICredentialType {
  name = 'perplexityApi';
  displayName = 'Perplexity API';
  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: {
        password: true,
      },
      default: '',
      required: true,
    },
  ];
}