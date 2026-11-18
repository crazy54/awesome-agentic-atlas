#!/usr/bin/env bash
# retry.sh N command [args...] -- run a command up to N times, waiting 15 s, then 45 s, then 135 s between tries.
#
# For the steps in the workflows that fail on the network rather than on the code: `pip install`, a `git push`
# that lost a race, a list host answering 502. The fetch stages have their own retry, sized to GitHub's
# GraphQL behaviour (`scripts/02_fetch.py`), and are not wrapped in this -- a second layer would multiply
# their attempts and hide an outage behind an hour of waiting.
#
# Only for commands that are safe to repeat. The status of the last try is the status of the step, and each
# failed try is a `::warning::` in the log, so a step that needed three tries on a green run is still visible.
set -uo pipefail
tries="$1"; shift
wait=15
for ((i = 1; i <= tries; i++)); do
  "$@" && exit 0
  status=$?
  if [ "$i" -lt "$tries" ]; then
    echo "::warning title=Retrying::'$*' exited ${status} (try ${i} of ${tries}); trying again in ${wait}s"
    sleep "$wait"
    wait=$((wait * 3))
  fi
done
echo "::error title=Gave up::'$*' exited ${status} on all ${tries} tries"
exit "$status"
