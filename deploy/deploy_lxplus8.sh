#!/bin/bash
# recast-atlas v0.1.8

# Setup Python virtual environment and install recast-atlas and requirements
python3 -m venv ~recast/public/recast-atlas-0.1.8
. ~recast/public/recast-atlas-0.1.8/bin/activate
python -m pip install --upgrade pip 'setuptools<58.0.0' wheel  # c.f. https://github.com/reanahub/reana-client/issues/558
python -m pip install --requirement ~recast/deploy/recast-atlas-0.1.8-requirements.txt

# Use heredoc syntax to generate public environment setup script
cat << EOF > ~recast/public/setup_0.1.8.sh
#!/bin/bash

export RECAST_DEFAULT_RUN_BACKEND=local
export RECAST_DEFAULT_BUILD_BACKEND=kubernetes
export PACKTIVITY_CONTAINER_RUNTIME=singularity
export SINGULARITY_CACHEDIR="/tmp/\$(whoami)/singularity"
mkdir -p "\${SINGULARITY_CACHEDIR}"

# https://twitter.com/lukasheinrich_/status/1021398718996713475
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

. ~recast/public/recast-atlas-0.1.8/bin/activate

\$(recast catalogue add /eos/project/r/recast/atlas/catalogue)
export KUBECONFIG=/eos/project/r/recast/atlas/cluster/clusterconfig
export PATH="\${PATH}:~recast/public/bin"
EOF

# Link public setup script to this version
ln --symbolic --force ~recast/public/setup_0.1.8.sh ~recast/public/setup.sh
