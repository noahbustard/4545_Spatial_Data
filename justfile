# ============================================================
# Course Tools — United Courses Constitution (MSU)
# Compatible with just 1.46.0
#
# Dry-run usage:
#   just all <SECTION> 1
# Example:
#   just all 02 1
# ============================================================

set shell := ["bash", "-cu"]

repo := justfile_directory()

help:
    @echo ""
    @echo "Course Tools — Commands"
    @echo "----------------------"
    @echo "just all 02              Run full pipeline"
    @echo "just all 02 dry=1        Dry-run full pipeline"
    @echo ""
    @echo "Individual:"
    @echo "just scaffold 02"
    @echo "just meta 02"
    @echo "just csv 02"
    @echo "just calendar 02"
    @echo "just readmees 02"
    @echo "just check 02"
    @echo ""
    @echo "Dry-run any supported command:"
    @echo "just meta 02 dry=1"
    @echo ""

# ------------------------------------------------------------
# Tasks
# ------------------------------------------------------------

scaffold section dry="0":
    cd "{{repo}}"
    python -m tools.course_tools.generate_scaffolding --root . --section {{section}} {{ if dry == "1" { "--dry-run" } else { "" } }}

meta section dry="0":
    cd "{{repo}}"
    python -m tools.course_tools.generate_meta --root . --section {{section}} --refresh {{ if dry == "1" { "--dry-run" } else { "" } }}

meta-print section assignment:
    python -m tools.course_tools.generate_meta \
        --root . \
        --section {{section}} \
        --assignment {{assignment}} \
        --print

meta-one section assignment:
    cd "{{repo}}"
    python -m tools.course_tools.generate_meta --root . --section {{section}} --assignment {{assignment}} --print

csv section:
    cd "{{repo}}"
    python -m tools.course_tools.export_assignments_csv --root . --section {{section}}

calendar section:
    cd "{{repo}}"
    python -m tools.course_tools.build_global_calendar --root . --section {{section}}

readmees section dry="0":
    cd "{{repo}}"
    python -m tools.course_tools.build_folder_readmees --root . --section {{section}} {{ if dry == "1" { "--dry-run" } else { "" } }}

check section:
    cd "{{repo}}"
    python -m tools.course_tools.course_manager --root . check --section {{section}}

# ------------------------------------------------------------
# Pipeline
# ------------------------------------------------------------

all section dry="0":
    just scaffold {{section}} {{dry}}
    just meta {{section}} {{dry}}
    just csv {{section}}
    just calendar {{section}}
    just readmees {{section}} {{dry}}