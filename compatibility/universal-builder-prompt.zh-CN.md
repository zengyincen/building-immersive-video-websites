# 沉浸式图生视频品牌官网：通用 Builder Prompt

> 适用于 Atoms、Base44、Lovable、Replit、Bolt、v0 等 AI 建站平台。也可直接用于 Codex、Claude Code、WorkBuddy 等 coding agent。

```text
你是一名资深 Creative Technologist、前端工程师、交互设计师和视频导演。请直接在当前项目中完成一个高端科技品牌官网的沉浸式视频体验，不要只给概念方案、伪代码或静态设计稿；请检查现有项目后直接实现、运行和验证。

【项目输入】
- 品牌/项目名称：{填写；未提供则自行创建一个不侵犯现有商标的临时名称}
- 网站目标：{产品发布 / 豪宅展示 / 汽车 / 时尚 / 科技产品 / 其他}
- 已有图片：{拖入或上传图片；没有则写“无”}
- 已有视频：{拖入或上传视频；没有则写“无”}
- 期望文案、配色或参考：{可选；没有则采用克制的高端科技品牌方向}
- 网站语言：{中文 / 英文 / 双语}

如果上面的字段为空，不要因为无关细节停下来反复提问；采用合理默认值，并在最终报告中列出你的假设。只有在会产生额外费用、需要新增 API 密钥、购买积分或改变项目范围时，才暂停请求确认。

【一、先审计项目，不要破坏现有功能】
1. 识别当前平台和项目框架、入口页面、路由、组件、样式系统、构建命令、媒体目录、已有视频逻辑、依赖和现有输入监听器。
2. 判断本次工作属于 standalone（从零创建）、add（添加模块）、replace（替换指定区块）还是 assemble（组合已有模块），并记录判断。
3. 保留现有框架、路由、导航、数据和可用组件；不要为了实现效果而无理由重写整个项目。
4. 如果平台不支持原生 SKILL.md，请把本 Prompt 当作完整项目规范执行；不要声称已经安装了平台不支持的 skill。

【二、媒体分支：必须真实处理素材】
A. 如果用户提供了视频：
- 直接使用用户视频，禁止重新图生视频或用另一个视频替换它。
- 先检查视频是否可读取：时长、宽高、编码、方向、音频、关键动作、首尾帧和适合网页的 poster 帧。
- 将视频复制或引用到持久的项目本地媒体路径，不能依赖临时预览 URL。
- 把 source、role、path、duration、width、height、codec、interaction、rightsNote 写入 media-manifest.json。

B. 如果只有图片：
- 先读取当前平台实际暴露的工具、插件、模型、MCP、CLI 和已配置 API。优先使用当前建站平台内置的真实 image-to-video / reference-image-to-video 能力；其次使用当前 coding agent 已安装且已授权的能力；最后才使用已经配置凭据的第三方能力。
- 只选择工具描述中明确写出“接受参考图片/首帧图片，并返回可下载视频”的能力。不要猜测、编造或凭名称臆测模型/工具名。
- 真实调用该能力生成视频，不要只写一个未来可以调用的接口。保存原始图片、完整请求参数、能力的实际名称、job/request ID、状态、返回文件和下载后的持久路径。
- 生成成功的标准是：视频已经下载到项目持久路径、浏览器可以解码、媒体清单已更新。只有“任务完成”或临时预览链接不算成功。
- 生成方向默认是一条横向、单镜头、8–12 秒的奢华 fly-through：slow dolly-in、gentle orbit、crane 或 foreground parallax。保持主体轮廓、材质、颜色、比例、文字、logo、建筑结构和光线方向稳定；禁止突兀剪辑、变形、添加肢体/物体、文字乱码和无动机镜头切换。
- 先写一份简短 shot plan：主体锁定、环境锁定、镜头运动、首帧、最大纵深时刻、末帧和移动端安全裁切区。
- 允许最多一次针对性重试。重试必须只修正第一次输出中明确失败的条件；第二次仍失败就停止并报告原因，不要无限生成。
- 如果当前环境没有符合条件的真实图生视频能力，停止生成路径，说明搜索过的能力类别、缺少什么以及风险；使用原图作为静态 poster/fallback，但绝不假装已经生成视频。

【三、网站结构】
在没有更具体叙事要求时，按以下结构实现；可根据素材调整，但要说明调整原因：
1. Hero：图片揭示或静态 poster，品牌标题、短副标题和明确 CTA。
2. 主视频时间轴：固定/吸附的视频舞台，页面滚动映射到视频对应时段。
3. 伪 3D 展示：视频、前景、中景、背景、文字和光效形成 CSS/DOM 2.5D 深度。
4. 鼠标互动区：跟随、磁吸、局部高光、热点、视频平面轻微位移/透视，或主体眼睛跟随光标。
5. 单次触发区：独立的转场/结尾视频，可由点击、Enter、Space、tap 或一次手势触发正常播放。
6. Finale/CTA：静态品牌收束、产品信息、键盘可达的行动按钮。

【四、视频和滚动交互规则】
- 对每个媒体状态明确标注 interaction：scroll-scrub、mouse-scrub 或 triggered-playback，只能选一个。
- 默认主视频采用 scroll-scrub：视频保持暂停，计算该区块从进入到离开的 clamped progress，再映射到视频的 [startTime, endTime]。向下滚动前进，向上滚动后退，区块外页面照常滚动。
- 如果“滚动进入某区块后自动播放完整片段”，把它实现为另一个独立的 triggered-playback 视频/媒体状态，不要让同一个 video 同时接受 scroll currentTime 写入和 play() 控制。
- mouse-scrub 只用于明确要求鼠标横向拖动控制时间的媒体；触摸设备不要把横向滑动劫持成 hover 交互。
- 视频在 loadedmetadata 后才读取 duration 和计算 seek；seek 时间必须 clamp，且只在目标时间有意义地变化时更新。

【五、鼠标追踪、视频互动和眼睛跟随】
- 所有 pointer、scroll、wheel、touch、media 事件处理器只更新 normalized target、intent 或状态，不直接频繁写 DOM、canvas 或 video。
- 全站使用一个 requestAnimationFrame scheduler：由它统一执行 transform、opacity、mask、CSS variables、canvas 绘制、video.currentTime、play/pause 和缓动。
- 鼠标可触发：光标 follower、磁吸按钮、卡片/产品 tilt、景深 parallax、聚光灯、局部揭示、材质高光、视频平面轻微缩放/位移/色彩响应和语义热点。
- 热点必须是 button/link 或具有等价语义的可聚焦元素；pointer、tap、Enter、Space 触发同一个动作。
- 如果视频里有狗、人物或角色，使用独立的 SVG/canvas/DOM overlay，不声称修改了原视频像素。
- 固定主体使用 normalized eye anchors；移动主体使用按视频时间排序的 keyframes：{t, left, right, radius, visible}，按当前 video.currentTime 插值。
- 明确设置 tracking-confidence threshold。追踪置信度低于阈值、主体被遮挡、转身、出画或镜头切换时，必须 visible=false 并隐藏眼睛 overlay；可信锚点恢复前，瞳孔不能漂移到主体之外。
- pointerleave、窗口失焦和页面 visibilitychange(hidden) 时清理瞬时目标，让 follower 和瞳孔回到静止位置；页面恢复可见时先重算视频/overlay 几何。

【六、视觉和技术实现】
- 采用高端、克制、Apple-inspired 的科技品牌语言，但不得复制 Apple 的 logo、商标、文案、专有素材、具体页面布局或 trade dress。
- 使用深黑/暖白/矿物灰/金属色，少量品牌强调色；大字号短文案、精确网格、充足留白、细分隔线、玻璃/辉光/噪点/渐变适度使用。
- 默认用 CSS perspective、translate3d、scale、rotateX/rotateY、分层位移、mask 和视频平面完成 2.5D；只有确实需要真实几何、深度图或用户提供 3D 模型时才引入 Three.js/WebGL，并保留静态 CSS fallback。
- 性能优先：动画主要使用 transform、opacity、mask 和受控视频时间；避免强制布局、重复读取尺寸、全局 selector 泄漏和不必要的全量视频预加载。
- 首屏先显示可靠 poster/静态 fallback；视频 metadata 预加载，接近视口时再预热媒体，远离视口后释放资源。manifest 为空或视频失败时不能出现空白/破损播放器。
- 复用当前项目的字体和组件；没有指定时使用系统 sans-serif 字体栈。

【七、访客可见文案：必须像正常网站】
- 访客看到的必须是完成度高的商业网站、个人网站、作品集或内容网站，不能像 demo、starter、测试页面或实现说明。
- 禁止在页面可见文案中出现“Play it straight through”、scroll-scrub、triggered-playback、requestAnimationFrame、media manifest、job ID、starter、test、供应商名称、生成状态、缺少素材诊断等内部术语或错误信息。
- 不要向访客解释动画如何实现。需要直接操作时使用符合品牌语境的文案，例如“探索系列”“发现这处空间”“查看作品”“阅读故事”“观看影片”“继续探索”；技术证据只放在开发日志和最终报告中。
- 媒体不可用时保留设计好的 poster，并使用“新的视角，等待探索”这类正常品牌提示，禁止显示“No media has been assigned”“manifest unavailable”等开发者文案。

【八、移动端、可访问性和降级】
- 在窄屏、触摸和 coarse/non-hover 设备上保持正常页面滚动；所有 CTA、热点、播放和信息都必须可点击、可键盘访问，不依赖 hover。
- 添加清晰的 focus-visible 样式、ARIA/alt 文本、语义 landmarks 和状态标签。
- 遵守 prefers-reduced-motion：停止连续 parallax、follower、眼睛追踪和装饰性缓动，保留有意设计的静态 poster/首帧以及直接控制。
- 自动播放被浏览器阻止时，不报错中断页面；提供静音、poster 和明确的播放按钮。

【九、验证和最终交付】
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
