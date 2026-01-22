# Process for Updating Main

## Command Summary

### Push claude-dev Branch Updates

```bash
git push
```

### Tag claude-dev Branch For Release

List the tags for the branch using 

```bash
git tag
```

Increment the version number and set the tag using 

```bash
git tag dev-v4
```

Push the new tag using

```bash
git push origin --tags
```

### Create Release Branch

Using GitHub-Desktop select the 'Current Branch' menu.. Click the 'New Branch' button and create a new branch named `release-v4` (increment number) based on the `claude-dev` branch. Once created, GitHub-Desktop will automatically switch the repo to this branch. This can be confirmed by watching VSCode's lower left corner where it shows the current branch.

### Remove Claude Files From Release Branch

Manually delete the files in file explorer. Then, remove the git references using the following commands.

```bash
git rm claude.md
git rm docs/PLAN.md
git rm docs/RESUME.md
git rm docs/ARCHITECTURE.md
git rm docs/VIBE_HISTORY.md
git rm docs/GIT_RELEASE_STEPS.md
```

Commit this branch update

```bash
git commit -m "Remove Claude development files for release"
```

### Set Main to Release Branch

Check out the `main` branch

```bash
git checkout main
```

Perform a hard reset of the `main` branch to the new release branch

```bash
git reset --hard release-v4
```

Push new `main` branch, it has to be forced.

```bash
git push origin main --force
```

### Clean Up

Delete Release Branch

```bash
git branch -d release-v4
```

Return to the `claude-dev` branch to continue work

```bash
git checkout claude-dev
```


## Example Run

```bash
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git push
Enumerating objects: 14, done.
Counting objects: 100% (14/14), done.
Delta compression using up to 2 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 20.71 KiB | 2.07 MiB/s, done.
Total 8 (delta 6), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (6/6), completed with 6 local objects.
To https://github.com/cutaway-security/click-plc-scanner.git
   9d6f8cb..dc57c24  claude-dev -> claude-dev
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git tag dev-v4
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git push origin --tags
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/cutaway-security/click-plc-scanner.git
 * [new tag]         dev-v4 -> dev-v4
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git rm claude.md
rm 'claude.md'
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git rm docs/PLAN.md
rm 'docs/PLAN.md'
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git rm docs/RESUME.md
rm 'docs/RESUME.md'
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git rm docs/ARCHITECTURE.md 
rm 'docs/ARCHITECTURE.md'
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git rm docs/VIBE_HISTORY.md 
rm 'docs/VIBE_HISTORY.md'
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git commit -m "Remove Claude development files for release"
[release-v4 8aac24e] Remove Claude development files for release
 5 files changed, 3117 deletions(-)
 delete mode 100644 claude.md
 delete mode 100644 docs/ARCHITECTURE.md
 delete mode 100644 docs/PLAN.md
 delete mode 100644 docs/RESUME.md
 delete mode 100644 docs/VIBE_HISTORY.md
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git reset --hard release-v4
HEAD is now at 8aac24e Remove Claude development files for release
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git push origin main --force
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 2 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 324 bytes | 162.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/cutaway-security/click-plc-scanner.git
 + 8080558...8aac24e main -> main (forced update)
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git branch -d release-v4
Deleted branch release-v4 (was 8aac24e).
(PyEnv) cutaway@ubuntu:~/Development/click-plc-scanner$ git checkout claude-dev
Switched to branch 'claude-dev'
Your branch is up to date with 'origin/claude-dev'.
```