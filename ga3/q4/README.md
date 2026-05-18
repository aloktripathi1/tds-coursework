# Q4: Automating Repository Updates for DevSync (Scheduled GitHub Action)

## Task

Create a scheduled [GitHub action](https://github.com/features/actions) that runs daily and automatically adds a commit to the remote repository. The automated workflow is part of DevSync Solutions' requirement to track daily activity, automate documentation, and provide an additional layer of backup.

---

## Requirements

* Configure the workflow to run **once per day** using specific `cron` syntax (e.g., `30 12 * * *`). Wildcards (`* * * * *`) are not permitted for the minute/hour slots.
* The workflow must contain a step whose name specifically includes the email: `your-student-id`.
* The workflow must programmatically create a commit in the repository during each automated run.
* The YAML file must be correctly placed in the `.github/workflows/` directory.

---

## Approach

### 1. Workflow Definition
A new YAML file `.github/workflows/daily-commit.yml` was created in the Git repository structure. 
The workflow is configured with two triggers (`on:`):
1. `schedule`: Utilizes a cron expression to trigger automatically (e.g., `cron: '30 12 * * *'` for 12:30 UTC every day).
2. `workflow_dispatch`: Permits manual execution directly from the GitHub Actions UI to verify the commit logic without waiting 24 hours for the scheduled event.

### 2. Job Execution
A single job named `daily-commit` is spun up on an `ubuntu-latest` runner.
It explicitly defines `permissions: contents: write` to ensure the virtual environment has authorization to write commits back to the GitHub tree.

### 3. Step Definition & Tracking
The runner utilizes `actions/checkout@v4` to pull down the repository code. 
A subsequent shell step is explicitly named `Track daily activity for your-student-id` to fulfill the rubric requirements. This step evaluates a bash command to echo a timestamped daily activity log into a file named `activity_log.txt`.

### 4. Git configuration and Push
The final step configures the global git user inside the runner instance to masquerade as the `github-actions[bot]`. It then executes the standard git staging sequence (`git add`, `git commit -m`) to record the modified `activity_log.txt` and completes the pipeline with `git push` to upload the newly generated commit to the main branch.

---

## Code Configuration (`daily-commit.yml`)

```yaml
name: Daily DevSync Commit
on:
  schedule:
    - cron: '30 12 * * *'
  workflow_dispatch:

jobs:
  daily-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write 
      
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Track daily activity for your-student-id
        run: |
          echo "Daily automated activity logged at $(date)" >> activity_log.txt

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add activity_log.txt
          git commit -m "Automated daily activity log update" || echo "No changes to commit"
          git push
```

---

## Verification

To verify the integration:
1. Navigate to the **Actions** tab inside the target GitHub repository.
2. Select **Daily DevSync Commit** from the left-nav menu.
3. Click **Run workflow** -> **Run workflow** to invoke the manual `workflow_dispatch` trigger.
4. Open the Actions run execution and ensure that the runner successfully processes the `Track daily activity for your-student-id` step.
5. Return to the root of the repository and verify that `activity_log.txt` was successfully populated and committed by the `github-actions[bot]` within the last few minutes.
