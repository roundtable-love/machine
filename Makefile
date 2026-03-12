# Machine — Transpilation Targets
#
# Generates: $(OUTDIR)/<type>/README.<type>.<lang>.md
#
# Usage:
#   make                  — all targets
#   make subject          — all languages for one node type
#   make en               — all node types for one language
#   make TRANSPILE=my-tool — override generation command
#
# TRANSPILE is called as: $(TRANSPILE) <node-type> <lang-code> --source <path>

TRANSPILE := nix run $(CURDIR)#transpile --

LANGUAGES := $(shell $(TRANSPILE) --languages)

NODE_TYPES := $(shell $(TRANSPILE) --node-types)

OUTDIR ?= human

# ── Rules ─────────────────────────────────────────────────────────────────────

define RULE
$(OUTDIR)/$(1)/README.$(1).$(2).md: machine.md grammar.md
	@mkdir -p $$(@D)
	$(TRANSPILE) $(1) $(2) > $$@
endef

$(foreach t,$(NODE_TYPES),\
  $(foreach l,$(LANGUAGES),\
    $(eval $(call RULE,$(t),$(l)))))

# ── Aggregate targets ──────────────────────────────────────────────────────────

_all_targets := $(foreach t,$(NODE_TYPES),\
                  $(foreach l,$(LANGUAGES),\
                    $(OUTDIR)/$(t)/README.$(t).$(l).md))

# Per-node-type: make subject
define NODE_PHONY
$(1): $(foreach l,$(LANGUAGES),$(OUTDIR)/$(1)/README.$(1).$(l).md)
endef

$(foreach t,$(NODE_TYPES),$(eval $(call NODE_PHONY,$(t))))

# Per-language: make en
define LANG_PHONY
$(1): $(foreach t,$(NODE_TYPES),$(OUTDIR)/$(t)/README.$(t).$(1).md)
endef

$(foreach l,$(LANGUAGES),$(eval $(call LANG_PHONY,$(l))))
