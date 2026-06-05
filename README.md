# gs-1098-model

台中洲際段1098地號建物 3D 建模 — Blender 5.1.2

## 快速開始

### 直接開啟（推薦）
```
Blender → File → Open → blend/1098_final_with_roads.blend
```
所有材質、燈光、家具、透明外殼完整保存，開啟即可繼續修改。

### 匯入到現有場景
```
File → Append → blend/1098_final_with_roads.blend → Object → (全選)
```
或使用 Link（保持連結，修改原檔會同步）：
```
File → Link → blend/1098_final_with_roads.blend → Object → (全選)
```

### 從備用格式匯入
| 格式 | 路徑 | 適用情境 |
|------|------|---------|
| FBX | `exports/1098_final.fbx` | 其他 DCC（3ds Max, Maya）或 Blender 含材質匯入 |
| GLB | `exports/1098_final.glb` | Web 瀏覽器、Three.js、Unity、Unreal Engine |

Blender 匯入 FBX：`File → Import → FBX (.fbx)`

## 場景說明

| 項目 | 數值 |
|------|------|
| 單位 | 公尺（1:1 實尺） |
| 樓層 | B1 + 1~5F + 屋突（共 7 層） |
| 總物件數 | 349 |
| 材質數 | 50 |
| 燈光 | 11 盞 Area Light |
| B1 停車 | 6 台車（8 格中佔 6） |
| 素材來源 | PolyHaven（家具）、自製幾何體（車、樹、結構） |

## 目錄結構

```
gs-1098-model/
├── blend/
│   └── 1098_final_with_roads.blend   ← 主場景（直接開啟）
├── exports/
│   ├── 1098_final.fbx                ← FBX 備用格式
│   └── 1098_final.glb                ← glTF/GLB 備用格式
├── scripts/
│   └── rebuild_scene.py              ← 重建腳本（骨架結構）
└── docs/
    ├── build-log.md                  ← 完整六階段建模日誌
    └── progress.md                   ← 本 repo 建置紀錄
```

## 重建腳本

若 `.blend` 主檔損毀，可用 `scripts/rebuild_scene.py` 重建場景骨架：
1. 開啟 Blender → Scripting workspace
2. 貼上或載入 `rebuild_scene.py`
3. 按 Run Script

> 注意：重建腳本只含結構量體、材質、燈光、攝影機，不含 PolyHaven 家具素材。
> 家具素材需透過 blender-mcp 重新下載配置（詳見 `docs/build-log.md` 第四階段）。

## 建物基本尺寸

- 軸線橫向（X）：0~23.7m
- B1 縱深（Y）：0~23.1m；地上各層：2.6~16.6m
- 各層高度：B1=-3.5~0m、1F=0~4m、2F=4~7.5m、3F=7.5~10.5m、
  4F=10.5~13.5m、5F=13.5~16.5m、屋突=16.5~19m

## 需求環境

- Blender 5.1.2（Windows）
- EEVEE 渲染引擎（已設定）
- 選用：blender-mcp（TCP 9876）若需繼續 AI 輔助建模
