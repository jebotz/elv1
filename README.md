This is my solution to Part 1.

To use this in another repo, copy the following files to your repo:
```
make-release-branch.py
.github/workflows/autobranch.yml
```

and create a file called `VERSION` containing only the semver string.

To schedule the creation of release branches we need to adjust two
parameters... one is the cron-style schedule in the action YAML file,
and the other is the minimum desired number of days between releases
which is passed as a command-line parameter to the python script.  This
is necessary if we want to be able to say "make a release every 3 weeks",
because the cron-style schedule doesn't have a way of specifying this,
so instead we schedule the script to run on a specific weekday and let
the script decide if it's time for a release yet.
