# Contributing

Everyone is welcome to create a PR with additions / bugfixes. There are some rules.

1. Your PR title and description MUST clearly explain what the PR does.
2. The PR CAN only have one goal. Multiple features / bugfixes ARE NOT allowed.
3. You MUST only change one thing at a time per commit. For example: change a readme. You cannot be changing code and adding stuff to the readme in one commit.
4. In addition to 3., you MUST use conventional commits. If you don't know what they are, please see: https://www.conventionalcommits.org/en/v1.0.0/#specification
5. You must write unit tests (using `pytest`, see examples in `tests`) if you write new code and modify existing unit tests if you are modifying code. Unit tests are not run in CI/CD, you must test everything and makes sure the unit tests pass before pushing. Check the README on how to run the tests.
6. Your PR must be to `dev`. Our main branch is `dev`. Syncs to `main` only happen regularly.
