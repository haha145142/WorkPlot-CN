#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1])
compat = root / "WorkPlot/Models/DeviceCompatibility.swift"
source = compat.read_text(encoding="utf-8")

old = '''        if major == 27 {
            guard let raw = build, let parsed = Build.parse(raw) else {
                return .unsupported(reason:
                    "Unable to verify your iOS 27 build. Only up to iOS 27.0 beta 4 (build 24A5390f) is supported; newer builds are patched.")
            }
            if parsed > newestSupportedBuild {
                return .unsupported(reason:
                    "Your build \\(raw) is newer than 27.0 developer beta 4 (24A5390f) and is patched.")
            }
        }'''
new = '''        if major == 27 {
            guard let raw = build else {
                return .unsupported(reason:
                    "无法读取当前 iOS 27 系统构建号。MobileGestalt 写入仅验证过 iOS 27.0 Beta 1–4。")
            }
            // Exact allow-list: build identifiers are not safely ordered by
            // their numeric suffix (for example, public 24A437 is not beta 4).
            let verifiedBuilds: Set<String> = [
                "24A5355q", // Developer Beta 1
                "24A5370h", // Developer Beta 2
                "24A5380h", // Developer Beta 3 / Public Beta 1
                "24A5390f"  // Developer Beta 4 / Public Beta 2
            ]
            guard verifiedBuilds.contains(raw) else {
                return .unsupported(reason:
                    "当前系统构建版本 \\(raw) 不在已验证范围内。MobileGestalt 写入仅在 iOS 27.0 Beta 1–4 验证；正式版及后续版本已修补。")
            }
        }'''
if old not in source:
    raise SystemExit("Could not find expected iOS 27 compatibility block; refusing to patch an unknown upstream version.")
source = source.replace(old, new, 1)

old2 = '''    static func fullFeatureStatus(feature: String) -> Status {
        let version = currentOS().version
        if version.majorVersion < 27 {
            return .unsupported(reason:
                "\\(feature) requires iOS 27. You are running iOS \\(version.majorVersion).\\(version.minorVersion), which currently supports PosterBoard only.")
        }
        return .supported
    }

    static var supportsFullFeatureSet: Bool {
        if case .supported = fullFeatureStatus(feature: "This feature") { return true }
        return false
    }'''
new2 = '''    static func fullFeatureStatus(feature: String) -> Status {
        if case .unsupported(let reason) = currentStatus {
            return .unsupported(reason: reason)
        }
        let version = currentOS().version
        if version.majorVersion < 27 {
            return .unsupported(reason:
                "\\(feature) 需要 iOS 27。当前系统为 iOS \\(version.majorVersion).\\(version.minorVersion)，目前仅支持 PosterBoard。")
        }
        return .supported
    }

    static var supportsFullFeatureSet: Bool {
        if case .supported = currentStatus,
           case .supported = fullFeatureStatus(feature: "此功能") {
            return true
        }
        return false
    }'''
if old2 not in source:
    raise SystemExit("Could not find expected feature-gating block; refusing to patch an unknown upstream version.")
source = source.replace(old2, new2, 1)
compat.write_text(source, encoding="utf-8")

unsupported = root / "WorkPlot/Views/UnsupportedView.swift"
view = unsupported.read_text(encoding="utf-8")
view = view.replace('Text(reason)\n                    .font(.subheadline)', 'Text(localizedReason)\n                    .font(.subheadline)', 1)
view = view.replace('''    private var os: DeviceCompatibility.OSInfo { DeviceCompatibility.currentInfo }

    var body: some View {''', '''    private var os: DeviceCompatibility.OSInfo { DeviceCompatibility.currentInfo }

    private var localizedReason: String {
        if os.version.majorVersion == 27 {
            return "当前系统构建版本 \\(os.build ?? "未知") 不在已验证范围内。MobileGestalt 写入仅在 iOS 27.0 Beta 1–4 验证；正式版及后续版本已修补。"
        }
        return "此工具需要 iOS 27.0 Beta 1–4 才能执行系统写入。当前系统版本不在支持范围内。"
    }

    var body: some View {''', 1)
# FeatureUnsupportedView has its own reason property and text.
marker = '''struct FeatureUnsupportedView: View {
    let feature: String

    private var os: DeviceCompatibility.OSInfo { DeviceCompatibility.currentInfo }

    private var reason: String {'''
replacement = '''struct FeatureUnsupportedView: View {
    let feature: String

    private var os: DeviceCompatibility.OSInfo { DeviceCompatibility.currentInfo }

    private var localizedReason: String {
        if os.version.majorVersion == 27 {
            return "当前系统构建版本 \\(os.build ?? "未知") 不在已验证范围内。此功能依赖的系统写入能力已在 iOS 27.0 正式版及后续版本中修补。"
        }
        return "此功能需要 iOS 27.0 Beta 1–4。当前系统版本不在已验证范围内。"
    }

    private var reason: String {'''
if marker not in view:
    raise SystemExit("Could not find FeatureUnsupportedView declaration.")
view = view.replace(marker, replacement, 1)
# Replace second remaining Text(reason) occurrence (first was changed above).
view = view.replace('Text(reason)\n                    .font(.subheadline)', 'Text(localizedReason)\n                    .font(.subheadline)', 1)
unsupported.write_text(view, encoding="utf-8")
print("Patched exact iOS 27 build allow-list and localized unsupported notices.")
