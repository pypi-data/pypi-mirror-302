# SARIF Manager

A simple CLI tool to parse SARIF files and output the results for different providers, like Azure DevOps, GitHub Actions, etc.

Currently supported providers:
- [x] Azure DevOps

Roadmap:

- [ ] GitHub Actions
- [ ] GitLab CI/CD
- [ ] Jenkins


## Installation

```bash
pip install sarif-manager
```

## Usage

```bash
sarif-manager --help
```

## Example

### Azure DevOps

Write logs in a pipeline:

```bash
azure write-logs \
    example.sarif \
    --org nightvision1 \
    --project temporary
```

Create work items:

```bash
sarif-manager azure create-work-items \
    example.sarif \
    --org nightvision1 \
    --project temporary
```

