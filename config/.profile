
# Cmder always starts up in its application directory, thus we set
# this environment variable to automatically switch to it.
if [ ! -z "$CDFROMPROFILE" ]; then
  cd ~
  unset CDFROMPROFILE
fi

if [ -f ~/.profile.local ]; then
  source ~/.profile.local
fi

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
  export PATH=${PATH}:"~/Library/Python/3.7/bin:/usr/local/lib/python3.7/site-packages"
  export PATH=${PATH}:"/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
  export PATH=${PATH}:"/usr/local/gnupg-2.2/bin"
  # added by Miniconda3 installer
  # export PATH="/Users/nrosenstein/miniconda3/bin:$PATH"
  export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home"
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

export PYTHONDONTWRITEBYTECODE=x
export PIPENV_VENV_IN_PROJECT=x

# =================================================================
# Aliases
# =================================================================

alias ll="ls -lha"
alias cr="craftr"

# =================================================================
# PS1 (thanks to https://stackoverflow.com/a/6086978/791713)
# =================================================================

nr powerline 2>/dev/null >/dev/null
if [ $? == 0 ]; then
    export PS1="\`nr powerline\`\n$ "
fi

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
