# Model inference performance stress test

```shell
evalscope-perf http://172.16.33.66:9997/v1/chat/completions gpt-4-32k \
    ./datasets/open_qa.jsonl \
    --parallels 4 \
    --parallels 8 \
    --parallels 16 \
    --n 20
```