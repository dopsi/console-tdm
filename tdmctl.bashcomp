_tdmctl() 
{
	local cur prev opts base
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"

	#
	#  The basic options we'll complete.
	#
	opts="init list add cache check default enable disable"

	#
	#  Complete the arguments to some of the basic commands.
	#
	case "${prev}" in
		check|default|disable)
			local sessions=$(tdmctl list)
			COMPREPLY=( $(compgen -W "${sessions}" -- ${cur}) )
			return 0
			;;
		enable)
			local sessions=$(tdmctl cache)
			COMPREPLY=( $(compgen -W "${sessions}" -- ${cur}) )
			return 0
			;;
		*)
			;;
	esac

	COMPREPLY=($(compgen -W "${opts}" -- ${cur}))  
	return 0
}
complete -F _tdmctl tdmctl
