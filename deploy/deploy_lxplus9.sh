#!/bin/bash

# Example usage:
# $ bash deploy_lxplus9.sh 0.3.0
# or to get the latest recast-atlas release by default:
# $ bash deploy_lxplus9.sh

# Ensure that pip can't install outside a venv
export PIP_REQUIRE_VIRTUALENV=true

RECAST_ATLAS_VERSION="${1:-0.0.0}"

if [[ "${RECAST_ATLAS_VERSION}" == "0.0.0" ]]; then
    # `pip index versions` will output the following warning to stderr:
    # WARNING: pip index is currently an experimental command. It may be removed/changed in a future release without prior warning.
    # so direct stderr to /dev/null to avoid this.
    # The next line will be:
    # recast-atlas (x.y.z)
    # so filter out the version number and output that
    RECAST_ATLAS_VERSION=$(python3 -m pip index versions recast-atlas 2> /dev/null | awk -F"[()]" 'NR==1 {print $2}')
fi

# Setup Python virtual environment and install recast-atlas and requirements
python3 -m venv ~recast/public/recast-atlas-"${RECAST_ATLAS_VERSION}"
. ~recast/public/recast-atlas-"${RECAST_ATLAS_VERSION}"/bin/activate

if [[ "${RECAST_ATLAS_VERSION}" == "0.1.8" ]]; then
    # c.f. https://github.com/reanahub/reana-client/issues/558
    python -m pip install --upgrade pip 'setuptools<58.0.0' wheel
else
    python -m pip install --upgrade pip setuptools wheel
fi

# Install the environment from a "lockfile" (just called a requirements.txt by
# pip-tools) generated with pip-tools compile. If the lockfile is missing, make
# compile one with pip-tools.
if [ ! -f ~recast/deploy/recast-atlas-"${RECAST_ATLAS_VERSION}".lock ]; then
    python -m pip install pip-tools
    python -m piptools compile \
        --generate-hashes \
        --output-file ~recast/deploy/recast-atlas-"${RECAST_ATLAS_VERSION}".lock \
        ~recast/deploy/recast-atlas-"${RECAST_ATLAS_VERSION}"-requirements.txt
fi
python -m pip install \
    --no-deps \
    --require-hashes \
    --requirement ~recast/deploy/recast-atlas-"${RECAST_ATLAS_VERSION}".lock

# Use heredoc syntax to generate public environment setup script
cat << EOF > ~recast/public/setup_"${RECAST_ATLAS_VERSION}".sh
#!/bin/bash

export RECAST_DEFAULT_RUN_BACKEND=local
export RECAST_DEFAULT_BUILD_BACKEND=kubernetes
export PACKTIVITY_CONTAINER_RUNTIME=singularity
export APPTAINER_CACHEDIR="/tmp/\${USER}/apptainer"
export SINGULARITY_CACHEDIR="\${APPTAINER_CACHEDIR}"
mkdir -p "\${APPTAINER_CACHEDIR}"

# https://twitter.com/lukasheinrich_/status/1021398718996713475
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

. ~recast/public/recast-atlas-${RECAST_ATLAS_VERSION}/bin/activate

\$(recast catalogue add /eos/project/r/recast/atlas/catalogue)
export KUBECONFIG=/eos/project/r/recast/atlas/cluster/clusterconfig
export PATH="\${PATH}:~recast/public/bin"

echo -e "\n# It is recommended to login to any private container registry now."
echo -e "# Example:\n# apptainer remote login --username \"\${USER}\" docker://gitlab-registry.cern.ch"
EOF

# Link public setup script to this version
ln --symbolic --force ~recast/public/setup_"${RECAST_ATLAS_VERSION}".sh ~recast/public/setup.sh
