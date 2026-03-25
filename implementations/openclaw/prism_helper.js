/**
 * 棱镜互联协议 - OpenClaw JavaScript辅助函数
 * Prism Interconnect Protocol - OpenClaw JavaScript Helpers
 * 
 * 提供棱镜协议的JavaScript实现和辅助功能
 */

const { v4: uuidv4 } = require('uuid');

/**
 * 光谱类型枚举
 */
const SpectrumType = {
  RED: 'red',       // 快速直觉
  BLUE: 'blue',     // 慢速分析
  PURPLE: 'purple', // 元认知审视
  GREEN: 'green',   // 生态视角
  ORANGE: 'orange'  // 历史经验
};

/**
 * 消息类型枚举
 */
const MessageType = {
  PRISM_MESSAGE: 'prism_message',
  CEASE_SIGNAL: 'cease_signal'
};

/**
 * 知止类型枚举
 */
const CeaseType = {
  TEMPORARY: 'temporary',
  PERMANENT: 'permanent',
  SAFETY: 'safety'
};

/**
 * 困惑类
 */
class Puzzle {
  constructor(text, context = null, metadata = {}) {
    this.text = text;
    this.context = context;
    this.metadata = metadata;
    
    this.validate();
  }
  
  validate() {
    if (!this.text || !this.text.trim()) {
      throw new Error('困惑文本不能为空');
    }
  }
  
  toJSON() {
    const result = { text: this.text };
    if (this.context) result.context = this.context;
    if (Object.keys(this.metadata).length > 0) {
      result.metadata = this.metadata;
    }
    return result;
  }
  
  get hash() {
    const content = `${this.text}:${this.context || ''}`;
    return require('crypto')
      .createHash('md5')
      .update(content)
      .digest('hex');
  }
}

/**
 * 光谱类
 */
class Spectrum {
  constructor(type, name, content, confidence = 1.0, metadata = {}) {
    this.type = type;
    this.name = name;
    this.content = content;
    this.confidence = confidence;
    this.metadata = metadata;
    
    this.validate();
  }
  
  validate() {
    if (!this.content || !this.content.trim()) {
      throw new Error('光谱内容不能为空');
    }
    if (this.confidence < 0 || this.confidence > 1) {
      throw new Error('置信度必须在0-1之间');
    }
  }
  
  toJSON() {
    const result = {
      type: this.type,
      name: this.name,
      content: this.content
    };
    if (this.confidence < 1.0) {
      result.confidence = Math.round(this.confidence * 100) / 100;
    }
    if (Object.keys(this.metadata).length > 0) {
      result.metadata = this.metadata;
    }
    return result;
  }
  
  get cognitiveStyle() {
    const styles = {
      [SpectrumType.RED]: '直觉性、故事性、身体感知',
      [SpectrumType.BLUE]: '分析性、结构性、逻辑推理',
      [SpectrumType.PURPLE]: '元认知性、反思性、开放性',
      [SpectrumType.GREEN]: '系统性、生态性、关系思维',
      [SpectrumType.ORANGE]: '历史性、经验性、模式识别'
    };
    return styles[this.type] || '未知风格';
  }
}

/**
 * 留白类
 */
class Whitespace {
  constructor(content, promptType = 'reflection', durationSuggestion = null) {
    this.content = content;
    this.promptType = promptType;
    this.durationSuggestion = durationSuggestion;
    
    this.validate();
  }
  
  validate() {
    if (!this.content || !this.content.trim()) {
      throw new Error('留白内容不能为空');
    }
    if (this.content.length > 200) {
      console.warn(`留白内容较长（${this.content.length}字符），建议精简`);
    }
  }
  
  toJSON() {
    const result = { content: this.content };
    if (this.promptType !== 'reflection') {
      result.promptType = this.promptType;
    }
    if (this.durationSuggestion) {
      result.durationSuggestion = this.durationSuggestion;
    }
    return result;
  }
}

/**
 * 棱镜会话类
 */
class PrismSession {
  constructor(sessionId = null, maxDepth = 3) {
    this.sessionId = sessionId || `session-${uuidv4().slice(0, 8)}`;
    this.maxDepth = maxDepth;
    this.currentDepth = 0;
    this.messageHistory = [];
    this.startTime = new Date();
    this.ceaseSignals = [];
  }
  
  canRecurse(depth) {
    return depth < this.maxDepth;
  }
  
  addMessage(message) {
    this.messageHistory.push({
      timestamp: new Date().toISOString(),
      depth: message.metadata?.recursion_depth || 0,
      messageId: message.id,
      type: message.type
    });
  }
  
  addCeaseSignal(signal) {
    this.ceaseSignals.push({
      timestamp: new Date().toISOString(),
      reason: signal.metadata?.reason || 'unknown',
      signal: signal
    });
  }
  
  getSummary() {
    const durationSeconds = (new Date() - this.startTime) / 1000;
    const depths = this.messageHistory.map(m => m.depth);
    const maxDepthReached = depths.length > 0 ? Math.max(...depths) : 0;
    
    return {
      sessionId: this.sessionId,
      durationSeconds: Math.round(durationSeconds * 10) / 10,
      totalMessages: this.messageHistory.length,
      maxDepthReached: maxDepthReached,
      ceaseSignals: this.ceaseSignals.length,
      startTime: this.startTime.toISOString(),
      currentDepth: this.currentDepth
    };
  }
}

/**
 * 棱镜代理类（JavaScript简化版）
 */
class PrismAgent {
  constructor(agentId, capabilities = null, maxDepth = 3, enableCaching = true) {
    this.agentId = agentId;
    this.capabilities = capabilities || [
      SpectrumType.RED,
      SpectrumType.BLUE,
      SpectrumType.PURPLE
    ];
    this.maxDepth = maxDepth;
    this.enableCaching = enableCaching;
    
    this.session = new PrismSession(`session-${agentId}`, maxDepth);
    this.spectrumCache = new Map();
    this.puzzleCache = new Map();
    
    console.log(`棱镜代理初始化: ${agentId}, 能力: ${this.capabilities.join(', ')}`);
  }
  
  /**
   * 折射困惑
   */
  async refract(puzzleText, context = null, depth = 0, metadata = {}) {
    try {
      // 创建困惑
      const puzzle = new Puzzle(puzzleText, context, metadata);
      
      // 检查递归深度
      if (!this.session.canRecurse(depth)) {
        console.warn(`达到最大递归深度 ${depth}，发送知止信号`);
        return await this.sendCeaseSignal(
          '达到最大递归深度',
          CeaseType.SAFETY
        );
      }
      
      // 生成光谱
      const spectra = await this.generateSpectra(puzzle, depth);
      
      // 生成留白（简化版）
      const whitespace = await this.generateWhitespace(spectra, puzzle);
      
      // 组装消息
      const message = this.assembleMessage(puzzle, spectra, whitespace, depth);
      
      // 记录会话
      this.session.addMessage(message);
      this.session.currentDepth = depth;
      
      console.log(`成功生成棱镜消息，深度: ${depth}, 光谱数: ${spectra.length}`);
      
      return message;
      
    } catch (error) {
      console.error(`折射失败: ${error.message}`, error);
      return await this.sendCeaseSignal(
        `处理失败: ${error.message}`,
        CeaseType.SAFETY
      );
    }
  }
  
  /**
   * 生成光谱数组
   */
  async generateSpectra(puzzle, depth) {
    // 检查缓存
    if (this.enableCaching) {
      const cacheKey = `${puzzle.hash}:${depth}`;
      if (this.spectrumCache.has(cacheKey)) {
        console.log(`使用缓存光谱: ${cacheKey}`);
        return this.spectrumCache.get(cacheKey);
      }
    }
    
    // 确定要生成的光谱类型
    const targetTypes = this.capabilities.slice(0, 3);
    if (targetTypes.length < 3) {
      // 能力不足，重复使用
      while (targetTypes.length < 3) {
        targetTypes.push(targetTypes[targetTypes.length - 1] || SpectrumType.RED);
      }
      console.warn('能力不足，使用重复类型生成三种光谱');
    }
    
    // 生成光谱（简化版，实际应该调用API）
    const spectra = [];
    for (const type of targetTypes) {
      try {
        const spectrum = await this.generateSingleSpectrum(type, puzzle);
        spectra.push(spectrum);
      } catch (error) {
        console.error(`光谱生成失败 (${type}): ${error.message}`);
        // 降级处理
        const fallback = new Spectrum(
          type,
          `${type}（生成失败）`,
          `暂时无法生成${type}视角，请稍后重试或尝试其他视角。`,
          0.1
        );
        spectra.push(fallback);
      }
    }
    
    // 确保至少有三个光谱
    if (spectra.length < 3) {
      throw new Error(`无法生成足够的光谱，只有${spectra.length}个有效`);
    }
    
    // 缓存结果
    if (this.enableCaching) {
      const cacheKey = `${puzzle.hash}:${depth}`;
      this.spectrumCache.set(cacheKey, spectra);
      this.puzzleCache.set(cacheKey, puzzle);
    }
    
    return spectra;
  }
  
  /**
   * 生成单个光谱（简化实现）
   */
  async generateSingleSpectrum(type, puzzle) {
    // 这里应该调用实际的API
    // 简化实现，返回示例内容
    
    const templates = {
      [SpectrumType.RED]: {
        name: '快速直觉',
        content: `直觉上，${puzzle.text} 让我联想到一种身体感受...`
      },
      [SpectrumType.BLUE]: {
        name: '慢速分析',
        content: `从分析角度看，${puzzle.text} 可能涉及以下几个层面...`
      },
      [SpectrumType.PURPLE]: {
        name: '元认知审视',
        content: `让我们先暂停问"如何解决"，而是问"我们如何思考这个问题"...`
      },
      [SpectrumType.GREEN]: {
        name: '生态视角',
        content: `从生态系统视角看${puzzle.text}...`
      },
      [SpectrumType.ORANGE]: {
        name: '历史经验',
        content: `从历史经验看${puzzle.text}...`
      }
    };
    
    const template = templates[type] || templates[SpectrumType.RED];
    
    return new Spectrum(
      type,
      template.name,
      template.content,
      0.8,
      {
        engine: 'js-simplified',
        generationTime: new Date().toISOString()
      }
    );
  }
  
  /**
   * 生成留白
   */
  async generateWhitespace(spectra, puzzle) {
    const spectrumTypes = spectra.map(s => s.type);
    const confidenceScores = spectra.map(s => s.confidence);
    
    let content, promptType, duration;
    
    if (spectrumTypes.includes(SpectrumType.PURPLE)) {
      content = `在这些视角中，哪一个问题让你最想深入思考？
      
暂停一下，感受你的身体反应：
- 哪个观点让你点头认同？
- 哪个观点让你想反驳？
- 哪个观点让你感到好奇？

这种反应本身，就是你需要倾听的内心声音。
给自己一分钟的沉默，只是感受，不急于回答。`;
      promptType = 'deep_reflection';
      duration = 60;
      
    } else if (confidenceScores.some(c => c < 0.7)) {
      content = `有些视角的确定性较低，这本身是重要的信息。

不确定性不是缺陷，而是探索的邀请。
在这些不够确定的观点中，你看到了什么可能性？
如果这些观点只是部分正确，完整的图景可能是什么？

让问题保持开放，比急于关闭更有价值。`;
      promptType = 'uncertainty_embrace';
      duration = 45;
      
    } else {
      content = `在${spectra.length}种视角中（${spectrumTypes.join(', ')}）：

哪一种最先触动你？为什么？
哪一种让你想追问更多？追问什么？
哪一种与你原有的理解不同？这种不同意味着什么？

给自己一点时间，让这些视角在你内心沉淀。
不急于整合，先让它们各自发声。`;
      promptType = 'reflection';
      duration = 30;
    }
    
    return new Whitespace(content, promptType, duration);
  }
  
  /**
   * 组装消息
   */
  assembleMessage(puzzle, spectra, whitespace, depth) {
    const spectrumDicts = spectra.map(s => s.toJSON());
    const avgConfidence = spectra.reduce((sum, s) => sum + s.confidence, 0) / spectra.length;
    const uniqueTypes = new Set(spectra.map(s => s.type)).size;
    
    return {
      protocol: 'PIP',
      version: '0.1',
      type: MessageType.PRISM_MESSAGE,
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      sender: {
        id: this.agentId,
        capabilities: this.capabilities,
        metadata: {
          maxDepth: this.maxDepth,
          cachingEnabled: this.enableCaching
        }
      },
      puzzle: puzzle.toJSON(),
      spectrums: spectrumDicts,
      whitespace: whitespace.toJSON(),
      metadata: {
        recursion_depth: depth,
        allow_recursion: depth < this.maxDepth - 1,
        cease_signal: false,
        generation_quality: {
          avg_confidence: Math.round(avgConfidence * 100) / 100,
          spectrum_count: spectra.length,
          unique_types: uniqueTypes
        },
        session_id: this.session.sessionId
      }
    };
  }
  
  /**
   * 发送知止信号
   */
  async sendCeaseSignal(reason, ceaseType = CeaseType.TEMPORARY, resumable = null) {
    if (resumable === null) {
      resumable = ceaseType === CeaseType.TEMPORARY;
    }
    
    const message = {
      protocol: 'PIP',
      version: '0.1',
      type: MessageType.CEASE_SIGNAL,
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      sender: { id: this.agentId },
      metadata: {
        reason: reason,
        cease_type: ceaseType,
        resumable: resumable,
        session_id: this.session.sessionId,
        session_summary: this.session.getSummary()
      }
    };
    
    this.session.addCeaseSignal(message);
    console.log(`发送知止信号: ${reason} (${ceaseType})`);
    
    return message;
  }
  
  /**
   * 处理接收到的消息
   */
  async processMessage(message) {
    try {
      const msgType = message.type;
      
      if (msgType === MessageType.CEASE_SIGNAL) {
        console.log('收到知止信号，结束会话');
        this.session.addCeaseSignal(message);
        return await this.sendCeaseSignal(
          '确认收到知止信号',
          CeaseType.PERMANENT,
          false
        );
      }
      
      if (msgType === MessageType.PRISM_MESSAGE) {
        const puzzleData = message.puzzle || {};
        const metadata = message.metadata || {};
        const depth = (metadata.recursion_depth || 0) + 1;
        
        return await this.refract(
          puzzleData.text || '',
          puzzleData.context,
          depth,
          {
            parent_message_id: message.id,
            responding_to: message.sender?.id
          }
        );
      }
      
      console.warn(`未知消息类型: ${msgType}`);
      return await this.sendCeaseSignal(
        `不支持的消息类型: ${msgType}`,
        CeaseType.SAFETY
      );
      
    } catch (error) {
      console.error(`消息处理失败: ${error.message}`, error);
      return await this.sendCeaseSignal(
        `处理失败: ${error.message}`,
        CeaseType.SAFETY
      );
    }
  }
  
  /**
   * 获取会话信息
   */
  getSessionInfo() {
    return this.session.getSummary();
  }
  
  /**
   * 清空缓存
   */
  clearCache() {
    this.spectrumCache.clear();
    this.puzzleCache.clear();
    console.log('缓存已清空');
  }
}

/**
 * 验证棱镜消息
 */
function validatePrismMessage(message) {
  const errors = [];
  
  // 检查必填字段
  const requiredFields = ['protocol', 'version', 'type'];
  for (const field of requiredFields) {
    if (!message[field]) {
      errors.push(`缺少必填字段: ${field}`);
    }
  }
  
  // 检查协议标识
  if (message.protocol !== 'PIP') {
    errors.push('protocol字段必须为"PIP"');
  }
  
  // 检查消息类型
  const msgType = message.type;
  const validTypes = Object.values(MessageType);
  if (!validTypes.includes(msgType)) {
    errors.push(`无效的消息类型: ${msgType}`);
  }
  
  // 棱镜消息额外检查
  if (msgType === MessageType.PRISM_MESSAGE) {
    const prismRequired = ['puzzle', 'spectrums', 'whitespace'];
    for (const field of prismRequired) {
      if (!message[field]) {
        errors.push(`棱镜消息缺少必填字段: ${field}`);
    }
    
    // 检查光谱数量
    const spectrums = message.spectrums || [];
    if (spectrums.length < 3) {
      errors.push(`光谱数量不足: 需要至少3个，当前${spectrums.length}个`);
    }
    
    // 检查留白内容
    const whitespace = message.whitespace || {};
    if (!whitespace.content || !whitespace.content.trim()) {
      errors.push('留白内容不能为空');
    }
    
    // 检查困惑文本
    const puzzle = message.puzzle || {};
    if (!puzzle.text || !puzzle.text.trim()) {
      errors.push('困惑文本不能为空');
    }
  }
  
  // 知止信号检查
  else if (msgType === MessageType.CEASE_SIGNAL) {
    const metadata = message.metadata || {};
    if (!metadata.reason || !metadata.reason.trim()) {
      errors.push('知止信号应该包含原因说明');
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors: errors
  };
}

/**
 * 格式化棱镜消息
 */
function formatPrismMessage(message, indent = 2) {
  try {
    const msgType = message.type;
    
    if (msgType === MessageType.PRISM_MESSAGE) {
      const puzzle = message.puzzle || {};
      const spectrums = message.spectrums || [];
      const whitespace = message.whitespace || {};
      const metadata = message.metadata || {};
      
      const output = [];
      output.push('='.repeat(60));
      output.push('棱镜消息');
      output.push('='.repeat(60));
      output.push(`困惑: ${puzzle.text}`);
      if (puzzle.context) {
        output.push(`上下文: ${puzzle.context}`);
      }
      output.push('');
      output.push('光谱:');
      
      spectrums.forEach((spectrum, index) => {
        output.push(`  ${index + 1}. [${spectrum.type}] ${spectrum.name}`);
        let content = spectrum.content || '';
        if (content.length > 100) {
          content = content.substring(0, 97) + '...';
        }
        output.push(`     ${content}`);
        output.push('');
      });
      
      output.push('留白:');
      output.push(`  ${whitespace.content}`);
      output.push('');
      output.push(`元数据: 深度=${metadata.recursion_depth || 0}, 允许递归=${metadata.allow_recursion || false}`);
      output.push('='.repeat(60));
      
      return output.join('\n');
    }
    
    if (msgType === MessageType.CEASE_SIGNAL) {
      const metadata = message.metadata || {};
      
      const output = [];
      output.push('='.repeat(60));
      output.push('知止信号');
      output.push('='.repeat(60));
      output.push(`原因: ${metadata.reason}`);
      output.push(`类型: ${metadata.cease_type}`);
      output.push(`可恢复: ${metadata.resumable}`);
      output.push('='.repeat(60));
      
      return output.join('\n');
    }
    
    return JSON.stringify(message, null, indent);
    
  } catch (error) {
    console.error(`格式化失败: ${error.message}`);
    return JSON.stringify(message, null, indent);
  }
}

/**
 * 示例使用
 */
async function exampleUsage() {
  console.log('棱镜协议JavaScript实现 - 使用示例');
  console.log('='.repeat(60));
  
  // 创建代理
  const agent = new PrismAgent(
    'js_demo_agent',
    [SpectrumType.RED, SpectrumType.BLUE, SpectrumType.PURPLE],
    3,
    true
  );
  
  // 示例1: 基础折射
  console.log('\n1. 基础折射示例:');
  const response = await agent.refract('为什么学习新技能这么难？');
  
  const validation = validatePrismMessage(response);
  if (validation.isValid) {
    console.log('✅ 消息验证通过');
    console.log(formatPrismMessage(response));
  } else {
    console.log('❌ 消息验证失败:');
    validation.errors.forEach(error => console.log(`  - ${error}`));
  }
  
  // 示例2: 知止信号
  console.log('\n2. 知止信号示例:');
  const ceaseResponse = await agent.sendCeaseSignal(
    '示例演示结束',
    CeaseType.TEMPORARY,
    true
  );
  console.log(formatPrismMessage(ceaseResponse));
  
  // 示例3: 会话信息
  console.log('\n3. 会话信息:');
  const sessionInfo = agent.getSessionInfo();
  console.log(`会话ID: ${sessionInfo.sessionId}`);
  console.log(`消息总数: ${sessionInfo.totalMessages}`);
  console.log(`最大深度: ${sessionInfo.maxDepthReached}`);
  console.log(`持续时间: ${sessionInfo.durationSeconds}秒`);
  
  console.log('\n' + '='.repeat(60));
  console.log('示例完成!');
  console.log('='.repeat(60));
}

// 导出模块
module.exports = {
  // 枚举
  SpectrumType,
  MessageType,
  CeaseType,
  
  // 类
  Puzzle,
  Spectrum,
  Whitespace,
  PrismSession,
  PrismAgent,
  
  // 函数
  validatePrismMessage,
  formatPrismMessage,
  
  // 示例
  exampleUsage
};

// 如果直接运行，执行示例
if (require.main === module) {
  exampleUsage().catch(console.error);
}