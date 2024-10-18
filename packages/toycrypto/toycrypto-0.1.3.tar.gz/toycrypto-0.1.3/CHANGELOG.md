[

# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.1.3 2024-10-17

### Added

- `py.typed` file. (This is the reason for the version bump.)

### Improved

- `ec` classes use `@property` instead of exposing some attributes directly.
- `ec` module now has a [documentation page]( https://jpgoldberg.github.io/toy-crypto-math/ec.html).
- This changelog is now in the proper location.
- This changelog is better formatted.

## 0.1.2 2024-10-15

### Added

- _Partial_ [documentation][docs].

### Improved

- Testing covers all supported Python versions (3.11, 3.12, 3.13)

## 0.1.1 2024-10-11

### Removed

- `redundent.prod()`. It was annoying type checkers and is, after all, redundant.

### Added

- `utils.xor()` function for xor-ing bytes with a pad.
- Explicit support for Python 3.13
- Github Actions for linting and testing

### Improved

- Conforms to some stronger lint checks
- Spelling in some code comments

## 0.1.0 - 2024-10-10

### Added

- First public release
  
[docs]: https://jpgoldberg.github.io/toy-crypto-math/