# srt-audit

A lightweight, **zero-runtime-dependency** command-line validator for `.srt` / SubRip subtitle files. Made for caption editors, video creators, CI pipelines, and localization workflows.

> Early-stage project: v0.1.0. No adoption, download, or contributor metrics are claimed.

## Features
- Detect missing or out-of-order cue indexes.
- Validate `HH:MM:SS,mmm` timestamps.
- Flag non-positive cue durations and overlapping cues.
- Detect missing subtitle text and incomplete cues.
- Machine-readable JSON and nonzero exit codes for CI.
- Works on Python 3.9+ without runtime dependencies.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
srt-audit captions.srt
srt-audit --json captions.srt translated.srt
```

Exit code `0` = all files valid; `1` = one or more files invalid/unreadable.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Limitations

SRT has multiple permissive dialects. This version intentionally checks a strict common form: sequential numeric indexes, comma-millisecond timestamps, non-overlapping cues. It does not fix files automatically or check reading speed.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports, tests, documentation improvements, and compatibility fixes are welcome.

## License

MIT. See [LICENSE](LICENSE).
