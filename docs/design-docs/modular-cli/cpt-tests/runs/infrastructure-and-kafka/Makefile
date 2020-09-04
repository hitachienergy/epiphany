ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

BMK_VERSION := 1
AZI_VERSION := 1
USER := epitest

.PHONY: all clean init-and-apply-azure-infrastructure init-and-apply-kafka just-init-kafka and-then-apply-kafka state ensure-shared

all: clean init-and-apply-azure-infrastructure init-and-apply-kafka state

clean: ensure-shared
	rm $(ROOT_DIR)/shared/*

init-and-apply-azure-infrastructure: guard-AZI_VERSION guard-USER ensure-shared
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-azi:$(AZI_VERSION) \
		init
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-azi:$(AZI_VERSION) \
		apply

init-and-apply-kafka: guard-BMK_VERSION guard-USER ensure-shared
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-bmk:$(BMK_VERSION) \
		init
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-bmk:$(BMK_VERSION) \
		apply

just-init-kafka: guard-BMK_VERSION guard-USER ensure-shared
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-bmk:$(BMK_VERSION) \
		init

and-then-apply-kafka: guard-BMK_VERSION guard-USER ensure-shared
	@docker run --rm \
		-v $(ROOT_DIR)/shared:/shared \
		-t $(USER)/epi-c-bmk:$(BMK_VERSION) \
		apply

state:
	@if test -f $(ROOT_DIR)/shared/state.yml; then cat $(ROOT_DIR)/shared/state.yml ; else echo UNINITIALIZED && exit 1; fi

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

ensure-shared:
	mkdir -p $(ROOT_DIR)/shared
