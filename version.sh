#!/bin/sh

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

# This script prints version information for a project managed with Git when
# executed in a shell. It works from checked-out repositories or downloaded
# archives alike. For more information see https://github.com/ansemjo/version.sh

# -- SYNOPSIS -- Copy this script to your project root and add the line
# 'version.sh export-subst' to your .gitattributes file, creating it if it does
# not exist. Commit both files, try running 'sh ./version.sh' and use annotated
# Git tags to track your versions.

# Ignore certain shellcheck warnings:
# - '$Format..' looks like a variable in single-quotes but this is
#     necessary so it does _not_ expand when interpreted by the shell
# - backslash before a literal newline is a portable way
#     to insert newlines with sed
# shellcheck disable=SC2016,SC1004

# Magic! These strings will be substituted by 'git archive':
COMMIT='$Format:%H$'
REFS='$Format:%D$'

# Fallback values:
FALLBACK_VERSION='commit'
FALLBACK_COMMIT='unknown'

# Revision and commit hash seperators in 'describe' string:
REVISION_SEPERATOR="${REVISION_SEPERATOR:--}"
COMMIT_SEPERATOR="${COMMIT_SEPERATOR:--g}"

# Check if variables contain substituted values?
subst() { test -n "${COMMIT##\$Format*}" && test -n "${REFS##\$Format*}"; }

# Check if git and repository information is available?
hasgit() {
  command -v git >/dev/null && { test -r .git || git rev-parse 2>/dev/null; };
}

# Parse the %D reflist in $REFS to get a tag or branch name:
refparse() {
  # try to find a tag:
  tag=$(echo "$REFS" | sed -ne 's/.*tag: \([^,]*\).*/\1/p');
    test -n "$tag" && echo "$tag" && return 0;
  # try to find a branch name:
  branch=$(echo "$REFS" | sed -e 's/HEAD -> //' -e 's/, /\
/' | sed -ne '/^[a-z0-9._-]*$/p' | sed -n '1p');
    test -n "$branch" && echo "$branch" && return 0;
  # nothing found, no tags and not a branch tip?
  return 1;
}

# Try to get commit and version information with git:
gitcommit() {
  hasgit && git describe --always --abbrev=0 --match '^$' --dirty;
}
gitversion() {
  hasgit && {
    {
      # try to use 'describe':
      V=$(git describe --tags 2>/dev/null) && \
      echo "$V" | sed 's/-\([0-9]*\)-g.*/'"$REVISION_SEPERATOR"'\1/';
    } || {
      # or count the number of commits otherwise:
      C=$(git rev-list --count HEAD) && \
      printf '0.0.0%s%s' "$REVISION_SEPERATOR" "$C";
    };
  };
}

# Wrappers to return version and commit (substituted -> git info -> fallback):
version() { subst && refparse || gitversion || echo "$FALLBACK_VERSION"; }
commit()  { subst && echo "$COMMIT" || gitcommit || echo "$FALLBACK_COMMIT"; }
describe() { printf '%s%s%.7s\n' "$(version)" "$COMMIT_SEPERATOR" "$(commit)"; }

# Parse commandline argument:
case "$1" in
  version)  version ;;
  commit)   commit ;;
  describe) describe ;;
  json)
    printf '{"version":"%s","commit":"%s","describe":"%s"}\n' \
      "$(version)" "$(commit)" "$(describe)" ;;
  help)
    printf '%s [version|commit|describe|json]\n' "$0" ;;
  *)
    printf 'version : %s\ncommit  : %s\n' "$(version)" "$(commit)" ;;
esac
