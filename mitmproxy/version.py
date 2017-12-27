import os
import subprocess

VERSION = "3.0.0"
PATHOD = "pathod " + VERSION
MITMPROXY = "mitmproxy " + VERSION

# Serialization format version. This is displayed nowhere, it just needs to be incremented by one
# for each change in the file format.
FLOW_FORMAT_VERSION = 5


def get_version(dev: bool = False, build: bool = False, refresh: bool = False) -> str:
    mitmproxy_version = VERSION

    if "dev" in VERSION and not refresh:
        pass  # There is a hardcoded build tag, so we just use what's there.
    elif dev or build:
        here = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        try:
            git_describe = subprocess.check_output(
                ['git', 'describe', '--tags', '--long'],
                stderr=subprocess.STDOUT,
                cwd=here,
            )
            last_tag, tag_dist, commit = git_describe.decode().strip().rsplit("-", 2)
            commit = commit.lstrip("g")[:7]
            tag_dist = int(tag_dist)
        except Exception:
            pass
        else:
            # Remove current suffix
            mitmproxy_version = mitmproxy_version.split(".dev")[0]

            # Add suffix for non-tagged releases
            if tag_dist > 0:
                mitmproxy_version += ".dev{tag_dist:04}".format(tag_dist=tag_dist)
                # The wheel build tag (we use the commit) must start with a digit, so we include "0x"
                mitmproxy_version += "-0x{commit}".format(commit=commit)

    if not dev:
        mitmproxy_version = mitmproxy_version.split(".dev")[0]
    elif not build:
        mitmproxy_version = mitmproxy_version.split("-0x")[0]

    return mitmproxy_version


if __name__ == "__main__":
    print(VERSION)
