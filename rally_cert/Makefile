CURRENT_DIRECTORY := $(shell pwd)
DATETIME = $(shell date +"%j_%h_%y_%Y_%T")

test: create_deployment run_tests generate_reports

create_deployment:
		rally deployment create --fromenv --name=Current

run_tests:
		sh ./run_rally.sh

generate_reports:
		mkdir $(ARTIFACTS_DIR)/$(DATETIME)
		$(eval TASK_LIST := $(shell rally task list --uuids-only))
		rally task report --tasks $(TASK_LIST) --out=$(ARTIFACTS_DIR)/$(DATETIME)/rally_report.html
		rally task report --tasks $(TASK_LIST) --out=$(ARTIFACTS_DIR)/$(DATETIME)/rally_report.xml --junit
