#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then echo "Usage: $0 /path/to/WorkPlot-source" >&2; exit 2; fi
SOURCE_ROOT="$(cd "$1" && pwd)"
PATCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$SOURCE_ROOT/WorkPlot/zh-Hans.lproj"
cp "$PATCH_ROOT/Localization/WorkPlot/zh-Hans.lproj/Localizable.strings" "$SOURCE_ROOT/WorkPlot/zh-Hans.lproj/Localizable.strings"
cp "$PATCH_ROOT/Localization/WorkPlot/zh-Hans.lproj/InfoPlist.strings" "$SOURCE_ROOT/WorkPlot/zh-Hans.lproj/InfoPlist.strings"
python3 - "$SOURCE_ROOT" <<'PY'
from pathlib import Path
import re, sys
root=Path(sys.argv[1])
pbx=root/"WorkPlot/WorkPlot.xcodeproj/project.pbxproj"
s=pbx.read_text(encoding="utf-8")
if '"zh-Hans"' not in s:
    s2,n=re.subn(r'(knownRegions = \(\n)([ \t]*en,\n)([ \t]*)(Base,)',r'\1\2\3"zh-Hans",\n\3\4',s,count=1)
    if n: pbx.write_text(s2,encoding="utf-8")
    else: print("WARN: could not register zh-Hans in knownRegions")
replacements={
"WorkPlot/Views/Components.swift":[
("struct ActionButton: View {\n    let title: String","struct ActionButton: View {\n    let title: LocalizedStringKey"),
("Text(title.uppercased())","Text(LocalizedStringKey(title)).textCase(.uppercase)"),
("Text(detail)","Text(LocalizedStringKey(detail))"),
("Text(message).font(.subheadline.weight(.semibold))","Text(LocalizedStringKey(message)).font(.subheadline.weight(.semibold))"),
("Text(message)\n                    .font(.subheadline.weight(.semibold))","Text(LocalizedStringKey(message))\n                    .font(.subheadline.weight(.semibold))")],
"WorkPlot/UI/WPActionButton.swift":[("let title: String","let title: LocalizedStringKey")],
"WorkPlot/Views/HomeView.swift":[
("Text(title)\n                .font(.subheadline.weight(.semibold))","Text(LocalizedStringKey(title))\n                .font(.subheadline.weight(.semibold))"),
("Text(title)\n                    .font(.subheadline.weight(.semibold))","Text(LocalizedStringKey(title))\n                    .font(.subheadline.weight(.semibold))"),
("Text(detail)\n                    .font(.caption)","Text(LocalizedStringKey(detail))\n                    .font(.caption)"),
("Text(tweak.title)","Text(LocalizedStringKey(tweak.title))"),
("Text(tweak.isEnabled ? (isConfiguring ? \"Configuring\" : \"Enabled\") : tweak.subtitle)","Text(LocalizedStringKey(tweak.isEnabled ? (isConfiguring ? \"Configuring\" : \"Enabled\") : tweak.subtitle))"),
("Text(option).tag(index)","Text(LocalizedStringKey(option)).tag(index)"),
("Label(note, systemImage: \"exclamationmark.triangle\")","Label(LocalizedStringKey(note), systemImage: \"exclamationmark.triangle\")")],
"WorkPlot/Views/SystemHubView.swift":[
("Text(title).font(.body.weight(.semibold))","Text(LocalizedStringKey(title)).font(.body.weight(.semibold))"),
("Text(detail).font(.caption)","Text(LocalizedStringKey(detail)).font(.caption)")],
"WorkPlot/Views/SiriAISetupView.swift":[
("Text(option.rawValue).tag(option)","Text(LocalizedStringKey(option.rawValue)).tag(option)"),
("Text(title).font(.body.weight(.semibold))","Text(LocalizedStringKey(title)).font(.body.weight(.semibold))"),
("Text(detail)\n                .font(.caption)","Text(LocalizedStringKey(detail))\n                .font(.caption)")],
"WorkPlot/Views/SettingsView.swift":[
("Text(selectedIcon.title)","Text(LocalizedStringKey(selectedIcon.title))"),
("Text(\"System\").tag(0)","Text(\"Follow System\").tag(0)")],
"WorkPlot/Views/AppIconPickerView.swift":[("Text(option.title)","Text(LocalizedStringKey(option.title))")]
}
for rel,pairs in replacements.items():
 p=root/rel
 if not p.exists(): print(f"WARN missing {rel}"); continue
 data=p.read_text(encoding="utf-8")
 for old,new in pairs:
  if old in data: data=data.replace(old,new)
  else: print(f"WARN replacement not found in {rel}: {old[:60]!r}")
 p.write_text(data,encoding="utf-8")
print("Simplified Chinese localization overlay applied.")
PY