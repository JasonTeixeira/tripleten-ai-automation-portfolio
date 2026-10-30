# Keep the official Ollama CPU binaries; omit unused CUDA/JetPack libraries.
FROM ollama/ollama@sha256:b2f0122c476bc9fe7ce679d8bb4bd555351e25e2554eefb156f61cb0a89cf429 AS vendor
FROM python:3.12-slim
COPY --from=vendor /usr/bin/ollama /usr/bin/ollama
COPY --from=vendor /usr/lib/ollama/*.so* /usr/lib/ollama/
COPY --from=vendor /usr/lib/ollama/llama-server /usr/lib/ollama/llama-server
COPY --from=vendor /usr/lib/ollama/llama-quantize /usr/lib/ollama/llama-quantize
COPY --from=vendor /usr/lib/ollama/*LICENSE /usr/lib/ollama/
ENV OLLAMA_HOST=0.0.0.0:11434
ENV LD_LIBRARY_PATH=/usr/lib/ollama
ENTRYPOINT ["/usr/bin/ollama"]
CMD ["serve"]
