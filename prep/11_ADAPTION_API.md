# 11. Adaption inference API: models, prices, how to call it safely

Read 2026-11-02 from docs.adaptionlabs.ai (models, generate-a-model-response, responses/create, key-concepts). 1 credit = 1 USD (Vatsal confirmed), so prices below are USD per 1M tokens. Credits and the $500 itself still depend on the onboarding email.

## 1. Models
| Model ID | Input (cached) | Output | Context | Our role |
|---|---|---|---|---|
| `deepseek-v4-flash` | 0.04444 (0.001414) | 0.13332 | 1,048,576 | Frontier-ish extreme (used last sprint) |
| `glm-53-flash` | 0.15 (0.03) | 0.50 | 1,048,576 | Frontier-ish extreme (`glm53f` last sprint) |
| `glm-5.2` | 0.104 (0.10) | 4.40 | 786,432 | Large; not in our earlier list |
| `qwen3.5-397b` | 0.55 (0.225) | 3.50 | 131,072 | Average / big |
| `qwen3.8-27b` | 0.039 (0.0039) | 1.25 | 262,144 | Cheap (this is the "Qwen 3.8") |
| `gemma-4-31b-it` | 0.09 (0.05) | 0.34 | 256,000 | Cheap |
| `gemma-4-26b-a4b-it` | 0.0765 (0.0425) | 0.255 | 256,000 | Cheap (26B total, about 4B active) |
The "127B" model from Vatsal's message is not on this list. `client.models.list(type="hosted")` shows what your key can use (availability can vary by key). The docs do not label any model frontier or cheap; those labels are ours.

## 2. What it costs (the big finding)
Illustrative call: 1,500 input + 100 output tokens, no caching.
| Model | Per call | One 20-agent, 30-round episode (600 calls) | Episodes per $500 |
|---|---|---|---|
| deepseek-v4-flash | $0.00008 | about $0.05 | about 10,000 |
| gemma-4-26b-a4b-it | $0.00014 | about $0.08 | about 6,000 |
| gemma-4-31b-it | $0.00017 | about $0.10 | about 5,000 |
| qwen3.8-27b | $0.00018 | about $0.11 | about 4,500 |
| glm-53-flash | $0.00028 | about $0.17 | about 3,000 |
| glm-5.2 | $0.00060 | about $0.36 | about 1,400 |
| qwen3.5-397b | $0.00118 | about $0.71 | about 700 |
**Money is not the limit.** Running 100 episodes on every model costs roughly $15-30. The real limits are **rate limits (not documented), latency, and the reasoning-token multiplier** (if a model "thinks", output tokens can be 10x and cost scales with them). So the $200/$200/$100 split in 09 is moot: set a sprint cap (suggest $150) and keep the rest of the credits for Vatsal's own projects.

## 3. How to call it (and keep the sandbox sealed)
- `POST https://api.prod.adaptionlabs.ai/api/v1/responses`, header `Authorization: Bearer $ADAPTION_API_KEY`. Python: `from adaption import Adaption; client = Adaption(); client.responses.create(model=..., instructions=..., input=...)`; text in `response.output_text`; tokens in `usage`.
- Parameters we can set: `temperature` (0-2), `max_output_tokens`, `instructions`, `input`. **No `seed`** and no documented thinking/reasoning control.
- **Call hygiene (part of the sandbox):** plain model ID only, never `stack:<slug>`; `tools=[]` or omitted; no MCP, connectors or `file_search`; `store=false` (default); `agentic_memory=false`; `background` is unsupported. The API key lives in an environment variable on the host, never in a prompt, a log or a repo.
- **Our own world's tools** are plain text actions parsed by our code. Hosted tool-calling is not used.

## 4. Consequences for the plan
1. **No seed means hosted runs are not exactly reproducible.** Fix: cache every request and response to disk (hashed) and make reruns read from the cache. This replaces the "seeded rerun" idea for hosted arms and goes in the freeze.
2. **A fully LLM-driven swarm of 20 is now affordable.** The "few LLM agents among scripted bots" design is only needed for the local GPU arm. Hosted arms can run all agents as LLMs.
3. **Thinking and latency are unknowns.** The timing test must now run against the API too: time per call, parallel calls allowed, tokens used per call.
4. **Max-tokens cap** (for example 150) on every call bounds spend and speed.
5. **Open:** rate limits and concurrency (docs say see the FAQ at docs.adaptionlabs.ai/resources/faq or support@adaptionlabs.ai), and the exact IDs your key lists.

## Update 2026-11-02
Hosted timing is still unmeasured (the key arrives by email about 1-2 days before the sprint). `bench/api_timing.py` in the prior-work repo is ready (offline self-test passes); replace its assumed prices ($1 / $4 per million tokens) with the real list above before running. Local fallback numbers are in 13 section 9.
