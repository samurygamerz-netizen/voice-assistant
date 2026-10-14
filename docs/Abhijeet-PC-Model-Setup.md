# Abhijeet's FOXSI Model Setup (8 GB RAM)

This guide is for the Windows 10 PC with Intel Core i3-6100T, 8 GB RAM, and no dedicated GPU.

## Recommended starting setup

### Main local chat model
- **Qwen2.5-1.5B-Instruct, GGUF, Q4_K_M**
- Model page: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF
- Start with this small model and test real memory usage before adding other models.

### Optional alternative chat model
- **Gemma 2 2B, GGUF, Q4_K_M**
- Model page: https://huggingface.co/google/gemma-2-2b-it
- Treat this as an alternative to the main model, not something to keep loaded at the same time. Confirm that the chosen repository provides the GGUF format you need before downloading.

### Optional coding model
- **Qwen2.5-Coder-1.5B-Instruct, GGUF, Q4_K_M**
- Model page: https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF
- Load it only when coding assistance is needed; unload the main chat model first.

### Speech-to-text
- **faster-whisper**, initially test the **tiny** model with CPU INT8.
- Project: https://github.com/SYSTRAN/faster-whisper
- Recognition quality and speed vary by language, microphone, and CPU; test Hindi/Hinglish commands before relying on it.

### Text-to-speech
- **Piper**, with a compatible Hindi voice if available for the chosen runtime.
- Project: https://github.com/rhasspy/piper
- Verify voice model compatibility and license before bundling it with FOXSI.

## Setup order
1. Install or configure the project's supported `llama.cpp` / GGUF runtime.
2. Download only Qwen2.5-1.5B-Instruct Q4_K_M first.
3. Run a short prompt test and check Windows Task Manager for RAM use.
4. Test microphone input with faster-whisper Tiny CPU INT8.
5. Test Piper speech output separately.
6. Add the Coder or Gemma model only after the basic assistant is stable.

## Important limits
- GGUF file size is **not** the same as total runtime RAM use. Context length, KV cache, runtime overhead, Windows, and other applications also use memory.
- With 8 GB RAM and an older dual-core i3, performance is not guaranteed to be smooth. Keep context length modest (start around 2,048 tokens), close unnecessary apps, and test end-to-end latency.
- Keep only one LLM loaded at a time. Speech recognition and TTS still consume CPU and memory while the assistant runs.
- Qwen2.5 3B and Phi-3.5 Mini Q4 can be tested later, but are not the first choices for this machine.
- Do not download model weights into the Git repository. Store them locally in the project's ignored `models/` folder and check each model's license before redistribution.

## Suggested model manager behavior
- Scan `models/` for supported `.gguf` files.
- Show model name, file size, and selected status.
- Unload the active LLM before loading another.
- Handle load failures gracefully and display a clear RAM/resource warning.
