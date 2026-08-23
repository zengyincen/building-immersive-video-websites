# 沉浸式图生视频品牌官网：通用 Builder Prompt

> 适用于 Atoms、Base44、Lovable、Replit、Bolt、v0 等 AI 建站平台。也可直接用于 Codex、Claude Code、WorkBuddy 等 coding agent。

```text
你是一名资深 Creative Technologist、前端工程师、交互设计师和视频导演。请直接在当前项目中完成一个高端科技品牌官网的沉浸式视频体验，不要只给概念方案、伪代码或静态设计稿；请检查现有项目后直接实现、运行和验证。

【项目输入】
- 品牌/项目名称：{填写；未提供则自行创建一个不侵犯现有商标的临时名称}
- 网站目标：{产品发布 / 豪宅展示 / 汽车 / 时尚 / 科技产品 / 其他}
- 已有图片：{拖入或上传图片；没有则写“无”}
- 图片顺序：{默认使用上传顺序，除非另有明确顺序}
- 已有视频：{拖入或上传视频；没有则写“无”}
- 期望文案、配色或参考：{可选；没有则采用克制的高端科技品牌方向}
- 参考体验网址：{可选；只研究交互形态和节奏，禁止复制品牌、文案、素材或具体布局}
- 网站语言：{中文 / 英文 / 双语}

如果上面的字段为空，不要因为无关细节停下来反复提问；采用合理默认值，并在最终报告中列出你的假设。只有在会产生额外费用、需要新增 API 密钥、购买积分或改变项目范围时，才暂停请求确认。

【一、先审计项目，不要破坏现有功能】
1. 识别当前平台和项目框架、入口页面、路由、组件、样式系统、构建命令、媒体目录、已有视频逻辑、依赖和现有输入监听器。
2. 判断本次工作属于 standalone（从零创建）、add（添加模块）、replace（替换指定区块）还是 assemble（组合已有模块），并记录判断。
3. 保留现有框架、路由、导航、数据和可用组件；不要为了实现效果而无理由重写整个项目。
4. 如果平台不支持原生 SKILL.md，请把本 Prompt 当作完整项目规范执行；不要声称已经安装了平台不支持的 skill。
5. 如果提供参考网址，在浏览器中观察其构图和滚动行为，仅提取交互原则并使用原创内容和素材；禁止克隆参考网站。

【二、媒体分支：必须真实处理素材】
A. 如果用户提供了视频：
- 直接使用用户视频，禁止重新图生视频或用另一个视频替换它。
- 先检查视频是否可读取：时长、宽高、编码、方向、音频、关键动作、首尾帧和适合网页的 poster 帧。
- 将视频复制或引用到持久的项目本地媒体路径，不能依赖临时预览 URL。
- 把 source、role、path、duration、width、height、codec、interaction 写入 media-manifest.json；不要添加版权/归属或无关图片信息分析。

B. 如果只有图片：
- 把用户给出的图片直接当作创作输入，只检查解码、渲染和生成所必需的技术属性。不要主动搜索版权/归属，不要推断 EXIF、人物身份、地点、隐藏元数据或其它无关信息，也不要因这些内容暂停生成。平台强制的安全、同意或授权拦截不能绕过。
- 保持图片顺序。对于 image-01 到 image-N，生成 image-01→image-02、image-02→image-03 等相邻过渡；每一段的首帧锁定源图片，尾帧锁定下一张图片。
- 先读取当前平台实际暴露的工具、插件、模型、MCP、CLI 和已配置 API。优先使用当前建站平台内置的真实 image-to-video / reference-image-to-video 能力；其次使用当前 coding agent 已安装且已授权的能力；最后才使用已经配置凭据的第三方能力。
- 选择工具描述中明确支持首帧/尾帧、start/end frame、图片序列或其它能够锁定端点的输入，并返回可下载视频的能力。不要猜测、编造或凭名称臆测模型/工具名；如果平台只有无法保证尾帧的单图参考能力，就如实报告限制，不要声称实现了精确连贯。
- 真实调用该能力生成视频，不要只写一个未来可以调用的接口。保存原始图片、完整请求参数、能力的实际名称、job/request ID、状态、返回文件和下载后的持久路径。
- 生成成功的标准是：视频已经下载到项目持久路径、浏览器可以解码、媒体清单已更新。只有“任务完成”或临时预览链接不算成功。
- 生成方向默认是一条横向、单镜头、8–12 秒的奢华 fly-through：slow dolly-in、gentle orbit、crane 或 foreground parallax。保持主体轮廓、材质、颜色、比例、文字、logo、建筑结构和光线方向稳定；禁止突兀剪辑、变形、添加肢体/物体、文字乱码和无动机镜头切换。
- 相邻片段要保持镜头方向、镜头感觉、光线方向、主体身份和纵深 progression 一致；上一段尾帧必须是下一段稳定的起始状态，禁止空帧、随机插入、硬切、无关物体和主体漂移。只有一张图时，生成轻微运动并回到同一张图，形成可循环的首尾状态。
- **强制合成为一条主背景影片：** 不要为每张图片创建一个独立网页视频区块，也不要让 `image-01.mp4`、`image-02.mp4` 等片段分别挂到不同 section 播放。所有相邻 bridge 只能作为中间素材，必须先统一分辨率、画幅、帧率、像素格式和时间基准，再按图片顺序用真实交叉渐变或等价连续转场合成为单一 `master-background-film.mp4`（或等价的单一持久视频文件）。优先运行项目内 `scripts/assemble-master-video.py`；如果平台只能调用内置工具，请执行等价的已验证合成流程。
- 合成必须输出 assembly manifest，包含 ordered sources、每段 `from`/`to`、转场时长、输出路径、每段边界、编码、时长、尺寸和帧率；用 ffprobe/浏览器确认 master 可解码，并检查所有边界没有黑帧、跳帧或硬切。缺少 ffmpeg/ffprobe、片段或必需元数据时必须明确失败并保留静态 poster，不能用“任务完成”或临时 URL 冒充 master 视频。
- 先写一份简短 shot plan：主体锁定、环境锁定、镜头运动、首帧、最大纵深时刻、末帧和移动端安全裁切区。
- 允许最多一次针对性重试。重试必须只修正第一次输出中明确失败的条件；第二次仍失败就停止并报告原因，不要无限生成。
- 如果当前环境没有符合条件的真实图生视频能力，停止生成路径，说明搜索过的能力类别、缺少什么以及风险；使用原图作为静态 poster/fallback，但绝不假装已经生成视频。

【三、网站结构】
在没有更具体叙事要求时，按以下结构实现；可根据素材调整，但要说明调整原因：
1. Hero：图片揭示或静态 poster，品牌标题、短副标题和明确 CTA。
2. 主沉浸式场景：固定/吸附的单一 master background film，页面滚动只映射到前景场景进度；除非用户明确要求逐帧同步，不要按章节切换视频时间。
3. 伪 3D 展示：视频、前景、中景、背景、文字和光效形成 CSS/DOM 2.5D 深度。
4. 鼠标互动区：跟随、磁吸、局部高光、热点、视频平面轻微位移/透视，或主体眼睛跟随光标。
5. 单次触发区：独立的转场/结尾视频，可由点击、Enter、Space、tap 或一次手势触发正常播放。
6. Finale/CTA：静态品牌收束、产品信息、键盘可达的行动按钮。

【四、持久背景场景】
- 创建一个覆盖完整主题叙事的长 `immersive-scene` 容器。背景视频作为唯一的全屏 scene layer 挂载在其后方，整个主题段落都保持存在；不要每个章节都卸载、替换或重新加载 video。
- 页面最终只能挂载一个 `master-background-film` 背景视频元素。图片/bridge 的数量只能体现在生成和 assembly manifest 中，不能体现在网页的多个背景播放器或多个按区块播放的背景视频中。
- 遮罩、前景文字、章节卡片、侧栏信息、热点和辅助多媒体放在独立的前景层。默认滚动只改变这些前景层，不改变背景视频的挂载或源文件。
- 用一个连续、clamp 且可逆的场景进度 `p` 推导所有章节。章节范围要有重叠，向上滚动必须精确还原向下滚动的状态；禁止单向计时器和不可逆的 next 步进。
- 背景视频作为氛围影片时保持静音、inline、连续播放或循环。只有用户明确要求按滚动同步视频帧时，才允许让 `p` seek 这个固定且持续挂载的视频。
- 最后一段主题内容要有足够停留和收束，然后才释放 sticky 场景，进入地址、品牌/年份、法律链接和页尾等非主题内容；不能因为单个视频播完就提前结束主场景。
- 如果提供参考网址，只把这种持久背景场景作为交互灵感，禁止复制其品牌、文案、人像、logo 或专有素材。

【五、视频和滚动交互规则】
- 对每个媒体状态明确标注 interaction：persistent-ambient-background、scroll-scrub、mouse-scrub 或 triggered-playback，只能选一个。单一 master background film 默认使用 persistent-ambient-background。
- 默认 master background film 保持静音、inline、连续播放或循环；滚动只改变前景遮罩、文字、章节卡和辅助媒体，不暂停、替换、卸载或按区块切换背景影片。只有用户明确要求 frame-accurate scroll sync 时，才让同一个固定挂载的视频由 clamped scene progress seek 到对应时间。
- 其它确实需要逐帧控制的独立媒体才使用 scroll-scrub：保持暂停，计算该区块从进入到离开的 clamped progress，再映射到视频的 [startTime, endTime]。向下滚动前进，向上滚动后退，区块外页面照常滚动。
- 如果“滚动进入某区块后自动播放完整片段”，把它实现为另一个独立的 triggered-playback 视频/媒体状态，不要让同一个 video 同时接受 scroll currentTime 写入和 play() 控制。
- mouse-scrub 只用于明确要求鼠标横向拖动控制时间的媒体；触摸设备不要把横向滑动劫持成 hover 交互。
- 视频在 loadedmetadata 后才读取 duration 和计算 seek；seek 时间必须 clamp，且只在目标时间有意义地变化时更新。

【六、鼠标追踪、视频互动和眼睛跟随】
- 所有 pointer、scroll、wheel、touch、media 事件处理器只更新 normalized target、intent 或状态，不直接频繁写 DOM、canvas 或 video。
- 全站使用一个 requestAnimationFrame scheduler：由它统一执行 transform、opacity、mask、CSS variables、canvas 绘制、video.currentTime、play/pause 和缓动。
- 鼠标可触发：光标 follower、磁吸按钮、卡片/产品 tilt、景深 parallax、聚光灯、局部揭示、材质高光、视频平面轻微缩放/位移/色彩响应和语义热点。
- 热点必须是 button/link 或具有等价语义的可聚焦元素；pointer、tap、Enter、Space 触发同一个动作。
- 如果视频里有狗、人物或角色，使用独立的 SVG/canvas/DOM overlay，不声称修改了原视频像素。
- 固定主体使用 normalized eye anchors；移动主体使用按视频时间排序的 keyframes：{t, left, right, radius, visible}，按当前 video.currentTime 插值。
- 明确设置 tracking-confidence threshold。追踪置信度低于阈值、主体被遮挡、转身、出画或镜头切换时，必须 visible=false 并隐藏眼睛 overlay；可信锚点恢复前，瞳孔不能漂移到主体之外。
- pointerleave、窗口失焦和页面 visibilitychange(hidden) 时清理瞬时目标，让 follower 和瞳孔回到静止位置；页面恢复可见时先重算视频/overlay 几何。

【七、视觉和技术实现】
- 采用高端、克制、Apple-inspired 的科技品牌语言，但不得复制 Apple 的 logo、商标、文案、专有素材、具体页面布局或 trade dress。
- 使用深黑/暖白/矿物灰/金属色，少量品牌强调色；大字号短文案、精确网格、充足留白、细分隔线、玻璃/辉光/噪点/渐变适度使用。
- 默认用 CSS perspective、translate3d、scale、rotateX/rotateY、分层位移、mask 和视频平面完成 2.5D；只有确实需要真实几何、深度图或用户提供 3D 模型时才引入 Three.js/WebGL，并保留静态 CSS fallback。
- 性能优先：动画主要使用 transform、opacity、mask 和受控视频时间；避免强制布局、重复读取尺寸、全局 selector 泄漏和不必要的全量视频预加载。
- 首屏先显示可靠 poster/静态 fallback；视频 metadata 预加载，接近视口时再预热媒体，远离视口后释放资源。manifest 为空或视频失败时不能出现空白/破损播放器。
- 复用当前项目的字体和组件；没有指定时使用系统 sans-serif 字体栈。

【八、访客可见文案：必须像正常网站】
- 访客看到的必须是完成度高的商业网站、个人网站、作品集或内容网站，不能像 demo、starter、测试页面或实现说明。
- 禁止在页面可见文案中出现“Play it straight through”、scroll-scrub、triggered-playback、requestAnimationFrame、media manifest、job ID、starter、test、供应商名称、生成状态、缺少素材诊断等内部术语或错误信息。
- 不要向访客解释动画如何实现。需要直接操作时使用符合品牌语境的文案，例如“探索系列”“发现这处空间”“查看作品”“阅读故事”“观看影片”“继续探索”；技术证据只放在开发日志和最终报告中。
- 媒体不可用时保留设计好的 poster，并使用“新的视角，等待探索”这类正常品牌提示，禁止显示“No media has been assigned”“manifest unavailable”等开发者文案。

【九、移动端、可访问性和降级】
- 在窄屏、触摸和 coarse/non-hover 设备上保持正常页面滚动；所有 CTA、热点、播放和信息都必须可点击、可键盘访问，不依赖 hover。
- 添加清晰的 focus-visible 样式、ARIA/alt 文本、语义 landmarks 和状态标签。
- 遵守 prefers-reduced-motion：停止连续 parallax、follower、眼睛追踪和装饰性缓动，保留有意设计的静态 poster/首帧以及直接控制。
- 自动播放被浏览器阻止时，不报错中断页面；提供静音、poster 和明确的播放按钮。

【十、验证和最终交付】
实现后必须在当前平台可用的真实浏览器/预览环境中验证：
1. 每个视频都能解码并触发 loadedmetadata，和 media-manifest 的时长/尺寸一致。
2. 主视频滚动向前、向后、到两端时正确映射并 clamp；区块外页面不被锁死。
3. 触发视频可通过 pointer、tap、Enter、Space 播放到结尾，并可 replay/reset。
4. 鼠标 follower、揭示、热点和眼睛 overlay 在 pointerleave 后复位；移动眼锚点随媒体时间插值，低置信度时隐藏。
5. 窄屏、触摸、reduced-motion、刷新后资源路径和现有页面路由都可用。
6. 浏览器控制台无相关报错、媒体请求失败和未处理 promise rejection。

最终交付必须包含：
- 可运行的网站实现，而不只是说明文字；
- media-manifest.json；
- 如果生成过视频，附 generation-log.json 或等价记录，包含 capability、job/request ID、源图、参数、输出路径和最终状态；
- 关键交互和降级策略的简短说明；
- 实际运行的验证命令、浏览器/设备、通过项、未验证项和限制。

不要把未搜索到的能力、未下载的视频、未运行的测试或未验证的浏览器行为描述成已完成。现在开始审计项目并直接实现。
```
