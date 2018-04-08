
# Cmder always starts up in its application directory, thus we set
# this environment variable to automatically switch to it.
if [ ! -z "$CDFROMPROFILE" ]; then
  cd ~
  unset CDFROMPROFILE
fi

export PYTHONDONTWRITEBYTECODE=x
export PIPENV_VENV_IN_PROJECT=x

# ==================================================================
# Automatic switch to $HOME
# Starting from Windows Taskbar enters at /
# ==================================================================

if [ "$(pwd)" == "/" ]; then
    echo ".profile: You would start at root, switching to home"
    cd ~
fi

# =================================================================
# PATH
# =================================================================

if [ "$(uname)" == "Darwin" ]; then
  export PATH=${PATH}:"~/Library/Python/3.6/bin"
  export PATH=${PATH}:"/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
elif [ "$(uname)" == "Linux" ]; then
  export PATH=${PATH}
else
  if [ -z "$NEXTCLOUD" ]; then
    echo "warning: NEXTCLOUD variable not set. Defaulting to ~/Nextcloud"
    export NEXTCLOUD=$HOME/Nextcloud
  fi
  export PATH=${PATH}:"$(cygpath $NEXTCLOUD/share/prefs/bin)"
  export PATH=${PATH}:"$(cygpath $NEXTCLOUD/share/prefs/bin/gnumake-3.8.1)"
  export PATH=${PATH}:"$(cygpath $NEXTCLOUD/share/prefs/bin/nano-2.4.2)"
  export PATH=${PATH}:"$(cygpath C:/Program\ Files/MongoDB/Server/3.4/bin)"
  export PATH=${PATH}:${HOME}/.local/Scripts

  # Only make these scripts available on Windows.
  export PATH=${PATH}:"${HOME}/repos/home/scripts-win"

  # GitForWindows bash inserts the PATH for GitForWindows before anything
  # else, thus it will shadow the GnuPG install, even when put at an early
  # position in the system environment variables.
  export PATH="$(cygpath C:/Program\ Files\ \(x86\)/gnupg/bin)":${PATH}
fi

export PATH=${PATH}:"${HOME}/repos/home/scripts"
export PATH=${PATH}:"${HOME}/bin"
export PATH=${PATH}:"${HOME}/.local/bin"
export PATH=".nodepy/bin":${PATH}

function show-path {
    python -c "import os; print('\n'.join(os.getenv('PATH').split(os.pathsep)))"
}

# =================================================================
# Aliases
# =================================================================

alias ll="ls -lha"
alias cr="craftr"

# =================================================================
# PS1 (thanks to https://stackoverflow.com/a/6086978/791713)
# =================================================================

function __ps1_git_branch {
    __green="\033[49m\033[32m%s"
    __red="\033[49m\033[31m%s"

    # Query current branch, and remove parentheses.
    __branch="`git branch 2> /dev/null | grep -e ^* | sed -E  s/^\\\\\*\ \(.+\)$/\(\\\\\1\)\ /`"
    __branch="`echo ${__branch} | sed 's/[)(]//g'`"
    __color=""

    if [ ! -z "$__branch" ]; then
        __porcelain="`git status --porcelain --untracked-files=no 2> /dev/null`"
        if [ -z "$__porcelain" ]; then
            __color="$__green"
        else
            __color="$__red"
            __branch="$__branch*"
        fi
        __untracked="`git ls-files --others --exclude-standard 2> /dev/null`"
        if [ ! -z "$__untracked" ]; then
            __branch="$__branch+"
        fi
        printf " $__color($__branch)"
    fi
}

function __set_ps1 {
    local __user_and_host="\[\033[01;32m\]\u@\h "
    local __cur_location="\[\033[01;33m\]\w"
    local __prompt_tail="\[\033[49m\]\[\033[34m\]\n$"
    local __last_color="\[\033[00m\]"
    export PS1="$__user_and_host$__cur_location\`__ps1_git_branch\`$__prompt_tail$__last_color "
}
__set_ps1

# =================================================================
# SSH Agent (thanks to http://stackoverflow.com/a/18915067/791713)
# =================================================================

if [ -d "$HOME/.ssh" ] && [[ $- == *i* ]]; then
    SSH_ENV="$HOME/.ssh/environment"
    function start_agent {
        echo ".profile: Initialising new SSH agent..."
        ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
        chmod 600 "${SSH_ENV}"
        . "${SSH_ENV}" > /dev/null
        ssh-add;
    }
    # Source SSH settings, if applicable
    if [ -f "${SSH_ENV}" ]; then
        . "${SSH_ENV}" > /dev/null
        #ps ${SSH_AGENT_PID} doesn't work under cywgin
        ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent > /dev/null || {
            start_agent;
        }
    else
        start_agent;
    fi
elif [[ $- != *i* ]]; then
    echo "note: Not a login shell. Skipping ssh-agent"
else
    echo "note: $HOME/.ssh does'nt exist. Skipping ssh-agent"
fi
