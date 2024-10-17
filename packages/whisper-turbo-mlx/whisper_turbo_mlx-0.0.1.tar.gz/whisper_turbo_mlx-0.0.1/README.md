# WTM (Whisper Turbo MLX)

This repository provides a fast implementation of the [Whisper](openai/whisper-large-v3-turbo) model using MLX, designed for efficient audio transcription.

![Alt text](https://raw.githubusercontent.com/JosefAlbers/whisper-turbo-mlx/main/assets/benchmark.png)

## Installation

```zsh
brew install ffmpeg
git clone https://github.com/JosefAlbers/whisper-turbo-mlx.git
cd whisper-turbo-mlx
pip install -e .
```

## Usage

To transcribe an audio file, call the `transcribe` function:

```zsh
transcribe 'test.wav'
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.