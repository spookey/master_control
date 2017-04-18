APP_NAME ?= shove
EXT_MODULE ?= ext
LIB_MODULE ?= lib
LOGGER_DIR ?= log

help:
	@echo "master control makefile"
	@echo "------ ------- --------"
	@echo
	@echo "clean"		"\t\t" "clean up unnecessary files"
	@echo " ↪︎ log"		"\t\t" "clean up old log files"
	@echo " ↪︎ pyc"		"\t\t" "clean up python temp files"
	@echo " ↪︎ rev"		"\t\t" "clean up pyreverse files"
	@echo "count"		"\t\t" "count lines of code with cloc"
	@echo "graph"		"\t\t" "make graph with pyreverse"
	@echo " ↪︎ o"		"\t\t" "make graph and open them"
	@echo "lint"		"\t\t" "lint code with pylint"
	@echo "reqs"		"\t\t" "update requirements.txt"
	@echo "sort"		"\t\t" "sort code with isort"
	@echo "watch"		"\t\t" "watch log output"


CLOC_CMD := cloc
DELTREE_CMD := rm -rfv
FIND_CMD := find
ISORT_CMD := isort
OPEN_CMD := open
PIPREQS_CMD := pipreqs
PYLINT_CMD := pylint
PYLINT_TPL := \
{C} {path}:{line}:{column} - {msg}\
  ↪︎ {category} {module}.{obj} ({symbol} {msg_id})
PYREV_CMD := pyreverse
PYREV_FILES := \
	classes_$(APP_NAME).png \
	packages_$(APP_NAME).png
TAIL_CMD := tail -F

cleanlog:
	@$(DELTREE_CMD) $(LOGGER_DIR)/*_debug.log.?

cleanrev:
	@$(DELTREE_CMD) $(PYREV_FILES)

cleanpyc:
	@$(FIND_CMD) . \
		-name '*.pyc' -delete -print \
		-o \
		-name '__pycache__' -delete -print

clean: cleanlog cleanpyc cleanrev


count:
	@$(CLOC_CMD) --progress-rate=5 .

graph:
	@$(PYREV_CMD) \
		--all-ancestors \
		--filter-mode="ALL" \
		--module-names="yes" \
		--output png \
		--project="$(APP_NAME)" \
		"$(LIB_MODULE)" "$(EXT_MODULE)"

grapho: graph
	@$(OPEN_CMD) $(PYREV_FILES)

lint:
	@$(PYLINT_CMD) \
		--disable "C0111" \
		--disable "I0011" \
		--msg-template="$(PYLINT_TPL)" \
		--output-format="colorized" \
		--reports="no" \
		"$(LIB_MODULE)" "$(EXT_MODULE)"

reqs:
	@$(PIPREQS_CMD) --force .

sort:
	@$(ISORT_CMD) -cs -fss -m=5 -y -rc .

watch:
	@$(TAIL_CMD) $(LOGGER_DIR)/*.log
