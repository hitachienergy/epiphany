#medatada method is printing static metadata information about module
metadata: guard-C_TEMPLATES
	@echo \# BMK \| metadata \| should print component metadata
	@cat ${C_TEMPLATES}/mocked-metadata.yml

#init method is used to initialize module configuration and check if state is providing strong (and weak) dependencies
init: guard-C_TEMPLATES guard-C_SHARED guard-C_CONFIG copy-config update-state
	@echo \# BMK \| init \| should create default config in shared directory
	$(eval unuseds = $(shell yq r ${C_SHARED}/state.yml --length --collect azi.nodes.usedBy==unused))
	$(eval required = $(shell yq r ${C_SHARED}/${C_CONFIG} bmk.size))
	$(eval unusedsPaths = $(shell yq r ${C_SHARED}/state.yml --printMode p azi.nodes.\(usedBy==unused\)))
	@export UP="$(unusedsPaths)" ; \
	if [ ${unuseds} -ge ${required} ] ; \
	then \
		n0=0 ; n1=1; while [[ $$n0 -lt $(required) ]] ; do \
			c=`echo $$UP  | cut -d ' ' -f $$n1` ; \
			yq w -i ${C_SHARED}/${C_CONFIG} bmk.clusterNodes[$$n0].privateIP `yq r ${C_SHARED}/state.yml $$c.privateIP` ; \
			yq w -i ${C_SHARED}/${C_CONFIG} bmk.clusterNodes[$$n0].publicIP `yq r ${C_SHARED}/state.yml $$c.publicIP` ; \
			n0=`expr $$n0 + 1`; \
			n1=`expr $$n1 + 1`; \
		done ; \
	else \
		echo NOT ENOUGH UNUSED MACHINES ; \
	fi

#plan method would get config file and environment state file and compare them and calculate what would be done o apply stage
plan: guard-C_SHARED
	@echo \# BMK \| plan \| should validate if config file is correct
	@echo \# BMK \| plan \| should also be called automatically before apply
	@if test -f ${C_SHARED}/${C_CONFIG}; then yq v ${C_SHARED}/${C_CONFIG} ; else echo file not found && exit 1; fi

#apply method runs module provider logic using config file
apply: guard-C_TEMPLATES guard-C_SHARED plan create-machines
	@echo \# BMK \| apply \| should apply module logic
	$(eval createdPaths = $(shell yq r ${C_SHARED}/state.yml --printMode p bmk.clusterNodes.\(state==created\)))
	@export CP="$(createdPaths)" ; \
	for p in $$CP ; do \
        yq w -i ${C_SHARED}/state.yml azi.nodes.\(privateIP==`yq r ${C_SHARED}/state.yml $$p.privateIP`\).usedBy bmk ; \
    done

#audit method should call logic to check if remote components are in "known" state
audit: guard-C_SHARED
	@echo \# BMK \| audit \| should output current state of remote components
	@echo \# BMK \| audit \| it should for example connect to machines it knows about and check if configuration is the same it applied
	@echo \# BMK \| audit \| this is crucial method for "update" processes

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

copy-config:
	@cp ${C_TEMPLATES}/mocked-config.yml ${C_SHARED}/${C_CONFIG}

update-state:
	@if test -f ${C_SHARED}/state.yml ; \
	then \
		yq m -x -i ${C_SHARED}/state.yml ${C_TEMPLATES}/mocked-state-new.yml ; \
	else \
		echo state not initialized ; \
		exit 1 ;\
	fi

create-machines:
	@yq m -x -i ${C_SHARED}/state.yml ${C_SHARED}/${C_CONFIG}
	@yq w -i ${C_SHARED}/state.yml bmk.status applied
	@yq w -i ${C_SHARED}/state.yml bmk.clusterNodes.*.state created
