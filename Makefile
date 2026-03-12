# Machine — Transpilation Targets
#
# Generates: human/<type>/README.<type>.<lang>.md
#
# Usage:
#   make                  — all targets
#   make subject          — all languages for one node type
#   make en               — all node types for one language
#   make TRANSPILE=my-tool — override generation command
#
# TRANSPILE is called as: $(TRANSPILE) <node-type> <lang-code> --source <path>

LANGUAGES := $(shell $(TRANSPILE) --languages)

NODE_TYPES := newborn infant child subject student peer

TRANSPILE := $(CURDIR)/bin/transpile

# ── Rules ─────────────────────────────────────────────────────────────────────

define RULE
human/$(1)/README.$(1).$(2).md: machine.md grammar.md
	@mkdir -p $$(@D)
	$(TRANSPILE) $(1) $(2) --source machine.md > $$@
endef

$(foreach t,$(NODE_TYPES),\
  $(foreach l,$(LANGUAGES),\
    $(eval $(call RULE,$(t),$(l)))))

# ── Aggregate targets ──────────────────────────────────────────────────────────

_all_targets := $(foreach t,$(NODE_TYPES),\
                  $(foreach l,$(LANGUAGES),\
                    human/$(t)/README.$(t).$(l).md))

# Per-node-type: make subject
define NODE_PHONY
$(1): $(foreach l,$(LANGUAGES),human/$(1)/README.$(1).$(l).md)
endef

$(foreach t,$(NODE_TYPES),$(eval $(call NODE_PHONY,$(t))))

# Per-language: make en
define LANG_PHONY
$(1): $(foreach t,$(NODE_TYPES),human/$(t)/README.$(t).$(1).md)
endef

$(foreach l,$(LANGUAGES),$(eval $(call LANG_PHONY,$(l))))

# ── Standards targets ──────────────────────────────────────────────────────────

COMPILE   := $(CURDIR)/bin/compile
LAW_DIR   := $(CURDIR)/../law
STD_DIR   := $(CURDIR)/../standards
LAW_FILES := $(filter-out $(LAW_DIR)/README.md,$(wildcard $(LAW_DIR)/*.md))
STD_YAMLS := $(patsubst $(LAW_DIR)/%.md,$(STD_DIR)/LAW-%.yaml,$(LAW_FILES))

# Per-file rule — UID mapping is handled inside the compile script;
# use --all so stem→UID lookup is centralised there.
$(STD_DIR)/LAW-CE.yaml: $(LAW_DIR)/CAUSE-AND-EFFECT.md
	$(COMPILE) $< $@

$(STD_DIR)/LAW-R.yaml: $(LAW_DIR)/REFLECTION.md
	$(COMPILE) $< $@

$(STD_DIR)/LAW-T.yaml: $(LAW_DIR)/TRUTH.md
	$(COMPILE) $< $@

.PHONY: standards
standards: $(STD_DIR)/LAW-CE.yaml $(STD_DIR)/LAW-R.yaml $(STD_DIR)/LAW-T.yaml

# ── Schema ─────────────────────────────────────────────────────────────────────

SCHEMA    := $(CURDIR)/bin/schema
STD_SCHEMA := $(CURDIR)/standard.schema.json

$(STD_SCHEMA): $(CURDIR)/../standard/standard.md
	$(SCHEMA) $< > $@

.PHONY: schema
schema: $(STD_SCHEMA)

# ── Standard targets ───────────────────────────────────────────────────────────

.PHONY: all clean $(NODE_TYPES) $(LANGUAGES)

all: $(_all_targets)

clean:
	rm -rf $(foreach t,$(NODE_TYPES),human/$(t))
