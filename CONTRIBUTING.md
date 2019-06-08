# Contributing to Andrometa
Thank you for taking time to contribute to our Community and most importantly our project. We value every contribution and it means a lot for us. 

Please remember to read the following guide to learn more about how we care to make our repos look clean.

# Style
 * Start comments with a Uppercase letter.
 * Document your code! Seriously, how else are we supposed to know what are you doing?
 * Indentation - 2 spaces
 * Encoding - UTF8
 * Newline - LF

# Branch naming
  * For feature branches - feat/issuenumber-branch-name
  * For bugfixes - bug/issuenumber or fix/issuenumber
  * For chores (updating dependencies, etc...) - chore/issuenumber-update-dependencies, for example

# Commit naming
   * First of all - a pull request to a bugfix should consist of one commit. Nobody likes thousands of commits, which actually worsen repo view and make navigating commits a lot harder. Use `git commit --amend, git push --force`
   * Start a commit with issue#. Example: #123: Fixes incorrect naming of variable
   * No pointless commit messages.
   * First line of the commit - 80 chars
   * You may also post the extended commit message. First a short line, then an empty line, then your extended commit message

# Merging
* Merging into Master is disabled. In order to do so you have to have at least one approved review and the tests to pass. 

# What should a PR consist of:
* Solves the bug / implements a feature correctly
* No failed tests
* Has unit tests
* Does not worsen test coverage

Have fun and enjoy hacking!
