#!/usr/bin/env bash

export INSTALL_EXT="command"
export INSTALL_PATH="${HOME}/bin"

family="01101"
declare -A POWER_SOCKETS=(
	[light_desk]="${family}01000"
	[music_ctrl]="${family}00100"
	[store_disk]="${family}00010"
)
export POWER_HOSTNAME="datensammel-leitschiene"
export POWER_SOCKETS
export POWER_URL="http://${POWER_HOSTNAME}.local"

declare STORE_APPS=(
	"Adobe Photoshop Lightroom 4"
	"iTunes"
	"Photos"
)
export STORE_APPS
export STORE_DELAY=30
export STORE_DEVICE="Kleinhirn"
export STORE_MOUNT="/Volumes/${STORE_DEVICE}"
export STORE_SOCKET="store_disk"

declare AUDIO_APPS=(
	"Deezer"
	"iTunes"
)
export AUDIO_APPS
export AUDIO_DELAY=10
export AUDIO_DEVICE="Krawallschachtel"
export AUDIO_SOCKET="music_ctrl"
