"""Increment version and make release branch."""


import os
import sys
from datetime import datetime

from github import Github

import semver

# Filename of file containing current version
VERSION_FN = 'VERSION'

# See if number of days between releases was given as argument
if len(sys.argv) > 1:
    release_days = int(sys.argv[1])
else:
    release_days = 0

# print(f"token={os.environ['GITHUB_TOKEN']}")
# print(f"repo={os.environ['GITHUB_REPO']}")
gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo(os.environ['GITHUB_REPO'])

with open(VERSION_FN, 'r') as version_file:
    ver = semver.VersionInfo.parse(version_file.read())

# If a argument was given then check if it's been more than
# that number of days since last release and exit without doing
# anything if so.
if release_days > 0:
    old_branch_name = f"release/{ver}"
    try:
        branch = repo.get_branch(branch=old_branch_name)
    except:
        branch = None
    # print(f"branch={branch}")

    # Only need to check if there was in fact an old branch, if not
    # we'll just continue and create one.
    if branch:
        commit = repo.get_commit(sha=branch.commit.sha)
        last_rel_dt = commit.commit.committer.date
        now_dt = datetime.now()
        timediff = last_rel_dt - now_dt
        if timediff.days < release_days:
            print("Not yet time for a release.")
            sys.exit(0)

# Bump the minor version
ver.bump_minor()
branch_name = f"release/{ver}"

# Create the branch
head = repo.get_commit('HEAD')
repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=head.commit.sha)

# Write out the new version
version_file = open(VERSION_FN, 'w')
version_file.write(f"{ver}")
version_file.close()
