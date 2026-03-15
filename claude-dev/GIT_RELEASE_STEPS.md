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

Create a new branch based on the current `claude-dev` branch and switch to it.

```bash
git checkout -b release-v4 claude-dev
```

This can be confirmed by checking VSCode's lower left corner where it shows the current branch, or by running:

```bash
git branch --show-current
```

### Remove Claude Files From Release Branch

Remove the Claude development files from the release branch using git rm.

```bash
git rm CLAUDE.md
git rm -r claude-dev/
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
