# 水墨金陵梦 · 数字长卷（网页版）

把 3D 场景渲染成一张 8000×3200 的超高清长卷，切片后供网页无限缩放查看；
另附 8 个机位的漫游页与 30 秒成片。

## 打开方式

DZI 瓦片必须走 http 加载（`file://` 会被浏览器同源策略挡住），所以要先起一个本地服务：

```bash
python serve.py          # 默认 8080
python serve.py 9000     # 或指定端口
```

然后浏览器访问 <http://127.0.0.1:8080/>

Windows 下也可以直接双击 `start.bat`。

## 页面

| 文件 | 内容 |
|---|---|
| `index.html` | 长卷主页面：滚轮缩放、拖拽平移、双击放大，右下角有导航缩略图 |
| `tour.html` | 机位漫游：8 个机位，滚轮 / 方向键 / 上下滑切换，带缓慢推近 |
| `media/film.mp4` | 30 秒成片（1728×720 / 12fps） |
| `media/poster.png` | 主视觉海报 |

## 目录

```
web/
  index.html          长卷页面
  tour.html           机位漫游页面
  serve.py            本地静态服务
  start.bat           Windows 一键启动
  lib/                OpenSeadragon 4.1.0（本地优先，失败回退 CDN）
  tiles/              DZI 瓦片金字塔（580 块 / 3.7 MB）
    hero.dzi
    hero_files/0..13/
  tour/               8 个机位（4000×1800 JPG / 6.4 MB）
  media/              成片与海报
```

## 部署

整个 `web/` 目录是纯静态的，可直接上传到任何静态托管
（GitHub Pages / Netlify / 阿里云 OSS / Nginx）。
上传后把 `index.html` 作为默认页即可，不需要服务端。

注意：`tiles/` 目录结构必须保持，OpenSeadragon 按 `hero_files/<层级>/<列>_<行>.jpg` 取图。

## 生成方式

| 步骤 | 脚本 |
|---|---|
| 渲超高清长卷 | `../scripts/render_hires.py`（8000×3200，约 138 秒） |
| 切 DZI 瓦片 | `../scripts/make_dzi.py`（约 7 秒） |
| 渲 8 个机位 | `../scripts/render_tour.py`（约 12 分钟） |

## 双联长卷（同景异时）

`tiles/hero.dzi` 对应一条 **14412 x 2880** 的双联长卷：

- 左半：春夏（青瓦、绿树）
- 右半：冬雪（白屋顶、枯枝、灰水）
- 接缝：纸色缝 + 两道细墨线 + 一层雾带过渡
- 底部两枚朱印：春 / 冬

网页交互：

| 效果 | 触发 |
|---|---|
| 落雪 | 常驻，**只在冬季那一半下雪**（接缝处淡入，不会硬切） |
| 过界雾 | 视口从春夏滑到冬雪时，闪一层白雾 |
| 题句 | 进入冬雪后 0.6 秒浮出「雪一落，南京就变成了金陵」，**3 秒后淡出** |

长卷分两步生成：

    python scripts/add_snow_scroll.py   # 加落雪颗粒 + 接缝雾（约 20 秒）
    python scripts/make_dzi.py          # 重切瓦片（约 40 秒）
