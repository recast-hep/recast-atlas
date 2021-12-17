#!/bin/bash

# Example usage:
# $ bash deploy_lxplus8.sh 0.1.9
# or to get the latest recast-atlas release by default:
# $ bash deploy_lxplus8.sh

# Ensure that pip can't install outside a venv
export PIP_REQUIRE_VIRTUALENV=true

# Ensure local virtualenv setup
if [ ! -f "${HOME}/opt/venv/bin/virtualenv" ]; then
    curl -sL --location --output /tmp/virtualenv.pyz https://bootstrap.pypa.io/virtualenv.pyz
    python3 /tmp/virtualenv.pyz ~/opt/venv
    ~/opt/venv/bin/pip install --upgrade pip
    ~/opt/venv/bin/pip install virtualenv
    mkdir -p ~/bin  # Ensure exists if new machine
    ln -s ~/opt/venv/bin/virtualenv ~/bin/virtualenv
fi

RECAST_ATLAS_VERSION="${1:-0.0.0}"

if [[ "${RECAST_ATLAS_VERSION}" == "0.0.0" ]]; then
    # LXPLUS8 has an ancient version of pip, so need to create a virtual environment
    # to bootstrap into a useable version and use virtualenv as it is significantly
    # faster
    virtualenv --quiet __venv__
    . __venv__/bin/activate
    python -m pip --quiet install --upgrade pip

    # `pip index versions` will output the following warning to stderr:
    # WARNING: pip index is currently an experimental command. It may be removed/changed in a future release without prior warning.
    # so direct stderr to /dev/null to avoid this.
    # The next line will be:
    # recast-atlas (x.y.z)
    # so filter out the version number and output that
    RECAST_ATLAS_VERSION=$(python -m pip index versions recast-atlas 2> /dev/null | awk -F"[()]" 'NR==1 {print $2}')

    # cleanup
    deactivate
    rm -r __venv__
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
python -m pip install --requirement ~recast/deploy/recast-atlas-"${RECAST_ATLAS_VERSION}"-requirements.txt

# Use heredoc syntax to generate public environment setup script
cat << EOF > ~recast/public/setup_"${RECAST_ATLAS_VERSION}".sh
#!/bin/bash

export RECAST_DEFAULT_RUN_BACKEND=local
export RECAST_DEFAULT_BUILD_BACKEND=kubernetes
export PACKTIVITY_CONTAINER_RUNTIME=singularity
export SINGULARITY_CACHEDIR="/tmp/\$(whoami)/singularity"
mkdir -p "\${SINGULARITY_CACHEDIR}"

# https://twitter.com/lukasheinrich_/status/1021398718996713475
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

. ~recast/public/recast-atlas-${RECAST_ATLAS_VERSION}/bin/activate

\$(recast catalogue add /eos/project/r/recast/atlas/catalogue)
export KUBECONFIG=/eos/project/r/recast/atlas/cluster/clusterconfig
export PATH="\${PATH}:~recast/public/bin"
EOF

# Link public setup script to this version
ln --symbolic --force ~recast/public/setup_"${RECAST_ATLAS_VERSION}".sh ~recast/public/setup.sh
