#!/usr/bin/env bash
# budget.sh LIMIT -- how much of its `timeout-minutes` this job has used, as a warning before it is a failure.
#
# A job cut off at its limit commits nothing, records nothing, and its log stops mid-line; the suite job was
# cancelled that way four times in October, at 30 minutes and then at 80, each time the first sign that it had
# outgrown its limit. Growth is gradual -- the daily went from 68 to 96 minutes of 180 as the atlas grew -- so
# the useful signal is the trend, a run or two before the limit, not the run that hits it. This prints the
# figure on every run and warns from 75%, which is the moment to raise the limit or split the job, not after.
#
# Reads JOB_START (epoch seconds), which each job's first step writes to $GITHUB_ENV. LIMIT is passed rather
# than read from the API so the number is the one in the same file, next to `timeout-minutes`, and
# `tests/ci_tools_test.py` asserts the two agree.
set -uo pipefail
limit="$1"
start="${JOB_START:-}"
if [ -z "$start" ]; then
  echo "JOB_START is not set, so the time used is unknown: the job's first step should set it"
  exit 0
fi
used=$(( ($(date +%s) - start + 59) / 60 ))
pct=$(( used * 100 / limit ))
line="This job used ${used} of its ${limit} minutes (${pct}%)."
echo "$line"
if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then echo "$line" >> "$GITHUB_STEP_SUMMARY"; fi
if [ "$pct" -ge 75 ]; then
  echo "::warning title=Close to the time limit::${line} A job cut off at its limit publishes and records nothing; raise timeout-minutes or split the job before it is reached (handbook/ci-cd.md)."
fi
exit 0
