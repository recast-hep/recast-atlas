function recast_shell_vol(){
    vol=${1:-recastdata}
    docker volume create $vol > /dev/null
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v $vol:/work -e PACKTIVITY_WORKDIR_LOCATION=/work:$(docker volume inspect $vol -f '{{.Mountpoint}}') recast/recast-atlas-preptool:latest bash
}

function recast_shell(){
    def=$PWD
    wrk=$(realpath ${1:-$def})
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v $wrk:/work -e PACKTIVITY_WORKDIR_LOCATION=/work:$wrk recast/recast-atlas-preptool:latest bash
}

function recast_run(){
    wrk=$(realpath ${1})
    analysis=${2}
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $wrk:/work -e PACKTIVITY_WORKDIR_LOCATION=/work:$wrk recast/recast-atlas-preptool:latest recast run $analysis
}

