# POC 1: Self-Hosted LLM (Ollama + GPT-OSS)
## Testing and Validation

**Status**: 🟢 Infrastructure Ready  
**Estimated Time**: 4-6 hours  
**Priority**: CRITICAL

---

## Overview

Test and validate your self-hosted LLM setup using the existing Ollama container with GPT-OSS 20B model.

**What's Already Done**:
- ✅ Ollama installed and running
- ✅ GPT-OSS 20B model downloaded (13GB)
- ✅ Container healthy and accessible

**What We Need to Validate**:
- [ ] Chat completion API
- [ ] Response streaming
- [ ] Response quality and coherence
- [ ] Performance benchmarks
- [ ] Error handling
- [ ] Concurrent request handling

---

## Prerequisites

```bash
# Verify Ollama is running
docker ps | grep ollama

# Should show: lm-ollama container UP

# Verify model is available
docker exec lm-ollama ollama list

# Should show: gpt-oss:20b
```

---

## Test Suite

### Test 1: Basic Chat Completion ⭐

**Goal**: Verify Ollama responds to basic prompts

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss:20b",
  "prompt": "What is the capital of France?",
  "stream": false
}'
```

**Success Criteria**:
- [x] Returns HTTP 200
- [x] Response contains "Paris"
- [x] Response time < 10 seconds
- [x] JSON format is valid

**Document**: Response time, token count, quality

---

### Test 2: Chat Format API ⭐⭐

**Goal**: Test conversation-style API

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "Explain photosynthesis simply."}
  ],
  "stream": false
}'
```

**Success Criteria**:
- [x] Returns HTTP 200
- [x] Response explains photosynthesis correctly
- [x] Follows system message instruction
- [x] Response is educational and clear

**Document**: Response quality, adherence to system prompt

---

### Test 3: Response Streaming ⭐⭐⭐

**Goal**: Validate streaming responses work

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss:20b",
  "prompt": "Count from 1 to 10 with explanations.",
  "stream": true
}'
```

**Success Criteria**:
- [x] Returns chunked responses
- [x] Each chunk is valid JSON
- [x] Final response is complete
- [x] No dropped chunks

**Document**: Streaming behavior, chunk timing

---

### Test 4: Educational Content Generation ⭐⭐⭐

**Goal**: Test content generation quality for educational use

**Test A: Math Explanation**
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "system", "content": "You are a high school math teacher. Explain concepts clearly."},
    {"role": "user", "content": "Explain the Pythagorean theorem with an example."}
  ],
  "stream": false
}'
```

**Test B: Science Explanation**
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "system", "content": "You are a science teacher. Use simple language."},
    {"role": "user", "content": "How does DNA replication work?"}
  ],
  "stream": false
}'
```

**Test C: History Summary**
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "system", "content": "You are a history teacher."},
    {"role": "user", "content": "Summarize the causes of World War 1 in 3 paragraphs."}
  ],
  "stream": false
}'
```

**Success Criteria**:
- [x] Content is factually accurate
- [x] Appropriate for high school level
- [x] Clear and well-structured
- [x] Matches subject/difficulty level

**Document**: Quality assessment for each subject

---

### Test 5: Performance Benchmarking ⭐⭐⭐

**Goal**: Measure response times and throughput

Create a simple benchmark script:

```bash
# Save as test-performance.sh
#!/bin/bash

echo "Running 10 test requests..."
for i in {1..10}; do
  start_time=$(date +%s%N)
  
  curl -s http://localhost:11434/api/generate -d '{
    "model": "gpt-oss:20b",
    "prompt": "Explain gravity in one sentence.",
    "stream": false
  }' > /dev/null
  
  end_time=$(date +%s%N)
  duration=$(( (end_time - start_time) / 1000000 ))
  
  echo "Request $i: ${duration}ms"
done
```

**Success Criteria**:
- [x] Average response time < 5000ms
- [x] No timeouts
- [x] Consistent performance
- [x] Memory usage stable

**Document**: 
- Average response time
- Min/max response time
- Standard deviation
- Resource usage (CPU/RAM)

---

### Test 6: Error Handling ⭐⭐

**Goal**: Validate graceful error handling

**Test A: Invalid Model**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "nonexistent-model",
  "prompt": "Test",
  "stream": false
}'
```

**Expected**: Error message about model not found

**Test B: Empty Prompt**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss:20b",
  "prompt": "",
  "stream": false
}'
```

**Expected**: Handles empty prompt gracefully

**Test C: Very Long Prompt**
```bash
# Create a ~2000 word prompt
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss:20b",
  "prompt": "Explain [long text here]...",
  "stream": false
}'
```

**Expected**: Handles long input or returns appropriate error

**Success Criteria**:
- [x] Returns appropriate error codes
- [x] Error messages are clear
- [x] No crashes or hangs

---

### Test 7: Concurrent Requests ⭐⭐⭐

**Goal**: Test handling of multiple simultaneous requests

Create a concurrent test script:

```bash
# Save as test-concurrent.sh
#!/bin/bash

echo "Sending 5 concurrent requests..."

for i in {1..5}; do
  (
    curl -s http://localhost:11434/api/generate -d '{
      "model": "gpt-oss:20b",
      "prompt": "What is '$(($i + 1))' plus '$(($i + 2))'?",
      "stream": false
    }' | jq -r '.response' > response_$i.txt
    echo "Request $i completed"
  ) &
done

wait
echo "All requests completed"
cat response_*.txt
rm response_*.txt
```

**Success Criteria**:
- [x] All requests complete successfully
- [x] No request errors or timeouts
- [x] Responses are correct
- [x] Reasonable throughput maintained

**Document**: Concurrent request handling capacity

---

### Test 8: Model Switching (Bonus) ⭐

**Goal**: Test if other models can be loaded

```bash
# Pull a smaller model for testing
docker exec lm-ollama ollama pull llama3.2:1b

# Test with new model
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

**Success Criteria**:
- [x] New model downloads successfully
- [x] Model switch works
- [x] Both models can be used

---

## Node.js Integration Test

Create a simple Node.js client to test programmatic access:

```javascript
// save as test-ollama.js
const axios = require('axios');

async function testOllama() {
  try {
    const response = await axios.post('http://localhost:11434/api/chat', {
      model: 'gpt-oss:20b',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Explain quantum computing in simple terms.' }
      ],
      stream: false
    });
    
    console.log('Response:', response.data.message.content);
    console.log('Tokens:', response.data.eval_count);
    console.log('Duration:', response.data.total_duration / 1e9, 'seconds');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testOllama();
```

Run with:
```bash
npm init -y
npm install axios
node test-ollama.js
```

---

## Python Integration Test

Create a Python client:

```python
# save as test_ollama.py
import requests
import json
import time

def test_ollama():
    url = 'http://localhost:11434/api/chat'
    
    payload = {
        'model': 'gpt-oss:20b',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful science tutor.'},
            {'role': 'user', 'content': 'Explain how vaccines work.'}
        ],
        'stream': False
    }
    
    start = time.time()
    response = requests.post(url, json=payload)
    duration = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['message']['content']}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Tokens: {data.get('eval_count', 'N/A')}")
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    test_ollama()
```

Run with:
```bash
pip install requests
python test_ollama.py
```

---

## Success Metrics

POC 1 is successful when:

1. ✅ All 8 tests pass
2. ✅ Response time < 5 seconds (P95)
3. ✅ Content quality is educational
4. ✅ Error handling is graceful
5. ✅ Can handle 3+ concurrent requests
6. ✅ Integration code works (Node.js/Python)

---

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Response Time (avg) | < 3s | ___ |
| Response Time (P95) | < 5s | ___ |
| Concurrent Requests | 3+ | ___ |
| Memory Usage | Stable | ___ |
| CPU Usage | < 80% | ___ |
| Error Rate | < 1% | ___ |

---

## Deliverables

After completing POC 1:

1. ✅ **Test Results Document**
   - All test outcomes
   - Performance metrics
   - Error cases documented

2. ✅ **Integration Code**
   - Node.js client example
   - Python client example
   - Both tested and working

3. ✅ **Performance Report**
   - Benchmarks recorded
   - Resource usage documented
   - Bottlenecks identified

4. ✅ **Best Practices Guide**
   - Optimal prompt formats
   - Error handling patterns
   - Performance tips

---

## Common Issues & Solutions

### Issue: Slow First Response
**Solution**: Model loading takes time on first request. Subsequent requests faster.

### Issue: Memory Usage High
**Solution**: GPT-OSS 20B requires ~13GB. Normal for this model size.

### Issue: Timeout on Long Prompts
**Solution**: Increase timeout or use streaming for long responses.

---

## Next Steps

After POC 1 completion:

1. Document findings in `RESULTS.md`
2. Move to **POC 3: Vector Database** (infrastructure ready)
3. Use learnings to optimize full implementation

---

**Status**: Ready to Start  
**Infrastructure**: ✅ Ready  
**Estimated Completion**: 4-6 hours
