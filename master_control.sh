#!/usr/bin/env bash

SELF_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1; pwd)
SELF_NAME=$(basename "${BASH_SOURCE[0]}" || exit 1;)
SELF_FULL="${SELF_PATH}/${SELF_NAME}"

# shellcheck source=./config.sh
source "${SELF_PATH}/config.sh" || exit 1

###
# common stuff

_log () {
	echo -n "${1^^}"; shift
	for t in "$@"; do echo -n " | ${t}"; done; echo
}
_notif () {
	local text=$1; shift
	local title=$1; shift
	local sub=""; for t in "$@"; do sub+="${t} "; done
	read -r -d '' script_notif <<EOT
display notification "${text}" with title "${title}" subtitle "${sub}"
EOT
	osascript -e "$script_notif"; return $?
}
alert () { (>&1 _log "alert" "$@"); return $?; }
error () { (>&2 _log "error" "$@"); return $?; }
finished () { alert "$@" && _notif "$@"; return $?; }

###
# system stuff

open_app () { local name=$1; open -a "$name"; return $?; }
kill_app () { local name=$1; pkill -ix "$name"; return $?; }
kill_apps () {
	for app in "$@"; do
		if kill_app "$app"; then
			finished "system" "kill" "$app terminated"
		fi
	done
	# Fixme: This does not stop when errors occurred.
	return 0
}

###
# power

_power_switch () {
	local power=$1
	local state=$2
	local pname=""

	for sock in "${!POWER_SOCKETS[@]}"; do
		if [[ $sock == "$power" ]]; then power="${POWER_SOCKETS[$sock]}"; fi
	done
	if [[ $power != "$1" ]]; then pname=" (${1})"; fi

	if ! (
		curl -s "$POWER_URL" -d power="$power" -d state="$state" >/dev/null
	); then
		error "power" "switch" "$state" "$power$pname" "could not connect"
		return 1
	fi

	finished "power" "switch" "$state" "$power$pname"
	return 0
}
power_full () { _power_switch "$1" "full"; return $?; }
power_null () { _power_switch "$1" "null"; return $?; }
power_teardown () {
	if ! store_umount; then
		error "power" "teardown" "could not unmount" "stopped"
		return 1
	fi
	kill_apps "${AUDIO_APPS[@]}"
	# Fixme: This powers off disks before unmounting them. This is bad.
	for sock in "${!POWER_SOCKETS[@]}"; do
		if ! power_null "$sock"; then
			error "power" "teardown" "$sock" "stopped"
			return 1
		fi
	done
	finished "power" "teardown" "complete" "${!POWER_SOCKETS[@]}"
	return 0
}

###
# store

_store_mounted () { mount | grep "on $STORE_MOUNT" >/dev/null; return $?; }
_store_wait () {
	local state=$1
	local action; if $state; then action="umount"; else action="mount"; fi
	_show () { alert "store" "$action" "$1" "$STORE_DEVICE"; }
	for ((sec=1;sec<=STORE_DELAY;sec++)); do
		if $state && ! _store_mounted; then _show "done"; return 0; fi
		if ! $state && _store_mounted; then _show "done"; return 0; fi
		sleep 1 && _show "wait $(printf "%02d" $sec)";
	done
	error "store" "$action" "wait timeout" "$STORE_DEVICE"
	return 1
}

store_mount () {
	if _store_mounted; then
		finished "store" "mount" "already there" "$STORE_DEVICE"
		return 0
	fi
	if ! power_full "$STORE_SOCKET"; then
		error "store" "mount" "powerup failed" "$STORE_DEVICE"
		return 1
	fi
	if _store_wait false; then
		finished "store" "mount" "success" "$STORE_DEVICE"
		return 0
	fi
	# Fixme: Find way to manually mount disk if automount failed.
	return 1
}

store_umount () {
	if ! _store_mounted; then
		finished "store" "umount" "already gone" "$STORE_DEVICE"
		power_null "$STORE_SOCKET"
		return 0
	fi

	kill_apps "${STORE_APPS[@]}"
	if ! diskutil eject "$STORE_MOUNT" >/dev/null; then
		error "store" "umount" "eject failed" "$STORE_DEVICE"
		return 1
		# Fixme: Try several times to unmount on error.
	fi

	if _store_wait true; then
		# Fixme: _store_wait loops exactly once here. Find more elegant way.
		finished "store" "umount" "success" "$STORE_DEVICE"
		power_null "$STORE_SOCKET"
		return 0
	fi
	return 1
}

###
# audio

audio_connect () {
	_press_escape () {
		read -r -d '' script_escape <<EOT
tell application "System Events"
	key code 53
end tell
EOT
		osascript -e "$script_escape"; return $?
	}

	local output
	read -r -d '' script_connect <<EOT
tell application "System Events" to tell process "SystemUIServer"
	set bt to (first menu bar item whose description is "bluetooth") of menu bar 1
	click bt
	tell (first menu item whose title is "${AUDIO_DEVICE}") of menu of bt
		click
		tell menu 1
			if exists (menu item "Connect")
				click menu item "Connect"
				return "connected"
			else if exists (menu item "Disconnect")
				return "already connected"
			end if
		end tell
	end tell
end tell
return "error connecting"
EOT
	power_full "$AUDIO_SOCKET" && sleep "$AUDIO_DELAY"
	output=$(osascript -e "$script_connect")
	_press_escape
	finished "audio" "connect" "$output" "$AUDIO_DEVICE"
	case $output in error*) return 1;; *) return 0;; esac
}

audio_launch () {
	local name=$1

	_is_storage () {
		# Fixme: Find some other way to handle application resources.
		for app in "${STORE_APPS[@]}"; do
			case $name in $app) return 0;; *);; esac
		done
		return 1
	}

	if _is_storage; then
		if ! store_mount; then
			error "audio" "launch" "mount failed"
			return 1
		fi
	fi
	audio_connect
	if ! open_app "$name"; then return 1; fi
	finished "audio" "launch" "success" "$name"
	return 0
}


###
# installation

_install_generate () {
	# Fixme: Do not bake in full paths in scripts.
	# Fixme: Abort when launched in older bash versions, or get compatible.
	local args
	local func=$1; shift
	for a in "$@"; do args+=" \"${a}\""; done
	read -r -d '' script_gen <<EOT
#!/usr/bin/env bash

source "${SELF_FULL}" && (
	${func}${args}
)
EOT
	echo -n "$script_gen"; return 0
}

_install_file () {
	# Fixme: Do not spread files around in user directories.
	local script
	local target
	script=$(_install_generate "$@")
	local name="${1,,}"; shift
	for a in "$@"; do name+="_${a,,}"; done
	target="${INSTALL_PATH}/${name}.${INSTALL_EXT}"
	if (echo -n "$script" > "$target" && chmod +x "$target"); then
		alert "install" "$name" "$target"
	fi
	return 0
}

installation () {
	_install_file "audio_connect"
	for name in "${AUDIO_APPS[@]}"; do
		_install_file "audio_launch" "$name"
	done
	for func in "power_full" "power_null"; do
		for name in "${!POWER_SOCKETS[@]}"; do
			_install_file "$func" "$name"
		done
	done
	_install_file "power_teardown"
	for func in "store_mount" "store_umount"; do
		_install_file "$func"
	done
	return 0
}

# invoke installer if this file is not sourced
if ! test "${BASH_SOURCE[1]+bbq}"; then installation; fi
