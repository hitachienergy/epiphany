#medatada method is printing static metadata information about module
metadata: guard-C_TEMPLATES
	@echo \# AzI \| metadata \| should print component metadata
	@cat ${C_TEMPLATES}/mocked-metadata.yml

#init method is used to initialize module configuration and check if state is providing strong (and weak) dependencies
init: guard-C_TEMPLATES guard-C_SHARED guard-C_CONFIG
	@echo \# AzI \| init \| should create default config in shared directory
	@echo \# AzI \| init \| should also validate state if strong requirements are met
	@cp ${C_TEMPLATES}/mocked-config.yml ${C_SHARED}/${C_CONFIG}
	@if test -f ${C_SHARED}/state.yml ; \
	then \
		yq m -x -i ${C_SHARED}/state.yml ${C_TEMPLATES}/mocked-state-new.yml ; \
	else \
		yq m -x ${C_TEMPLATES}/mocked-state-new.yml > ${C_SHARED}/state.yml ; \
	fi

#plan method would get config file and environment state file and compare them and calculate what would be done o apply stage
plan: guard-C_SHARED
	@echo \# AzI \| plan \| should validate if config file is correct
	@echo \# AzI \| plan \| should also be called automatically before apply
	@if test -f ${C_SHARED}/${C_CONFIG}; then yq v ${C_SHARED}/${C_CONFIG} ; else echo file not found && exit 1; fi

#apply method runs module provider logic using config file
apply: guard-C_TEMPLATES guard-C_SHARED plan
	@echo \# AzI \| apply \| should apply module logic
	@yq m -x -i ${C_SHARED}/state.yml ${C_SHARED}/${C_CONFIG}
	@yq w -i ${C_SHARED}/state.yml azi.status applied
	$(eval last = $(shell yq r ${C_SHARED}/${C_CONFIG} azi.size))
	@number=0 ; while [[ $$number -lt $(last) ]] ; do \
		yq w -i ${C_SHARED}/state.yml azi.nodes[$$number].privateIP "10.0.0.$$number" ; \
		yq w -i ${C_SHARED}/state.yml azi.nodes[$$number].publicIP "213.1.1.$$number" ; \
		yq w -i ${C_SHARED}/state.yml azi.nodes[$$number].usedBy unused ; \
		number=`expr $$number + 1`; \
	done

#audit method should call logic to check if remote components are in "known" state
audit: guard-C_SHARED
	@echo \# AzI \| audit \| should output current state of remote components
	@echo \# AzI \| audit \| it should for example connect to machines it knows about and check if configuration is the same it applied
	@echo \# AzI \| audit \| this is crucial method for "update" processes

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi
