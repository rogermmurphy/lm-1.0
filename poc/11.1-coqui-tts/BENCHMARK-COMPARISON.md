# Processing Time Comparison: Azure vs Coqui TTS

## Azure TTS
| Test | Characters | Time |
|------|------------|------|
| test_basic | 62 | 0.797s |
| test_guy | 38 | 0.926s |
| test_ssml | 60 | 0.861s |
| benchmark_short | 13 | 0.797s |
| benchmark_medium | 114 | 0.926s |
| benchmark_long | 402 | 0.861s |
| benchmark_very_long | 877 | 0.907s |

## Coqui TTS
| Test | Characters | Time |
|------|------------|------|
| test_basic | 62 | 7.323s |
| test_guy | 27 | 3.121s |
| test_ssml | 60 | 5.634s |
| benchmark_short | 13 | 2.243s |
| benchmark_medium | 114 | 11.803s |
| benchmark_long | 348 | 30.569s |
| benchmark_very_long | 778 | 82.629s |

## Difference
| Test | Azure | Coqui | Coqui/Azure |
|------|-------|-------|-------------|
| short | 0.797s | 2.243s | 2.8x slower |
| medium | 0.926s | 11.803s | 12.7x slower |
| long | 0.861s | 30.569s | 35.5x slower |
| very_long | 0.907s | 82.629s | 91.1x slower |
