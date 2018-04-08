This repository keeps track of my cross-platform development environment.

The configuration files can be linked into their correct location using
the `link-config.py` script.

**Notes for Windows** &ndash; You need elevated privileges to create symlinks
on Windows. If the administrator user is a different user, set the `USERPROFILE`
environment variable to your home directory before running the script.

## Reference

### GPG on Windows

1. Install from https://gnupg.org/download/, do **not** select Gpg4win,
   but instead the "Simple installer for the current GnuPG"
2. Make sure to set up your `PATH` to prefer the `gpg` from the just
   installed version of GnuPG instead of `gpg` from GitForWindows.
3. `git config --global gpg.program 'C:\Program Files (x86)\gnupg\bin\gpg.exe'`
4. `gpgconf --list-dirs` to find the home directory of your GPG installation
5. Go into the homedir directory and add `gpg-agent.conf`, check the reference
   file in the `config/` directory for config values.
6. `gpgconf --reload gpg-agent`

> *To do* GPG also supports acting as an SSH agent with the
> `enable-ssh-support`, effectively allowing you to use your GPG key
> as an SSH key. Unfortunately, the Git for Windows OpenSSH client is
> not compatible with the GPG ssh-agent because of how they treat the
> `SSH_SOCK_AUTH` and `SSH_AGENT_PID` environment variables.
>
> Otherwise, we could use this in `.profile`:
>
> ```
> function __gpg_homedir {
>     if [[ "$(gpgconf --list-dirs)" =~ homedir:(.*) ]];
>     then
>         echo ${BASH_REMATCH[1]/\%3a/:}
>         return 0
>     else
>         return 1
>     fi
> }
> 
> function __gpg_ssh_port {
>     data="$(cat $(__gpg_homedir)/S.gpg-agent.ssh)"
>     if [[ "$data" =~ ^([0-9]+) ]];
>     then
>         echo ${BASH_REMATCH[1]}
>         return 0
>     else
>         return 1
>     fi
> }
>
> export SSH_AUTH_SOCK=$(__gpg_homedir)\\S.gpg-agent.ssh
> export SSH_AUTH_PORT=$(__gpg_ssh_port)
> ```
