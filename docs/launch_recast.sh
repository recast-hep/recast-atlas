function launch_recast(){
    def=test
    wrk=$(realpath ${1:-$def})
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v $wrk:/work -e PACKTIVITY_WORKDIR_LOCATION=/work:$wrk recast/recast-atlas-preptool:latest bash
}
