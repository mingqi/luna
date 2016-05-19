from collections import namedtuple
import string
import re


def _parse_bool(s):
    if s in ['True', 'true']:
        return True
    elif s in ['False', 'false']:
        return False

    raise Exception('%s is not a boolean value' % s)


def _parse_single_option(arg):
    Options = namedtuple('Options', ['type', 'names', 'value'])

    if arg[0] != '-':
        return None

    if arg == '--' or arg == '-':
        print arg
        raise Exception('-- or - must follow a option name')

    if arg[1] != '-':
        for o in arg[1:]:
            if o not in string.lowercase and o not in string.uppercase:
                raise Exception('illegal option %s' % arg)
        return Options(type='short', names=list(arg[1:]), value=None)
    else:
        sp = arg[2:].split('=', 1)
        if len(sp) == 2:
            return Options(type='long', names=[sp[0]], value=sp[1])
        else:
            return Options(type='long', names=[sp[0]], value=None)


def new_options_parser(doc):
    options = dict()
    OptionDefination = namedtuple('OptionDefination', ['name', 'type'])
    for line in doc.splitlines():
        line = line.strip()
        m = re.search('--([^\s=]+)(=(\S+))?', line)
        if not m:
            continue
        if not m.group(3):
            option_type = 'string'
        elif m.group(3).lower() in ['false', 'true']:
            option_type = 'boolean'
        elif m.group(3) == '[]':
            option_type = 'list'
        else:
            option_type = 'string'

        opt_def = OptionDefination(m.group(1), option_type)
        options[opt_def.name] = opt_def

        m = re.search('-([a-zA-Z]),', line)
        if m:
            options[m.group(1)] = opt_def

    def _parser(args):
        result = dict()
        i = 0
        while i < len(args):
            arg = args[i]
            opt = _parse_single_option(arg)
            if not opt:
                break
            must_be_boolean = len(opt.names) > 1
            for name in opt.names:
                opt_def = options.get(name)
                if not opt_def:
                    raise Exception('option %s is not defined' % name)
                if must_be_boolean and opt_def.type != 'boolean':
                    raise Exception('option --%s must be have a value' % opt_def.name)
                if opt_def.type == 'boolean':
                    result[opt_def.name] = _parse_bool(opt.value) if opt.value else True
                else:
                    i = i + 1
                    value = args[i]
                    if opt_def.type == 'list':
                        if opt_def.name not in result:
                            result[opt_def.name] = []
                        result[opt_def.name].append(value)
                    else:
                        result[opt_def.name] = args[i]
            i = i + 1

        return (result, args[i:])

    return _parser

RUN_DOC = """
  -a, --attach=[]            Attach to STDIN, STDOUT or STDERR
  --add-host=[]              Add a custom host-to-IP mapping (host:ip)
  -c, --cpu-shares=0         CPU shares (relative weight)
  --cap-add=[]               Add Linux capabilities
  --cap-drop=[]              Drop Linux capabilities
  --cidfile=""               Write the container ID to the file
  --cpuset-cpus=""           CPUs in which to allow execution (0-3, 0,1)
  -d, --detach=false         Run container in background and print container ID
  --device=[]                Add a host device to the container
  --dns=[]                   Set custom DNS servers
  --dns-search=[]            Set custom DNS search domains
  -e, --env=[]               Set environment variables
  --entrypoint=""            Overwrite the default ENTRYPOINT of the image
  --env-file=[]              Read in a file of environment variables
  --expose=[]                Expose a port or a range of ports
  -h, --hostname=""          Container host name
  --help=false               Print usage
  -i, --interactive=false    Keep STDIN open even if not attached
  --ipc=""                   IPC namespace to use
  --link=[]                  Add link to another container
  --log-driver=""            Logging driver for container
  --lxc-conf=[]              Add custom lxc options
  -m, --memory=""            Memory limit
  -l, --label=[]             Set metadata on the container (e.g., --label=com.example.key=value)
  --label-file=[]            Read in a file of labels (EOL delimited)
  --mac-address=""           Container MAC address (e.g. 92:d0:c6:0a:29:33)
  --memory-swap=""           Total memory (memory + swap), '-1' to disable swap
  --name=""                  Assign a name to the container
  --net="bridge"             Set the Network mode for the container
  -P, --publish-all=false    Publish all exposed ports to random ports
  -p, --publish=[]           Publish a container's port(s) to the host
  --pid=""                   PID namespace to use
  --privileged=false         Give extended privileges to this container
  --read-only=false          Mount the container's root filesystem as read only
  --restart="no"             Restart policy (no, on-failure[:max-retry], always)
  --rm=false                 Automatically remove the container when it exits
  --security-opt=[]          Security Options
  --sig-proxy=true           Proxy received signals to the process
  -t, --tty=false            Allocate a pseudo-TTY
  -u, --user=""              Username or UID (format: <name|uid>[:<group|gid>])
  -v, --volume=[]            Bind mount a volume
  --volumes-from=[]          Mount volumes from the specified container(s)
  -w, --workdir=""           Working directory inside the container
"""
run = new_options_parser(RUN_DOC)
