# GitHub Branch Rulesets Guide

This guide explains how to configure branch rules in GitHub, especially for the dev branch.

## Goal

Use a safe workflow:

1. feature branches merge into dev
2. dev is the integration and validation branch
3. dev merges into main only when stable

## Before You Start

Make sure these branches already exist in GitHub:

- main
- dev

If they do not exist yet, create and push them locally first.

## Create Ruleset for dev Branch

1. Open your repository in GitHub.
2. Go to Settings.
3. Open Rules, then Rulesets.
4. Click New branch ruleset.
5. Set Ruleset Name to dev protection.
6. Keep Enforcement status as Active.
7. Leave Bypass list empty.

### Target Branch

1. In Target branches, click Add target.
2. Choose Include by pattern.
3. Type dev.
4. Save the target.

### Rules to Enable for dev

Enable these options:

- Require a pull request before merging
- Block force pushes
- Restrict deletions

Recommended for better quality:

- Require status checks to pass

Important note:

If GitHub says required checks cannot be empty, disable this option temporarily, save the ruleset, run one PR to generate checks, then edit the ruleset and add the check name.

### Pull Request Details for dev

Inside the pull request rule, recommended values:

- Minimum approvals: 1
- Require conversation resolution before merging: On
- Dismiss stale pull request approvals when new commits are pushed: Optional

## Create Ruleset for main Branch

1. Create another branch ruleset.
2. Ruleset Name: main protection.
3. Target branch pattern: main.

Enable these options:

- Require a pull request before merging
- Require status checks to pass
- Require conversation resolution before merging
- Block force pushes
- Restrict deletions

Recommended for main:

- Minimum approvals: 1 or 2

## Set Default Branch

1. Go to Settings, then Branches.
2. Set Default branch to main.

## Working Model

## Branch Workflow

Use this standard workflow for all new work:

1. Create a feature branch from dev.
2. Make your changes in the feature branch.
3. Open a pull request from the feature branch into dev.
4. Review the pull request and wait for checks to pass.
5. Merge the feature branch into dev.
6. When dev is stable, open a pull request from dev into main.
7. Merge dev into main only after all checks pass.

Important rule:

- Do not push directly to main.
- main should be protected so changes enter only through pull requests.

Daily development:

1. Create feature branch from dev.
2. Open PR from feature branch to dev.
3. Merge after checks and review.

Release promotion:

1. Open PR from dev to main.
2. Merge after all checks pass.

## Suggested Branch Names

- feature/github-ingestion
- feature/new-kpi-model
- fix/dbt-schema-bug
- chore/readme-update

## Common Errors and Fixes

Error: Repository not found

- Verify remote URL owner and repository name.
- Verify repository exists in GitHub web.
- Verify authentication is valid.

Error: Required status checks cannot be empty

- Save without required checks.
- Run one pull request with Actions.
- Edit ruleset and add actual check names.

Error: No checks available in list

- Trigger GitHub Actions by pushing a commit or opening a PR.
- Return to ruleset and select the check.

## Quick Verification Checklist

- main and dev exist in GitHub
- main is default branch
- main ruleset exists and is active
- dev ruleset exists and is active
- force push blocked on main and dev
- pull requests required on main and dev
- status checks required where configured

## How to Send Screenshots for Faster Help

If you need support while configuring GitHub settings, you can send a screenshot and I will guide you step by step.

For best results, include these details in the screenshot:

- Full page header so I can identify the exact GitHub section.
- The selected options or toggles currently enabled.
- Any visible warning or error message text.
- The URL path shown in the browser (if possible).

When sharing the screenshot, add a short message with:

1. What you expected to happen.
2. What actually happened.
3. Which branch you are configuring (`main` or `dev`).

This helps me give precise instructions without trial and error.

## Example Screenshots in Documentation

You can embed screenshots directly in this guide.

1. Save the image under `docs/github/images/`.
2. Use descriptive file names with numeric prefixes.
3. Add a short caption under each image.

### Example: Status Check Error

![Required status checks cannot be empty](images/Captura%20de%20pantalla%202026-08-06%20005036.png)

Caption: GitHub ruleset validation error when `Require status checks to pass` is enabled without selecting at least one check.

### Example: Target Branch Pattern

![Main branch ruleset target configuration](images/Captura%20de%20pantalla%202026-08-06%20005119.png)

Caption: Active ruleset example showing `main` configured in the branch targeting criteria.

### Example: Required Checks Selected

If no checks are listed yet, run one pull request so GitHub Actions creates check runs, then return to the ruleset and add them.

### Notes

- Paths are relative to `docs/github/BRANCH_RULESETS_GUIDE.md`.
- GitHub and VS Code Markdown preview will render these images automatically.
