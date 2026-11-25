# Wiki publishing

The source of these pages is the root [wiki directory](https://github.com/RuchirChawdhry/copier-python-cli/tree/main/wiki), outside the Copier-rendered template.

Edit the Markdown files in the source repository. The Publish wiki workflow runs on main-branch pushes that touch wiki pages or the publishing workflow; it can also be run manually from the Actions tab. Only main can publish. The publisher copies top-level Markdown pages into the existing GitHub wiki repository, commits changes and pushes normally. It does not force-push or delete other pages. A page with the same filename is replaced by the source version; edit managed pages in the source repository, not the wiki UI. Removing a source page does not delete its previously published counterpart.

## First run

Enable Wikis in the repository settings and create an initial Home page through the GitHub wiki UI if one does not exist. GitHub requires an initial page before the wiki can be cloned.

The workflow uses the built-in job token with contents: write by default. An explicitly configured WIKI_TOKEN takes precedence. If the token cannot push to the wiki, configure a repository Actions secret named WIKI_TOKEN with a Git credential authorized to write that wiki, then rerun. Keep the token in Actions secrets, never in a file or commit. A classic personal access token with public_repo scope is an option for this public repository; set an expiration and revoke it when no longer needed.

Verify a successful run in [Actions](https://github.com/RuchirChawdhry/copier-python-cli/actions/workflows/publish-wiki.yml) and inspect the [published wiki](https://github.com/RuchirChawdhry/copier-python-cli/wiki). Repeated runs with identical sources should make no new commit.

The local workflow is a thin caller of the central [wiki-publish.yml](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/wiki-publish.yml) reusable workflow. Publishing logic and its tests live in ci-workflows. See the [central setup guide](https://github.com/RuchirChawdhry/ci-workflows/blob/main/docs/wiki-publish.md). Neither the caller nor the wiki directory is copied into generated projects.
