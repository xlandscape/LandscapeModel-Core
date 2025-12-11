# Contributing

Contributions to the project are welcome. Please contact the authors. These contribution notes refer to the general
Landscape Model contribution guidelines and were written on 2025-12-11.

## Issues

Whenever you identify a bug or like to suggest an enhancement to the code, please file an issue. Stick to the following
checklist when submitting an issue.

1. Check whether a similar issue already exists. If so, please comment on the existing issue instead of creating a new
   one.
2. Identify the most appropriate repository for the issue, that is the repository nearest to the presumed code changes.
   For instance, if you found a bug in the base classes, please submit it in the Landscape Model core repository or an
   enhancement of a specific component in the component's repository. If you are not sure about the most appropriate
   repository, please use the top level repository of the according model variant, e.g., xAquaticRisk or
   xOffFieldSoilRisk.
3. Give the issue a strong, self-explanatory title.
4. Provide any information in the issue's description that is needed to understand the purpose of the issue and allows
   working on it. This includes a rationale, excerpts of log files, screenshots etc. Be concise.
5. If you are going to work on the issue yourself, assign the issue to you. In any other case, assign the issue to the
   repository owner.
6. Assign one of the following labels to the issue: `bug` if the issue is related to exceptions or erroneous runtime
   behavior, `documentation` for issues related with the documentation of functionality and code, `enhancement` for
   code improvements that add to the usability or performance, or `suggestion` for ideas that should be considered part
   of the backlog or require further discussion.
7. In the case of a `bug` issue, you may additionally assign the `highPriority` label if the bug is breaking the normal
   usage of the application.
8. Whenever you start working on an issue, you should assign the label `Work in progress` to it to communicate that the
   issue is actively addressed. Likewise, if you finish work on an issue, the label `work in progress` should be
   removed before closing the issue.
9. If an issue requires additional input or is delayed for future work actions, you can mark it with the label
   `Waiting`.
10. In case another issue is blocking the work on an issue or if two issues are otherwise related, please actively link
    the issues using the according GitLab options.

## Merge requests

The Landscape Model repositories adapt the GitFlow approach for versioning (see
[A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) for a detailed
explanation). Briefly, there is a *master* branch that always contains the latest tested stable version (tagged with a
version number). This branch is protected and only the repository owner can push to it. To contribute to the repository,
please adhere to the following steps:

1. Locally, create a new branch starting at the newest commit of the master branch. You should do all your coding and
   modifications in this feature branch.
2. Develop in your local feature branch until you reach a state that you like to submit. This may encompass multiple
   local commits.
3. Use concise and meaningful commit messages that help to track changes.
4. If the repository gets updated during your development, please merge the new master commit into your feature branch
   and resolve merge conflicts, if any occur.
5. Make sure that all your changes are reflected in the repositories documentation and modify the documentation if
   needed.
6. Do not assign new version numbers. This will be done during the next release of the repository.
7. Test your code extensively!
8. If your code works satisfyingly, push your local feature branch to the GitLab repository.
9. Create then a merge request for your pushed branch (= source branch) into the master branch.
10. Assign the owner of the repository to the merge request.
11. Your changes will be reviewed by the owner of the repository and the merge will be performed, or you may be asked
    for additional modifications of your code.

## Components

If you are requesting a merge containing component code, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The repository can be cloned from GitLab.
- [ ] The component runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.
- [ ] You haven't introduced inputs to the component that are not needed for calculations.

## Model variant

If you are requesting a merge relating to a model variant, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The entire model, including all submodules, can be cloned from GitLab.
- [ ] The model runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.

## Scenario

If you are requesting a merge relating to a scenario, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The repository can be cloned from GitLab.
- [ ] The component runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.
- [ ] Added data is required, cannot be retrieved by a component and is not redundant.

