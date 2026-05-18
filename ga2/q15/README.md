# Q15: Cloudflare Workers Serverless Deployment

A Cloudflare Worker that processes POST requests and returns transformed (reversed) data.

## Endpoint

```
POST https://tds-ga2-q15.tds-23f3003225.workers.dev/data
```

## Request Format

```json
{ "type": "...", "value": ... }
```

### Supported Types

| Type     | Behavior                              | Example Input          | Example Output        |
|----------|---------------------------------------|------------------------|-----------------------|
| `string` | Reverse characters                    | `"hello"`              | `"olleh"`             |
| `array`  | Reverse element order                 | `[1, 2, 3]`           | `[3, 2, 1]`          |
| `words`  | Reverse word order                    | `"hello world"`        | `"world hello"`       |
| `number` | Reverse digits (returns as integer)   | `12345`                | `54321`               |

## Response Format

```json
{
  "reversed": ...,
  "email": "your-student-id"
}
```

## Deployment

```bash
npm install
npx wrangler login
npx wrangler deploy
```

## Testing

```bash
node test.js
```

Or via curl:

```bash
curl -X POST https://tds-ga2-q15.tds-23f3003225.workers.dev/data \
  -H "Content-Type: application/json" \
  -d '{"type":"array","value":[59,69,14,1,4,85,13]}'
```

Expected response:

```json
{"reversed":[13,85,4,1,14,69,59],"email":"your-student-id"}
```
