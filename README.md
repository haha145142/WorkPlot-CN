# WorkPlot 简体中文版（非官方）

这是基于 gievano/WorkPlot 的社区简体中文本地化构建。上游源码在 GitHub Actions 构建时按固定提交拉取，随后叠加本仓库的中文资源与本地化补丁。

- 上游：https://github.com/gievano/WorkPlot
- 固定上游提交：0efe6e3f8740d213905afa5cee14846ed9bb91bf
- 许可证：GPL-3.0；请保留上游版权、许可证与第三方声明。

## 构建

推送到 main 后会自动运行 GitHub Actions；也可在 Actions 页面手动运行 Build WorkPlot Chinese IPA。成功后在运行记录的 Artifacts 下载 WorkPlot-CN-unsigned-IPA。

输出为未签名 IPA，需要自行签名安装。

## 重要兼容性警告

汉化只改变界面语言，不会恢复已被系统修补的 MobileGestalt 写入能力。上游明确说明写入能力只在 iOS 27 Developer Beta 1–4 验证；后续版本已修补。iOS 27.0 正式版 24A437 不应期待核心写入功能可用。请先完整备份设备，不要尝试不受支持的系统写入。

## 免责声明

这是非官方汉化构建，与 Apple 或 WorkPlot 原作者无关联。WorkPlot 会修改系统状态，可能造成系统功能异常、数据丢失或需要恢复设备。风险由使用者自行承担。
