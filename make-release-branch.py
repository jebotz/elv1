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
ver = ver.bump_minor()
branch_name = f"release/{ver}"

# Write out the new version... this writes directly to the HEAD of
# the upstream repo at github.  Need to do this before making the
# branch so the new version is reflected in both places.
ver_file_contents = repo.get_contents(VERSION_FN, ref='HEAD')
repo.update_file(ver_file_contents.path, f"{ver}", f"{ver}",
                 ver_file_contents.sha, branch='main')

# Create the branch
head = repo.get_commit('HEAD')
repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=head.commit.sha)

# Pull to update the local clone; this shouldn't hurt when run from
# workflow and is a good thing when run manually
os.system("git pull")
