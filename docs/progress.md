# Repo 建置進度

## 目標
將 Blender 3D 建模（台中洲際段1098地號）遷移到獨立 git repo，
保存 .blend 主檔與重建腳本，確保後續可直接在 Blender 開啟修改。

## 計畫 milestone
- [ ] M1：repo 目錄結構 + git init + .gitignore
- [ ] M2：複製 .blend + 進度文件，初始 commit
- [ ] M3：匯出 FBX / glTF 備用格式
- [ ] M4：產生 rebuild_scene.py（重建腳本）
- [ ] M5：README + 最終 commit

## 進度日誌

## Fallback 指引
- 主檔：`blend/1098_final_with_roads.blend` → Blender 5.1.2 直接開啟
- 重建腳本：`scripts/rebuild_scene.py` → 在 Blender Scripting 分頁執行可從頭重建場景
- 備用格式：`exports/` 下的 .fbx / .glb → 其他 DCC 工具匯入用
