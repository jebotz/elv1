This is my solution to Part 1.

To use this in another repo, copy the following files to  the same
locations in your repo:
```
make-release-branch.py
.github/workflows/autobranch.yml
```
and create a file called `VERSION` containing only the semver string
representing the current version of your project.

To schedule the creation of release branches we need to adjust two
parameters... one is the cron-style schedule in the workflow YAML file
(see comments in that file for more info), and the other is the minimum
desired number of days between releases which is passed as a
command-line parameter to the python script (which can also be changed
in the YAML file). This is necessary if we want to be able to say things
like "make a release every 3 weeks", because the cron-style schedule
doesn't have a way of specifying this, so instead we schedule the script
to run on a specific weekday and let the script decide if it's time for
a release yet.

The `make-release-branch.py` script can also be run manually for
testing. To do so set the environment variables `REPO_NAME` and
`GITHUB_TOKEN` to the repo you want to run it on (ghuser/repo), and 
a personal access token respectively. There must be a file named
`VERSION` containing a semver compatible version at the top level of
the repo.

