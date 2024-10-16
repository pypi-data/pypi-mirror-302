# Get in Touch!

You have found a bug in energy-tools or have a suggestion for a new functionality? Then get in touch with us by opening up an issue on the energy-tools issue board to discuss possible new developments with the community and the maintainers.

# Setup your git repository

**Note**: *The following setup is just a suggestion of how to setup your repository and is supposed to make contributing easier, especially for newcomers. If you have a different setup that you are more comfortable with, you do not have to adopt this setup.*

If you want to contribute for the first time, you can set up your environment like this:

1. If you have not done it yet: install git and create a GitLab account;
2. Create a fork of the official energy-tools repository by clicking on "Fork" in the official energy-tools repository;
3. Clone the forked repository to your local machine:

```
git clone https://gitlab.com/YOUR-USERNAME/energy-tools.git
```

4. Copy the following configuration at the bottom of to the energy-tools/.git/config file (the .git folder is hidden, so you might have to enable showing hidden folders) and insert your github username:

```
[remote "origin"]
    url = https://gitlab.com/YOUR-USERNAME/energy-tools.git
    fetch = +refs/heads/*:refs/remotes/origin/*
    pushurl = https://gitlab.com/YOUR-USERNAME/energy-tools.git
[remote "upstream"]
    url = https://gitlab.com/miek770/energy-tools.git
    fetch = +refs/heads/*:refs/remotes/upstream/*
[branch "develop"]
    remote = origin
    merge = refs/heads/develop
```

The develop branch is now configured to automatically track the official energy-tools develop branch. So if you are on the develop branch and use:

```
git fetch upstream
git merge upstream/develop
```

your local repository will be updated with the newest changes in the official energy-tools repository.

Since you cannot push directly to the official energy-tools repository, if you are on develop and do:

```
git push
```

your push is by default routed to your own fork instead of the official energy-tools repository with the setting as defined above.

# Contribute

All contributions to the energy-tools repository are made through merge requests to the develop branch. You can either submit a merge request from the develop branch of your fork or create a special feature branch that you keep the changes on. A feature branch is the way to go if you have multiple issues that you are working on in parallel and want to submit with seperate merge requests. If you only have small, one-time changes to submit, you can also use the develop branch to submit your merge request.

If you wish to submit a merge request for discussion, i.e. which isn't ready to be merged, add [WiP] in the title to let others know. The title can be renamed later, once the changes are ready to be merged.

**Note**: *The following guide assumes the remotes are set up as described above. If you have a different setup, you will have to adapt the commands accordingly.*

## Contribute from your develop branch

1. Check out the develop branch on your local machine:

```
git checkout develop
```

2. Update your local copy to the most recent version of the energy-tools develop branch:

```
git fetch upstream
git merge upstream/develop
```

3. Make changes in the code;

4. Add and commit your changes:

```
git add --all
git commit -m "commit message"
```

5. [Black (the uncompromising Python code formatter)](https://black.readthedocs.io/en/stable/) is used in a pre-commit hook to automatically reformat all code prior to any commit. If Black modifies any file when `git commit` is executed, you need to run `git commit` again to proceed with the commit and Black's changes. **Running Black as a pre-commit hook is not optional**;

6. If there is an open issue that the commit belongs to, reference the issue in the commit message, for example for issue 3:

```
git commit -m "commit message #3"
```

7. Push your changes to your fork:

```
git push
```

8. Put in a merge request to the main repository: [https://docs.gitlab.com/ee/gitlab-basics/add-merge-request.html](https://docs.gitlab.com/ee/gitlab-basics/add-merge-request.html);

9. If you want to amend the merge request (for example because the community/maintainers have asked for modifications), simply push more commits to the branch:

```
git add --all
git commit -m "I have updated the pull request after discussions #3"
git push
```

   The pull request will be automatically updated.

## Contribute from a feature branch

**To be developped**

# Test Suite

energy-tools uses pytest for automatic software testing.

## Making sure you don't break anything

If you make changes to energy-tools that you plan to submit, first make sure that all tests are still passing. You can do this locally with:

```
make tests
```

## Adding Tests for new functionality

If you have added new functionality, you should also add a new function that tests this functionality. pytest automatically detects all functions in the energy-tools/tests folder that start with 'test_' and are located in a file that also starts with 'test_' as relevant test cases.
