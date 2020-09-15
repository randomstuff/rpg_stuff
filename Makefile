.DEFAULT: all
.PHONY: all
all: output/tactical_rule.svg output/province_rule.svg

output/tactical_rule.svg: params/tactical_rule.yaml templates/rule.svg.j2
	./render.py params/tactical_rule.yaml -o output/tactical_rule.svg
output/province_rule.svg: params/province_rule.yaml templates/rule.svg.j2
	./render.py params/province_rule.yaml -o output/province_rule.svg

