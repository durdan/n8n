# Perplexity Node

This node allows you to make research queries using the Perplexity AI API and process the results.

## Prerequisites

- Perplexity API key
- n8n instance

## Configuration

### Credentials

1. Get your Perplexity API key from the Perplexity dashboard
2. Create new credentials in n8n of type 'Perplexity API'
3. Enter your API key

### Node Settings

- **Query**: The research query to send to Perplexity
- **Model**: Choose between available models:
  - pplx-7b-online: Faster, more concise responses
  - pplx-70b-online: More detailed, comprehensive responses

## Usage

### Basic Usage

1. Add Perplexity node to your workflow
2. Configure the query and model
3. Connect to other nodes to process the results

### Example Workflow

The `perplexityResearchEmail` workflow demonstrates how to:
1. Make a research query
2. Send results via email

## Output

The node outputs a JSON object containing:
- query: Original research query
- result: Research findings from Perplexity

## Error Handling

The node implements error handling for:
- API authentication errors
- Rate limiting
- Network issues
- Invalid queries

## Tips

- Use specific, well-formed queries for better results
- Consider rate limits in production use
- Implement retry logic for important workflows