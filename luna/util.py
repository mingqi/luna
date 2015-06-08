
from docopt import docopt, DocoptExit


def parse_run_cli(args):
    doc = """
Usage: run [--attach=ATTACH]... 
                 [--dns=DNS]... 
                 [--dns-search=DNS]... 
                 [--env=ENV]...
                 [env-file=ENVFILE]...
                 [--expose=EXPOSE]...
                 [--link=LINK]...
                 [--lxc-conf=LXCCONF]...
                 [--publish=PUBLISH]...
                 [--volume=VOLUME]...
                 [--volumes-from=]...
                 [options] IMAGE [CMD ...]


Options:
    -a --attach=ATTACH
    -c --cpu-shares=CPU
    --cidfile=CIDFILE
    --cpuset=CPUSET
    -d
    --detach=DETACH
    --dns=DNS
    --dns-search=DNSSEARCH
    -e --env=ENV
    --entrypoint=ENTRYPOINT
    --env-file=ENVFILE
    --expose=EXPOSE
    -h --hostname=HOSTNAME
    -i
    --interactive=INTERACTIVE
    --link=LINK
    --lxc-conf=LXC
    -m --memory=MEMORY
    --name=NAME
    --net=NET
    -P
    --publish-all=PUBLISHALL
    -p --publish=PUBLISH
    --privileged=PRIVILEGED
    --rm=RM
    --sig-proxy=PROXY
    -t
    --tty=TTY
    -u --user=USER
    -v --volume=VOLUME
    --volumes-from=VOLUMES
    -w --workdir=WORKDIR
    """
    try:
        return docopt(doc, args, help=False, version=None)
    except DocoptExit:
        raise Exception('failed to parse docker run arguments')
