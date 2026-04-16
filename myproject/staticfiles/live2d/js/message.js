// 使用demo.html中定义的home_Path变量
if(typeof home_Path === 'undefined') {
	var home_Path = document.location.protocol +'//' + window.document.location.hostname +'/';
}

// 语音合成配置
var speechEnabled = true; // 是否启用语音
var speechVolume = 1.0; // 音量 0-1
var speechRate = 1.0; // 语速 0.1-10
var speechPitch = 1.0; // 音调 0-2
var speechVoice = null; // 语音声音
var speechLang = 'zh-CN'; // 语音语言
var currentUtterance = null; // 当前正在播放的语音

var userAgent = window.navigator.userAgent.toLowerCase();
console.log(userAgent);
var norunAI = [ "android", "iphone", "ipod", "ipad", "windows phone", "mqqbrowser" ,"msie","trident/7.0"];
var norunFlag = false;


for(var i=0;i<norunAI.length;i++){
	if(userAgent.indexOf(norunAI[i]) > -1){
		norunFlag = true;
		break;
	}
}

if(!window.WebGLRenderingContext){
	norunFlag = true;
}

if(!norunFlag){
	var hitFlag = false;
	var AIFadeFlag = false;
	var liveTlakTimer = null;
	var sleepTimer_ = null;
	var AITalkFlag = false;
	var talkNum = 0;
	
	// 初始化语音合成
	function initSpeechSynthesis() {
		// 检查浏览器是否支持语音合成
		if ('speechSynthesis' in window) {
			console.log('语音合成已初始化');
			
			// 获取可用的语音列表
			window.speechSynthesis.onvoiceschanged = function() {
				var voices = window.speechSynthesis.getVoices();
				// 尝试找到中文语音
				for (var i = 0; i < voices.length; i++) {
					if (voices[i].lang.indexOf('zh') !== -1) {
						speechVoice = voices[i];
						console.log('已选择语音：', speechVoice.name);
						break;
					}
				}
				
				// 如果没有找到中文语音，使用默认语音
				if (!speechVoice && voices.length > 0) {
					speechVoice = voices[0];
					console.log('未找到中文语音，使用默认语音：', speechVoice.name);
				}
			};
			
			// 触发voices加载
			window.speechSynthesis.getVoices();
		} else {
			console.warn('当前浏览器不支持语音合成');
			speechEnabled = false;
		}
	}
	
	// 语音播报函数
	function speakText(text) {
		// 如果语音未启用或浏览器不支持，直接返回
		if (!speechEnabled || !('speechSynthesis' in window)) {
			return;
		}
		
		// 如果有正在播放的语音，先停止
		if (currentUtterance) {
			window.speechSynthesis.cancel();
		}
		
		// 创建一个新的语音实例
		var utterance = new SpeechSynthesisUtterance();
		
		// 去除HTML标签，只保留纯文本
		var tempDiv = document.createElement('div');
		tempDiv.innerHTML = text;
		utterance.text = tempDiv.textContent || tempDiv.innerText || '';
		
		// 设置语音参数
		utterance.volume = speechVolume; // 音量
		utterance.rate = speechRate;     // 语速
		utterance.pitch = speechPitch;   // 音调
		utterance.lang = speechLang;     // 语言
		
		// 如果有可用的语音，设置语音
		if (speechVoice) {
			utterance.voice = speechVoice;
		}
		
		// 保存当前语音实例
		currentUtterance = utterance;
		
		// 播放语音
		window.speechSynthesis.speak(utterance);
		
		// 语音播放结束后清除当前语音实例
		utterance.onend = function() {
			currentUtterance = null;
		};
		
		// 语音播放错误处理
		utterance.onerror = function(event) {
			console.error('语音播放错误:', event);
			currentUtterance = null;
		};
	}
	
	// 初始化语音合成
	initSpeechSynthesis();
	(function (){
		function renderTip(template, context) {
			var tokenReg = /(\\)?\{([^\{\}\\]+)(\\)?\}/g;
			return template.replace(tokenReg, function (word, slash1, token, slash2) {
				if (slash1 || slash2) {
					return word.replace('\\', '');
				}
				var variables = token.replace(/\s/g, '').split('.');
				var currentObject = context;
				var i, length, variable;
				for (i = 0, length = variables.length; i < length; ++i) {
					variable = variables[i];
					currentObject = currentObject[variable];
					if (currentObject === undefined || currentObject === null) return '';
				}
				return currentObject;
			});
		}
		
		String.prototype.renderTip = function (context) {
			return renderTip(this, context);
		};
		
		var re = /x/;
		re.toString = function() {
			showMessage('哈哈，你打开了控制台，是想要看看我的秘密吗？', 5000);
			return '';
		};
		
		$(document).on('copy', function (){
			showMessage('你都复制了些什么呀，转载要记得加上出处哦~~', 5000);
		});
		
		function initTips(){
			$.ajax({
				cache: true,
				url: message_Path+'message.json',
				dataType: "json",
				success: function (result){
					$.each(result.mouseover, function (index, tips){
						$(tips.selector).mouseover(function (){
							var text = tips.text;
							if(Array.isArray(tips.text)) text = tips.text[Math.floor(Math.random() * tips.text.length + 1)-1];
							text = text.renderTip({text: $(this).text()});
							showMessage(text, 3000);
							talkValTimer();
							clearInterval(liveTlakTimer);
							liveTlakTimer = null;
						});
						$(tips.selector).mouseout(function (){
							showHitokoto();
							if(liveTlakTimer == null){
								liveTlakTimer = window.setInterval(function(){
									showHitokoto();
								},15000);
							};
						});
					});
					$.each(result.click, function (index, tips){
						$(tips.selector).click(function (){
							if(hitFlag){
								return false
							}
							hitFlag = true;
							setTimeout(function(){
								hitFlag = false;
							},8000);
							var text = tips.text;
							if(Array.isArray(tips.text)) text = tips.text[Math.floor(Math.random() * tips.text.length + 1)-1];
							text = text.renderTip({text: $(this).text()});
							showMessage(text, 3000);
						});
						clearInterval(liveTlakTimer);
						liveTlakTimer = null;
						if(liveTlakTimer == null){
							liveTlakTimer = window.setInterval(function(){
								showHitokoto();
							},15000);
						};
					});
				}
			});
		}
		initTips();
	
		var text;
		if(document.referrer !== ''){
			var referrer = document.createElement('a');
			referrer.href = document.referrer;
			text = '嗨！来自 <span style="color:#0099cc;">' + referrer.hostname + '</span> 的朋友！';
			var domain = referrer.hostname.split('.')[1];
			if (domain == 'baidu') {
				text = '嗨！ 来自 百度搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' + document.title.split(' - ')[0] + ' 」</span>';
			}else if (domain == 'so') {
				text = '嗨！ 来自 360搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' + document.title.split(' - ')[0] + ' 」</span>';
			}else if (domain == 'google') {
				text = '嗨！ 来自 谷歌搜索 的朋友！<br>欢迎访问<span style="color:#0099cc;">「 ' + document.title.split(' - ')[0] + ' 」</span>';
			}
		}else {
			if (window.location.href == home_Path) { //主页URL判断，需要斜杠结尾
				var now = (new Date()).getHours();
				if (now > 23 || now <= 5) {
					text = '你是夜猫子呀？这么晚还不睡觉，明天起的来嘛？';
				} else if (now > 5 && now <= 7) {
					text = '早上好！一日之计在于晨，美好的一天就要开始了！';
				} else if (now > 7 && now <= 11) {
					text = '上午好！工作顺利嘛，不要久坐，多起来走动走动哦！';
				} else if (now > 11 && now <= 14) {
					text = '中午了，工作了一个上午，现在是午餐时间！';
				} else if (now > 14 && now <= 17) {
					text = '午后很容易犯困呢，今天的运动目标完成了吗？';
				} else if (now > 17 && now <= 19) {
					text = '傍晚了！窗外 sunset 的景色很美丽呢，最美不过 sunset red~~';
				} else if (now > 19 && now <= 21) {
					text = '晚上好，今天过得怎么样？';
				} else if (now > 21 && now <= 23) {
					text = '已经这么晚了呀，早点休息吧，晚安~~';
				} else {
					text = '嗨~ 快来逗我玩吧！';
				}
			}else {
				text = `欢迎阅读<span style="color:#0099cc;">「 ${document.title.split(' - ')[0]} 」</span>`;
			}
		}
		showMessage(text, 12000);
	})();
	
	liveTlakTimer = setInterval(function(){
		showHitokoto();
	},15000);
	
	// 获取页面内容的函数
	function getPageContent() {
		// 创建一个对象来存储页面信息
		var pageInfo = {
			title: document.title,
			url: window.location.href,
			headings: [],
			mainText: "",
			metaDescription: ""
		};

		// 获取meta描述
		var metaDesc = document.querySelector('meta[name="description"]');
		if (metaDesc) {
			pageInfo.metaDescription = metaDesc.getAttribute('content');
		}

		// 获取所有标题
		var headings = document.querySelectorAll('h1, h2, h3');
		headings.forEach(function(heading) {
			if (heading.textContent.trim() !== "") {
				pageInfo.headings.push({
					level: heading.tagName.toLowerCase(),
					text: heading.textContent.trim()
				});
			}
		});

		// 获取主要内容
		// 尝试找到主要内容区域 (通常在article, main, #content, .content等标签中)
		var mainContent = document.querySelector('article, main, #content, .content, .post, .entry, .page-content');
		if (mainContent) {
			pageInfo.mainText = mainContent.textContent.trim().substring(0, 1000); // 限制长度
		} else {
			// 如果找不到明确的内容区域，获取body中的所有段落文本
			var paragraphs = document.querySelectorAll('p');
			var allText = "";
			paragraphs.forEach(function(p) {
				if (p.textContent.trim().length > 20) { // 只获取有意义的段落
					allText += p.textContent.trim() + "\n";
				}
			});
			pageInfo.mainText = allText.substring(0, 1000); // 限制长度
		}

		return pageInfo;
	}

	// 使用大模型介绍页面内容
	function introducePageContent() {
		if (!talkAPI || talkAPI === "") {
			console.warn("未配置talkAPI，无法介绍页面内容");
			return;
		}

		var pageInfo = getPageContent();
		var userid_ = sessionStorage.getItem("live2duser") || "visitor";

		// 构建提示信息
		var prompt = "请简单介绍一下我正在浏览的页面内容。页面信息如下：\n";
		prompt += "标题：" + pageInfo.title + "\n";
		
		if (pageInfo.metaDescription) {
			prompt += "描述：" + pageInfo.metaDescription + "\n";
		}

		if (pageInfo.headings.length > 0) {
			prompt += "主要标题：\n";
			pageInfo.headings.slice(0, 3).forEach(function(heading) { // 最多显示3个标题
				prompt += "- " + heading.text + "\n";
			});
		}

		if (pageInfo.mainText) {
			prompt += "页面内容摘要：" + pageInfo.mainText.substring(0, 300) + "...\n";
		}

		// 显示思考中的消息
		showMessage('我正在了解这个页面...', 0);

		// 调用API获取页面介绍
		fetch(talkAPI, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"message": prompt,
				"userid": userid_,
				"context": "page_introduction"
			})
		})
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			return response.body.getReader();
		})
		.then(reader => {
			const decoder = new TextDecoder('utf-8', { fatal: false });
			let currentMessage = '';
			$('.message').fadeTo(200, 1);

			// 如果有正在播放的语音，先停止
			if (currentUtterance) {
				window.speechSynthesis.cancel();
				currentUtterance = null;
			}

			// 用于存储完整的响应文本，用于语音播报
			let fullResponseText = '';

			function readStream() {
				return reader.read().then(({ done, value }) => {
					if (done) {
						// 流结束后，播放完整的响应文本
						if (speechEnabled && fullResponseText) {
							// 过滤掉表情符号和特殊字符，提高语音质量
							var cleanText = fullResponseText.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27FF]/g, '');
							speakText(cleanText);
						}
						return;
					}

					try {
						const chunk = decoder.decode(value, { stream: true });
						const cleanedChunk = chunk
							.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '')
							.replace(/[\x7F-\x9F]/g, '')
							.replace(/\uFFFD/g, '');
						
						currentMessage += cleanedChunk;
						
						// 更新用于语音播报的完整文本
						fullResponseText = $('<div>').html(currentMessage).text();
						
						let displayContent = currentMessage;
						if (typeof marked === 'function') {
							try {
								displayContent = marked.parse(currentMessage, { 
									sanitize: true,
									breaks: true,
									gfm: true
								});
							} catch (e) {
								displayContent = currentMessage
									.replace(/&/g, '&amp;')
									.replace(/</g, '&lt;')
									.replace(/>/g, '&gt;')
									.replace(/"/g, '&quot;')
									.replace(/\n/g, '<br>');
							}
						} else {
							displayContent = currentMessage
								.replace(/&/g, '&amp;')
								.replace(/</g, '&lt;')
								.replace(/>/g, '&gt;')
								.replace(/"/g, '&quot;')
								.replace(/\n/g, '<br>');
						}
						
						$('.message').html(displayContent);
						talkValTimer();
						
						return readStream();
					} catch (error) {
						console.error('解码错误:', error);
						showMessage('抱歉，我无法正确解析页面内容。', 0);
					}
				});
			}

			return readStream();
		})
		.catch(error => {
			console.error('获取页面介绍失败:', error);
			showMessage('抱歉，我无法获取页面的介绍信息。', 0);
		});
	}

	function showHitokoto(){
		if(sessionStorage.getItem("Sleepy")!=="1"){
			if(!AITalkFlag){
				// 随机决定行为：一言、表情或页面介绍
				var randomAction = Math.random();
				
				// 15%概率介绍页面内容（如果不是首页）
				if(randomAction < 0.05 && window.location.href !== home_Path) {
					introducePageContent();
					return;
				}
				
				// 25%概率做一个随机动作
				if(randomAction < 0.4) {
					var actions = ['normal', 'happy', 'shy', 'wink', 'surprised', 'sad'];
					var randomIndex = Math.floor(Math.random() * actions.length);
					console.log('随机表情: ' + actions[randomIndex]);
				}
				
				// 60%概率获取一言
				$.getJSON('https://v1.hitokoto.cn/',function(result){
					talkValTimer();
					// 添加表情符号增强情感表达
					var emotions = ['😊', '🤔', '😄', '😌', '🙂', '😎', '🧐', '✨'];
					var randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
					
					// 根据内容添加适当的表情
					var content = result.hitokoto;
					if(content.includes('开心') || content.includes('快乐') || content.includes('喜欢')) {
						randomEmotion = '😄';
					} else if(content.includes('思考') || content.includes('想') || content.includes('认为')) {
						randomEmotion = '🤔';
					} else if(content.includes('伤心') || content.includes('难过') || content.includes('痛苦')) {
						randomEmotion = '😢';
					}
					
					showMessage(randomEmotion + ' ' + content, 0);
				});
			}
		}else{
			hideMessage(0);
			if(sleepTimer_==null){
				sleepTimer_ = setInterval(function(){
					checkSleep();
				},200);
			}
			console.log(sleepTimer_);
		}
	}
	
	function checkSleep(){
		var sleepStatu = sessionStorage.getItem("Sleepy");
		if(sleepStatu!=='1'){
			talkValTimer();
			// 随机欢迎语
			var welcomeMessages = [
				'你回来啦~ 我好想你！',
				'哇，终于等到你了！',
				'欢迎回来！我刚刚在想你呢~',
				'你好啊！今天过得怎么样？',
				'嘿！我正好有事想和你聊聊！',
				'太好了，你回来了！'
			];
			var randomIndex = Math.floor(Math.random() * welcomeMessages.length);
			showMessage(welcomeMessages[randomIndex], 0);
			clearInterval(sleepTimer_);
			sleepTimer_= null;
		}
	}
	
	function showMessage(text, timeout){
		if(Array.isArray(text)) text = text[Math.floor(Math.random() * text.length + 1)-1];
		//console.log('showMessage', text);
		$('.message').stop();
		
		var processedText = text; // Default to original text
		try {
			if (typeof marked === 'function') {
				// WARNING: marked.parse() does not sanitize HTML. Ensure input is trusted or sanitize separately.
				processedText = marked.parse(text);
			} else {
				console.warn('marked.js not found or not loaded correctly. Markdown rendering disabled.');
			}
		} catch (e) {
			console.error('Error parsing Markdown:', e);
			// Fallback to original text if parsing fails
			processedText = text;
		}

		// 播放语音
		if (speechEnabled) {
			// 提取纯文本用于语音播报
			var speechText = $('<div>').html(text).text();
			// 过滤掉表情符号和特殊字符，提高语音质量
			speechText = speechText.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27FF]/g, '');
			// 调用语音合成
			speakText(speechText);
		}

		// 添加打字机效果
		var typingSpeed = 50; // 打字速度(ms)
		var i = 0;
		var messageElement = $('.message');
		messageElement.html(''); // 清空现有内容
		messageElement.fadeTo(200, 1);

		// 创建一个临时div来处理HTML实体并获取纯文本长度用于打字机
		var tempDiv = $('<div>').html(processedText);
		var plainText = tempDiv.text(); // 获取纯文本内容
		var htmlContent = tempDiv.html(); // 获取处理后的HTML内容

		// 如果纯文本很短，或者不是打字机效果的场景（例如，timeout为0的即时消息），直接显示完整HTML
		if(plainText.length < 10 || timeout === 0) {
			messageElement.html(htmlContent);
			// 如果需要，在这里处理 timeout 逻辑 (原代码注释掉了 hideMessage)
			// if (timeout > 0) hideMessage(timeout);
			return;
		}

		// 否则使用打字机效果 (注意：打字机效果作用于纯文本，最后设置完整HTML)
		var currentHtml = '';
		var charIndex = 0;
		var typingEffect = setInterval(function() {
			if(charIndex < plainText.length) {
				// 逐步构建显示的文本，这里简单处理，可能无法完美还原复杂HTML的打字效果
				// 更好的方式可能是逐字显示纯文本，结束后替换为完整HTML
				messageElement.html(plainText.substring(0, charIndex + 1));
				charIndex++;
			} else {
				clearInterval(typingEffect);
				messageElement.html(htmlContent); // 打字结束后显示完整HTML
				// 如果需要，在这里处理 timeout 逻辑
				// if (timeout > 0) hideMessage(timeout);
			}
		}, typingSpeed);

		//if (timeout === null) timeout = 5000;
		//hideMessage(timeout);
	}
	function talkValTimer(){
		$('#live_talk').val('1');
	}
	
	function hideMessage(timeout){
		//$('.message').stop().css('opacity',1);
		if (timeout === null) timeout = 5000;
		$('.message').delay(timeout).fadeTo(200, 0);
	}
	
	function initLive2d (){
		// 添加语音控制面板
		var speechControlHtml = `
		<div class="live2d-speech-control" style="display:none; position:absolute; bottom:5px; left:0; right:0; background:rgba(255,255,255,0.95); border-radius:12px; padding:15px; z-index:10; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.15); backdrop-filter:blur(5px); transition:all 0.3s ease;">
			<div style="margin-bottom:12px; display:flex; align-items:center; justify-content:center;">
				<label class="speech-toggle" style="position:relative; display:inline-block; width:50px; height:24px; margin-right:10px;">
					<input type="checkbox" id="live2d-speech-enabled" ${speechEnabled ? 'checked' : ''} style="opacity:0; width:0; height:0;">
					<span style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#ccc; transition:.4s; border-radius:24px;">
						<span style="position:absolute; content:''; height:16px; width:16px; left:4px; bottom:4px; background-color:white; transition:.4s; border-radius:50%; transform:${speechEnabled ? 'translateX(26px)' : 'translateX(0)'}"></span>
					</span>
				</label>
				<span style="font-weight:500; color:#333;">启用语音</span>
			</div>
			<div style="margin-bottom:12px;">
				<div style="display:flex; align-items:center; margin-bottom:6px;">
					<label style="flex:1; text-align:left; font-size:13px; color:#555;">音量</label>
					<span style="font-size:12px; color:#888; margin-left:5px;">${Math.round(speechVolume * 100)}%</span>
				</div>
				<input type="range" id="live2d-speech-volume" min="0" max="1" step="0.1" value="${speechVolume}" 
					style="width:100%; height:5px; border-radius:5px; -webkit-appearance:none; background:linear-gradient(to right, #4e9eff ${speechVolume*100}%, #e0e0e0 ${speechVolume*100}%);">
			</div>
			<div style="margin-bottom:12px;">
				<div style="display:flex; align-items:center; margin-bottom:6px;">
					<label style="flex:1; text-align:left; font-size:13px; color:#555;">语速</label>
					<span style="font-size:12px; color:#888; margin-left:5px;">${speechRate}x</span>
				</div>
				<input type="range" id="live2d-speech-rate" min="0.5" max="2" step="0.1" value="${speechRate}" 
					style="width:100%; height:5px; border-radius:5px; -webkit-appearance:none; background:linear-gradient(to right, #4e9eff ${(speechRate-0.5)/1.5*100}%, #e0e0e0 ${(speechRate-0.5)/1.5*100}%);">
			</div>
			<div style="margin-bottom:12px;">
				<div style="display:flex; align-items:center; margin-bottom:6px;">
					<label style="flex:1; text-align:left; font-size:13px; color:#555;">音调</label>
					<span style="font-size:12px; color:#888; margin-left:5px;">${speechPitch}x</span>
				</div>
				<input type="range" id="live2d-speech-pitch" min="0.5" max="2" step="0.1" value="${speechPitch}" 
					style="width:100%; height:5px; border-radius:5px; -webkit-appearance:none; background:linear-gradient(to right, #4e9eff ${(speechPitch-0.5)/1.5*100}%, #e0e0e0 ${(speechPitch-0.5)/1.5*100}%);">
			</div>
			<div style="margin-top:15px; display:flex; justify-content:space-between;">
				<button id="live2d-speech-test" style="flex:1; padding:8px 0; margin-right:8px; background:#4e9eff; color:white; border:none; border-radius:6px; cursor:pointer; font-weight:500; transition:all 0.2s ease; box-shadow:0 2px 5px rgba(78,158,255,0.3);">测试语音</button>
				<button id="live2d-speech-close" style="flex:1; padding:8px 0; background:#f5f5f5; color:#555; border:none; border-radius:6px; cursor:pointer; font-weight:500; transition:all 0.2s ease;">关闭</button>
			</div>
		</div>
		`;
		
		// 添加语音设置按钮
		var speechSettingButton = `<button id="live2d-speech-setting" style="position:absolute; bottom:5px; right:5px; background:rgba(255,255,255,0.7); border:none; color:#4e9eff; font-size:20px; cursor:pointer; z-index:9; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:all 0.2s ease;">🔊</button>`;
		
		// 添加滑块样式
		var sliderStyle = document.createElement('style');
		sliderStyle.innerHTML = `
			/* 滑块样式 */
			input[type=range] {
				-webkit-appearance: none;
				margin: 10px 0;
				width: 100%;
			}
			input[type=range]:focus {
				outline: none;
			}
			input[type=range]::-webkit-slider-runnable-track {
				width: 100%;
				height: 5px;
				cursor: pointer;
				background: #e0e0e0;
				border-radius: 5px;
			}
			input[type=range]::-webkit-slider-thumb {
				height: 16px;
				width: 16px;
				border-radius: 50%;
				background: #4e9eff;
				cursor: pointer;
				-webkit-appearance: none;
				margin-top: -5.5px;
				box-shadow: 0 1px 3px rgba(0,0,0,0.2);
				transition: all 0.2s ease;
			}
			input[type=range]::-webkit-slider-thumb:hover {
				background: #3d8eff;
				transform: scale(1.1);
			}
			/* 开关按钮悬停效果 */
			#live2d-speech-setting:hover {
				background: rgba(255,255,255,0.9);
				color: #3d8eff;
				transform: scale(1.05);
			}
			/* 控制面板按钮悬停效果 */
			#live2d-speech-test:hover {
				background: #3d8eff;
				transform: translateY(-2px);
				box-shadow: 0 4px 8px rgba(78,158,255,0.4);
			}
			#live2d-speech-close:hover {
				background: #ebebeb;
				transform: translateY(-2px);
			}
		`;
		document.head.appendChild(sliderStyle);
		
		// 将控制面板和按钮添加到landlord元素中
		$('#landlord').append(speechControlHtml);
		$('#landlord').append(speechSettingButton);
		
		// 绑定语音控制面板事件
		$('#live2d-speech-setting').on('click', function() {
			$('.live2d-speech-control').slideToggle(200);
		});
		
		$('#live2d-speech-close').on('click', function() {
			$('.live2d-speech-control').slideUp(200);
		});
		
		$('#live2d-speech-enabled').on('change', function() {
			speechEnabled = $(this).prop('checked');
			localStorage.setItem('live2d-speech-enabled', speechEnabled ? '1' : '0');
			// 更新开关按钮样式
			$(this).next().find('span').css('transform', speechEnabled ? 'translateX(26px)' : 'translateX(0)');
		});
		
		$('#live2d-speech-volume').on('input', function() {
			speechVolume = parseFloat($(this).val());
			localStorage.setItem('live2d-speech-volume', speechVolume);
			// 更新滑块背景和显示值
			$(this).css('background', `linear-gradient(to right, #4e9eff ${speechVolume*100}%, #e0e0e0 ${speechVolume*100}%)`);
			$(this).parent().find('div:first').find('span:last').text(`${Math.round(speechVolume * 100)}%`);
		});
		
		$('#live2d-speech-rate').on('input', function() {
			speechRate = parseFloat($(this).val());
			localStorage.setItem('live2d-speech-rate', speechRate);
			// 更新滑块背景和显示值
			$(this).css('background', `linear-gradient(to right, #4e9eff ${(speechRate-0.5)/1.5*100}%, #e0e0e0 ${(speechRate-0.5)/1.5*100}%)`);
			$(this).parent().find('div:first').find('span:last').text(`${speechRate}x`);
		});
		
		$('#live2d-speech-pitch').on('input', function() {
			speechPitch = parseFloat($(this).val());
			localStorage.setItem('live2d-speech-pitch', speechPitch);
			// 更新滑块背景和显示值
			$(this).css('background', `linear-gradient(to right, #4e9eff ${(speechPitch-0.5)/1.5*100}%, #e0e0e0 ${(speechPitch-0.5)/1.5*100}%)`);
			$(this).parent().find('div:first').find('span:last').text(`${speechPitch}x`);
		});
		
		$('#live2d-speech-test').on('click', function() {
			if (speechEnabled) {
				speakText('语音测试，当前设置音量' + speechVolume + '，语速' + speechRate + '，音调' + speechPitch);
			} else {
				alert('请先启用语音功能');
			}
		});
		
		// 从localStorage加载语音设置
		function loadSpeechSettings() {
			var enabled = localStorage.getItem('live2d-speech-enabled');
			if (enabled !== null) {
				speechEnabled = enabled === '1';
				$('#live2d-speech-enabled').prop('checked', speechEnabled);
				// 更新开关按钮样式
				$('#live2d-speech-enabled').next().find('span').css('transform', speechEnabled ? 'translateX(26px)' : 'translateX(0)');
			}
			
			var volume = localStorage.getItem('live2d-speech-volume');
			if (volume !== null) {
				speechVolume = parseFloat(volume);
				$('#live2d-speech-volume').val(speechVolume);
				// 更新滑块背景和显示值
				$('#live2d-speech-volume').css('background', `linear-gradient(to right, #4e9eff ${speechVolume*100}%, #e0e0e0 ${speechVolume*100}%)`);
				$('#live2d-speech-volume').parent().find('div:first').find('span:last').text(`${Math.round(speechVolume * 100)}%`);
			}
			
			var rate = localStorage.getItem('live2d-speech-rate');
			if (rate !== null) {
				speechRate = parseFloat(rate);
				$('#live2d-speech-rate').val(speechRate);
				// 更新滑块背景和显示值
				$('#live2d-speech-rate').css('background', `linear-gradient(to right, #4e9eff ${(speechRate-0.5)/1.5*100}%, #e0e0e0 ${(speechRate-0.5)/1.5*100}%)`);
				$('#live2d-speech-rate').parent().find('div:first').find('span:last').text(`${speechRate}x`);
			}
			
			var pitch = localStorage.getItem('live2d-speech-pitch');
			if (pitch !== null) {
				speechPitch = parseFloat(pitch);
				$('#live2d-speech-pitch').val(speechPitch);
				// 更新滑块背景和显示值
				$('#live2d-speech-pitch').css('background', `linear-gradient(to right, #4e9eff ${(speechPitch-0.5)/1.5*100}%, #e0e0e0 ${(speechPitch-0.5)/1.5*100}%)`);
				$('#live2d-speech-pitch').parent().find('div:first').find('span:last').text(`${speechPitch}x`);
			}
		}
		
		// 加载语音设置
		loadSpeechSettings();
		
		// 原有的Live2D控制按钮
		$('#hideButton').on('click', function(){
			if(AIFadeFlag){
				return false;
			}else{
				AIFadeFlag = true;
				localStorage.setItem("live2dhidden", "0");
				$('#landlord').fadeOut(200);
				$('#open_live2d').delay(200).fadeIn(200);
				setTimeout(function(){
					AIFadeFlag = false;
				},300);
			}
		});
		$('#open_live2d').on('click', function(){
			if(AIFadeFlag){
				return false;
			}else{
				AIFadeFlag = true;
				localStorage.setItem("live2dhidden", "1");
				$('#open_live2d').fadeOut(200);
				$('#landlord').delay(200).fadeIn(200);
				setTimeout(function(){
					AIFadeFlag = false;
				},300);
			}
		});
		$('#youduButton').on('click',function(){
			if($('#youduButton').hasClass('doudong')){
				var typeIs = $('#youduButton').attr('data-type');
				$('#youduButton').removeClass('doudong');
				$('body').removeClass(typeIs);
				$('#youduButton').attr('data-type','');
			}else{
				var duType = $('#duType').val();
				var duArr = duType.split(",");
				var dataType = duArr[Math.floor(Math.random() * duArr.length)];

				$('#youduButton').addClass('doudong');
				$('#youduButton').attr('data-type',dataType);
				$('body').addClass(dataType);
			}
		});
		if(talkAPI!==""){
			$('#showInfoBtn').on('click',function(){
				var live_statu = $('#live_statu_val').val();
				if(live_statu=="0"){
					return
				}else{
					$('#live_statu_val').val("0");
					$('.live_talk_input_body').fadeOut(500);
					AITalkFlag = false;
					showHitokoto();
					$('#showTalkBtn').show();
					$('#showInfoBtn').hide();
				}
			});
			$('#showTalkBtn').on('click',function(){
				var live_statu = $('#live_statu_val').val();
				if(live_statu=="1"){
					return
				}else{
					$('#live_statu_val').val("1");
					$('.live_talk_input_body').fadeIn(500);
					AITalkFlag = true;
					$('#showTalkBtn').hide();
					$('#showInfoBtn').show();
					
				}
			});
			$('#talk_send').on('click', async function() { // 使用 async
				var info_ = $('#AIuserText').val();
				var userid_ = $('#AIuserName').val();
				if(info_ == "" ){
					showMessage('写点什么吧！',0);
					return;
				}
				if(userid_ == ""){
					showMessage('聊之前请告诉我你的名字吧！',0);
					return;
				}
				// 保存用户名到sessionStorage
				sessionStorage.setItem("live2duser", userid_);
				
				showMessage('思考中~', 0);
				$('.message').html(''); // 清空之前的消息
				
				// 如果有正在播放的语音，先停止
				if (currentUtterance) {
					window.speechSynthesis.cancel();
					currentUtterance = null;
				}

				try {
					const response = await fetch(talkAPI, {
						method: 'POST',
						headers: {
							'X-CSRFToken': csrftoken,
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({
							"message": info_,
							"userid": userid_
						})
					});

					if (!response.ok) {
                        let errorText = '网络似乎出现了问题，请稍后再试！';
                        try {
                            const errorData = await response.json(); // 尝试解析JSON错误
                            errorText = errorData.error || errorText;
                        } catch (e) {
                            // 如果不是JSON，尝试读取文本
                            errorText = await response.text() || errorText;
                        }
						throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
					}

					const reader = response.body.getReader();
					// 使用更稳健的UTF-8解码配置，忽略错误字符
					const decoder = new TextDecoder('utf-8', { fatal: false });
					let result = '';
                    let currentMessage = '';
                    $('.message').fadeTo(200, 1); // 确保消息框可见

					// 用于存储完整的响应文本，用于语音播报
					let fullResponseText = '';
					
					while (true) {
						const { done, value } = await reader.read();
						if (done) {
							// 流结束后，播放完整的响应文本
							if (speechEnabled && fullResponseText) {
								// 过滤掉表情符号和特殊字符，提高语音质量
								var cleanText = fullResponseText.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27FF]/g, '');
								speakText(cleanText);
							}
							break;
						}
						// 解码时处理流式数据
						try {
							// 使用stream:true确保流式解码正确处理
							const chunk = decoder.decode(value, { stream: true });
							
							// 增强的文本清理：保留常见可见字符和中文字符，移除可能导致乱码的控制字符
							// 保留ASCII可打印字符(32-126)、中文字符(常用+扩展)、常见标点和符号
							const cleanedChunk = chunk
								.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '') // 移除控制字符
								.replace(/[\x7F-\x9F]/g, '')                      // 移除扩展ASCII控制字符
								.replace(/\uFFFD/g, '');                           // 移除Unicode替换字符(常见乱码标志)
							
							currentMessage += cleanedChunk;
							
							// 更新用于语音播报的完整文本
							fullResponseText = $('<div>').html(currentMessage).text();
							
							// 检查是否包含错误标识
							if (currentMessage.startsWith("Error:")) {
								showMessage(currentMessage, 0);
								reader.cancel(); // 停止读取流
								return; // 提前退出
							}
							
							// 安全地处理HTML内容，防止XSS和乱码
							let displayContent = currentMessage;
							
							// 逐步显示文本，并解析Markdown
							if (typeof marked === 'function') {
								try {
									// 使用marked的安全选项，确保XSS防护
									const markedOptions = { 
										sanitize: true,
										breaks: true,     // 自动将换行符转换为<br>
										gfm: true         // 启用GitHub风格Markdown
									};
									displayContent = marked.parse(currentMessage, markedOptions);
								} catch (markdownError) {
									console.warn('Markdown解析错误:', markdownError);
									// 降级处理：安全地替换换行符和转义HTML
									displayContent = currentMessage
										.replace(/&/g, '&amp;')
										.replace(/</g, '&lt;')
										.replace(/>/g, '&gt;')
										.replace(/"/g, '&quot;')
										.replace(/\n/g, '<br>');
								}
							} else {
								// Fallback: 安全地替换换行符和转义HTML
								displayContent = currentMessage
									.replace(/&/g, '&amp;')
									.replace(/</g, '&lt;')
									.replace(/>/g, '&gt;')
									.replace(/"/g, '&quot;')
									.replace(/\n/g, '<br>');
								console.warn('marked.js not found. Markdown rendering disabled.');
							}
							
							// 安全地设置HTML内容
							$('.message').html(displayContent);
							talkValTimer(); // 更新对话状态
						} catch (decodeError) {
							console.error('解码错误:', decodeError);
							// 增强的错误恢复机制
							try {
								// 使用更宽容的解码配置
								const fallbackDecoder = new TextDecoder('utf-8', { 
									fatal: false,
									ignoreBOM: true // 忽略字节顺序标记，增加兼容性
								});
								
								// 尝试直接解码整个数据块
								const fallbackChunk = fallbackDecoder.decode(value);
								
								// 更严格的字符过滤，只保留确定安全的字符
								const cleanedChunk = fallbackChunk.replace(
									/[^\x20-\x7E\u4E00-\u9FFF\u3000-\u303F\uFF00-\uFFEF\u2000-\u206F\u2E00-\u2E7F]/g, 
									''
								);
								
								currentMessage += cleanedChunk;
								
								// 安全显示内容，确保HTML转义
								const safeContent = currentMessage
									.replace(/&/g, '&amp;')
									.replace(/</g, '&lt;')
									.replace(/>/g, '&gt;')
									.replace(/"/g, '&quot;')
									.replace(/\n/g, '<br>');
									
								$('.message').html(safeContent);
								talkValTimer();
								
								// 记录恢复成功
								console.info('使用备用解码方法成功恢复内容');
							} catch (fallbackError) {
								// 如果所有解码方法都失败，显示友好错误消息
								console.error('备用解码也失败:', fallbackError);
								showMessage('抱歉，接收到的消息无法正确显示。请刷新页面后重试。', 0);
							}
						}
					}

                    // 流结束后处理
                    $('#AIuserText').val("");
                    sessionStorage.setItem("live2duser", userid_);

				} catch (error) {
					talkValTimer();
                    let errorMsg = '网络似乎出现了问题，请稍后再试！';
                    if (error.message && error.message.includes('HTTP error!')) {
                        // 尝试提取后端返回的错误信息
                        const match = error.message.match(/message: (.*)/);
                        if (match && match[1]) {
                            errorMsg = match[1];
                        }
                    }
					showMessage(errorMsg, 0);
					console.error('Fetch error:', error);
				}
			});
		}else{
			$('#showInfoBtn').hide();
			$('#showTalkBtn').hide();
			
		}

		// 添加页面介绍按钮
		$('#landlord').append('<div id="pageInfoBtn" class="live_ico_item" title="介绍页面内容"><svg viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M11 9h2V7h-2m1 13c-4.41 0-8-3.59-8-8s3.59-8 8-8s8 3.59 8 8s-3.59 8-8 8m0-18A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2m-1 15h2v-6h-2v6z"></path></svg></div>');
		// 添加页面介绍按钮的样式
		var style = document.createElement('style');
		style.innerHTML = `
			#pageInfoBtn {
				margin-bottom: 10px;
				animation: breath 0.8s ease-in-out infinite alternate;
				color: #0099cc;
			}
			#pageInfoBtn:hover {
				color: #33ccff;
				transform: scale(1.1);
			}
		`;
		document.head.appendChild(style);
		$('#pageInfoBtn').on('click', function(){
			introducePageContent();
		});
		//获取音乐信息初始化
		var bgmListInfo = $('input[name=live2dBGM]');
		if(bgmListInfo.length == 0){
			$('#musicButton').hide();
		}else{
			var bgmPlayNow = parseInt($('#live2d_bgm').attr('data-bgm'));
			var bgmPlayTime = 0;
			var live2dBGM_Num = sessionStorage.getItem("live2dBGM_Num");
			var live2dBGM_PlayTime = sessionStorage.getItem("live2dBGM_PlayTime");
			if(live2dBGM_Num){
				if(live2dBGM_Num<=$('input[name=live2dBGM]').length-1){
					bgmPlayNow = parseInt(live2dBGM_Num);
				}
			}
			if(live2dBGM_PlayTime){
				bgmPlayTime = parseInt(live2dBGM_PlayTime);
			}
			var live2dBGMSrc = bgmListInfo.eq(bgmPlayNow).val();
			$('#live2d_bgm').attr('data-bgm',bgmPlayNow);
			$('#live2d_bgm').attr('src',live2dBGMSrc);
			$('#live2d_bgm')[0].currentTime = bgmPlayTime;
			$('#live2d_bgm')[0].volume = 0.5;
			var live2dBGM_IsPlay = sessionStorage.getItem("live2dBGM_IsPlay");
			var live2dBGM_WindowClose = sessionStorage.getItem("live2dBGM_WindowClose");
			if(live2dBGM_IsPlay == '0' && live2dBGM_WindowClose == '0'){
				$('#live2d_bgm')[0].play();
				$('#musicButton').addClass('play');
			}
			sessionStorage.setItem("live2dBGM_WindowClose" , '1');
			$('#musicButton').on('click',function(){
				if($('#musicButton').hasClass('play')){
					$('#live2d_bgm')[0].pause();
					$('#musicButton').removeClass('play');
					sessionStorage.setItem("live2dBGM_IsPlay",'1');
				}else{
					$('#live2d_bgm')[0].play();
					$('#musicButton').addClass('play');
					sessionStorage.setItem("live2dBGM_IsPlay",'0');
				}
			});
			window.onbeforeunload = function(){ 
			 	sessionStorage.setItem("live2dBGM_WindowClose" , '0');
				if($('#musicButton').hasClass('play')){
					sessionStorage.setItem("live2dBGM_IsPlay",'0');
				}
			} 
			document.getElementById('live2d_bgm').addEventListener("timeupdate", function(){
				var live2dBgmPlayTimeNow = document.getElementById('live2d_bgm').currentTime;
				sessionStorage.setItem("live2dBGM_PlayTime" , live2dBgmPlayTimeNow );
			});
			document.getElementById('live2d_bgm').addEventListener("ended", function(){
				var listNow = parseInt($('#live2d_bgm').attr('data-bgm'));
				listNow ++ ;
				if(listNow > $('input[name=live2dBGM]').length-1){
					listNow = 0;
				}
				var listNewSrc = $('input[name=live2dBGM]').eq(listNow).val();
				sessionStorage.setItem("live2dBGM_Num",listNow);
				$('#live2d_bgm').attr('src',listNewSrc);
				$('#live2d_bgm')[0].play();
				$('#live2d_bgm').attr('data-bgm',listNow);
			});
			document.getElementById('live2d_bgm').addEventListener("error", function(){
				$('#live2d_bgm')[0].pause();
				$('#musicButton').removeClass('play');
				showMessage('音乐似乎加载不出来了呢！',0);
			});
		}
		//获取用户名
		var live2dUser = sessionStorage.getItem("live2duser");
		if(live2dUser !== null){
			$('#AIuserName').val(live2dUser);
		}
		//获取位置
		var landL = sessionStorage.getItem("historywidth");
		var landB = sessionStorage.getItem("historyheight");
		if(landL == null || landB ==null){
			landL = '5px'
			landB = '0px'
		}
		$('#landlord').css('left',landL+'px');
		$('#landlord').css('bottom',landB + 'px');
		//移动
		function getEvent() {
			return window.event || arguments.callee.caller.arguments[0];
		}
		var smcc = document.getElementById("landlord");
		var moveX = 0;
		var moveY = 0;
		var moveBottom = 0;
		var moveLeft = 0;
		var moveable = false;
		var docMouseMoveEvent = document.onmousemove;
		var docMouseUpEvent = document.onmouseup;
		smcc.onmousedown = function(){
			var ent = getEvent();
			moveable = true;
			moveX = ent.clientX;
			moveY = ent.clientY;
			var obj = smcc;
			moveBottom = parseInt(obj.style.bottom);
			moveLeft = parseInt(obj.style.left);
			if(isFirefox=navigator.userAgent.indexOf("Firefox")>0){
				window.getSelection().removeAllRanges();
			}			
			document.onmousemove = function(){
				if(moveable){
					var ent = getEvent();
					var x = moveLeft + ent.clientX - moveX;
					var y = moveBottom +  (moveY - ent.clientY);
					obj.style.left = x + "px";
					obj.style.bottom = y + "px";
				}
			};
			document.onmouseup = function(){
				if(moveable){
					var historywidth = obj.style.left;
					var historyheight = obj.style.bottom;
					historywidth = historywidth.replace('px', '');
					historyheight = historyheight.replace('px', '');
					sessionStorage.setItem("historywidth", historywidth);
					sessionStorage.setItem("historyheight", historyheight);
					document.onmousemove = docMouseMoveEvent;
					document.onmouseup = docMouseUpEvent;
					moveable = false; 
					moveX = 0;
					moveY = 0;
					moveBottom = 0;
					moveLeft = 0;
				}
			};
		};
	}
	$(document).ready(function() {
		var AIimgSrc = [
			message_Path + "model/histoire/histoire.1024/texture_00.png",
			message_Path + "model/histoire/histoire.1024/texture_01.png",
			message_Path + "model/histoire/histoire.1024/texture_02.png",
			message_Path + "model/histoire/histoire.1024/texture_03.png"
		]
		var images = [];
		var imgLength = AIimgSrc.length;
		var loadingNum = 0;
		for(var i=0;i<imgLength;i++){
			images[i] = new Image();
			images[i].src = AIimgSrc[i];
			images[i].onload = function(){
				loadingNum++;
				if(loadingNum===imgLength){
					var live2dhidden = localStorage.getItem("live2dhidden");
					if(live2dhidden==="0"){
						setTimeout(function(){
							$('#open_live2d').fadeIn(200);
						},1300);
					}else{
						setTimeout(function(){
							$('#landlord').fadeIn(200);
						},1300);
					}
					setTimeout(function(){
						loadlive2d("live2d", message_Path+"model/histoire/model.json");
						// 添加随机动作定时器
						setInterval(function(){
							// 随机触发动作和表情 - 降低概率从30%到15%
							if(Math.random() < 0.15) { // 15%概率触发随机动作
								var randomActions = ['normal', 'happy', 'shy', 'surprised', 'sad'];
								// 从动作列表中移除了'wink'(眨眼/闭眼)动作
								
								// 即使在剩余动作中，也进一步降低闭眼相关动作的概率
								if(Math.random() > 0.7) { // 30%概率添加wink回列表
									randomActions.push('wink');
								}
								
								var randomIndex = Math.floor(Math.random() * randomActions.length);
								console.log('随机动作: ' + randomActions[randomIndex]);
								
								// 如果模型支持表情切换，可以在这里调用相关API
								// 模拟表情变化效果
								var action = randomActions[randomIndex];
								if(action === 'happy') {
									showMessage('😊', 1000);
								} else if(action === 'shy') {
									showMessage('😳', 1000);
								} else if(action === 'surprised') {
									showMessage('😲', 1000);
								} else if(action === 'sad') {
									showMessage('😢', 1000);
								}
								
								// 添加轻微的动画效果
								$('#landlord').addClass('animated');
								setTimeout(function(){
									$('#landlord').removeClass('animated');
								}, 1000);
							}
						}, 12000); // 延长间隔时间从8秒到12秒
					},1000);
					initLive2d ();
					images = null;
				}
			}
		}
		
		// 添加CSS动画类
		var style = document.createElement('style');
		style.type = 'text/css';
		style.innerHTML = `
			.animated {
				animation: shake 0.5s ease-in-out;
			}
			@keyframes shake {
				0%, 100% { transform: translateX(0); }
				25% { transform: translateX(-5px); }
				75% { transform: translateX(5px); }
			}
		`;
		document.getElementsByTagName('head')[0].appendChild(style);
	});
}


// 全局动作控制方法
// 说明：
// - 在不修改 live2d.js 的前提下，优先通过向 canvas 触发一次“点击/点按”事件，调起模型内置的 tap 动作。
// - 对于情绪类动作（happy/shy/surprised/sad/wink），提供 UI 级别的表情与轻微动画反馈。
// - 该方法不会破坏现有逻辑，未找到模型或不支持时会优雅降级并给出日志提示。
/**
 * 控制 Live2D 动作的统一入口
 * 用法示例：
 *   window.live2dAction('tap');                // 触发一次 tap 动作（最通用）
 *   window.live2dAction('randomTap');         // 同上，别名
 *   window.live2dAction('tap:3');             // 连续触发 3 次 tap（有些模型会随机播放不同动作）
 *   window.live2dAction('happy');             // 显示“开心”表情并轻微抖动
 *   window.live2dAction('shy', {message:'害羞啦~'}); // 自定义提示文本
 *
 * @param {string} action - 动作名称：tap/randomTap/tap:N 或 happy|shy|surprised|sad|wink
 * @param {{duration?: number, message?: string}} [options]
 * @returns {boolean} 是否成功发起动作（不代表模型一定有对应动画）
 */
window.live2dAction = function(action, options){
	try{
		options = options || {};
		var duration = typeof options.duration === 'number' ? options.duration : 1000;
		var customMsg = options.message;
		var canvas = document.getElementById('live2d');
		var landlord = document.getElementById('landlord');

		// 触发一次 tap：很多 Live2D 实现会在 canvas 的点击事件中调用随机 tap 动作
		function triggerTapOnce(){
			if(!canvas){
				console.warn('[live2dAction] 未找到 #live2d 画布，无法触发 tap');
				return false;
			}
			try{
				['mousedown','mouseup','click','touchstart','touchend'].forEach(function(type){
					var e;
					if(type.indexOf('touch') === 0){
						e = new TouchEvent(type, {bubbles:true, cancelable:true});
					}else{
						e = new MouseEvent(type, {bubbles:true, cancelable:true, view:window});
					}
					canvas.dispatchEvent(e);
				});
				return true;
			}catch(err){
				console.error('[live2dAction] 触发 tap 失败:', err);
				return false;
			}
		}

		// 轻微抖动动画
		function shake(){
			if(!landlord) return;
			landlord.classList.add('animated');
			setTimeout(function(){ landlord.classList.remove('animated'); }, Math.max(300, duration));
		}

		// 情绪到表情映射
		var emojiMap = {
			happy: '😊',
			shy: '😳',
			surprised: '😲',
			sad: '😢',
			wink: '😉'
		};

		// 处理 tap 类动作
		if(action === 'tap' || action === 'randomTap'){
			return triggerTapOnce();
		}
		var tapTimesMatch = /^tap[:\(](\d+)[\)]?$/.exec(action);
		if(tapTimesMatch){
			var times = Math.min(10, Math.max(1, parseInt(tapTimesMatch[1], 10) || 1));
			var ok = false;
			for(var i=0;i<times;i++){
				setTimeout(function(){ ok = triggerTapOnce() || ok; }, i*120);
			}
			return ok;
		}

		// 处理情绪类动作（UI 级反馈 + 提示）
		if(emojiMap[action]){
			var tip = customMsg || emojiMap[action];
			try { showMessage(tip, duration); } catch(_) { /* 忽略消息系统未初始化的情况 */ }
			shake();
			return true;
		}

		console.warn('[live2dAction] 未识别的动作:', action);
		return false;
	}catch(e){
		console.error('[live2dAction] 执行动作异常:', e);
		return false;
	}
};

/**
 * 只读方法：判断 Live2D 画布是否已就绪
 * @returns {boolean}
 */
window.live2dIsReady = function(){
	var c = document.getElementById('live2d');
	return !!(c && c.width > 0 && c.height > 0);
};
// 
// 全局动作控制方法
// 说明：
// - 在不修改 live2d.js 的前提下，优先通过向 canvas 触发一次“点击/点按”事件，调起模型内置的 tap 动作。
// - 对于情绪类动作（happy/shy/surprised/sad/wink），提供 UI 级别的表情与轻微动画反馈。
// - 该方法不会破坏现有逻辑，未找到模型或不支持时会优雅降级并给出日志提示。
/**
 * 控制 Live2D 动作的统一入口
 * 用法示例：
 *   window.live2dAction('tap');                // 触发一次 tap 动作（最通用）
 *   window.live2dAction('randomTap');         // 同上，别名
 *   window.live2dAction('tap:3');             // 连续触发 3 次 tap（有些模型会随机播放不同动作）
 *   window.live2dAction('happy');             // 显示“开心”表情并轻微抖动
 *   window.live2dAction('shy', {message:'害羞啦~'}); // 自定义提示文本
 *
 * @param {string} action - 动作名称：tap/randomTap/tap:N 或 happy|shy|surprised|sad|wink
 * @param {{duration?: number, message?: string}} [options]
 * @returns {boolean} 是否成功发起动作（不代表模型一定有对应动画）
 */
window.live2dAction = function(action, options){
	try{
		options = options || {};
		var duration = typeof options.duration === 'number' ? options.duration : 1000;
		var customMsg = options.message;
		var canvas = document.getElementById('live2d');
		var landlord = document.getElementById('landlord');

		// 触发一次 tap：很多 Live2D 实现会在 canvas 的点击事件中调用随机 tap 动作
		function triggerTapOnce(){
			if(!canvas){
				console.warn('[live2dAction] 未找到 #live2d 画布，无法触发 tap');
				return false;
			}
			try{
				['mousedown','mouseup','click'].forEach(function(type){
					var e = new MouseEvent(type, {bubbles:true, cancelable:true, view:window});
					canvas.dispatchEvent(e);
				});
				return true;
			}catch(err){
				console.error('[live2dAction] 触发 tap 失败:', err);
				return false;
			}
		}

		// 轻微抖动动画
		function shake(){
			if(!landlord) return;
			landlord.classList.add('animated');
			setTimeout(function(){ landlord.classList.remove('animated'); }, Math.max(300, duration));
		}

		// 情绪到表情映射
		var emojiMap = {
			happy: '😊',
			shy: '😳',
			surprised: '😲',
			sad: '😢',
			wink: '😉'
		};

		// 处理 tap 类动作
		if(action === 'tap' || action === 'randomTap'){
			return triggerTapOnce();
		}
		var tapTimesMatch = /^tap[:\(](\d+)[\)]?$/.exec(action);
		if(tapTimesMatch){
			var times = Math.min(10, Math.max(1, parseInt(tapTimesMatch[1], 10) || 1));
			var ok = false;
			for(var i=0;i<times;i++){
				setTimeout(function(){ ok = triggerTapOnce() || ok; }, i*120);
			}
			return ok;
		}

		// 处理情绪类动作（UI 级反馈 + 提示）
		if(emojiMap[action]){
			var tip = customMsg || emojiMap[action];
			try { showMessage(tip, duration); } catch(_) { /* 忽略消息系统未初始化的情况 */ }
			shake();
			return true;
		}

		console.warn('[live2dAction] 未识别的动作:', action);
		return false;
	}catch(e){
		console.error('[live2dAction] 执行动作异常:', e);
		return false;
	}
};

/**
 * 只读方法：判断 Live2D 画布是否已就绪
 * @returns {boolean}
 */
window.live2dIsReady = function(){
	var c = document.getElementById('live2d');
	return !!(c && c.width > 0 && c.height > 0);
};
// 
// $(document).ready(function() {
// ... existing code ...