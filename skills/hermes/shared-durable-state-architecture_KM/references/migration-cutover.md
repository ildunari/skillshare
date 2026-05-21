# Migration cutover checklist

When moving canonical state out of the repo, patch all of these together:
- `HERMES.md`
- helper scripts
- cron prompts/jobs
- skills that teach canonical paths
- repo docs/specs that currently imply the old home
- troubleshooting skills for old path assumptions when relevant

Do not leave a split-brain period where some surfaces still say the repo path is canonical.

## Legacy path handling

For old canonical homes, decide explicitly whether they become:
- mirror
- redirect stub
- archive
- or are retired entirely

Write that decision down. Do not leave it implicit.
