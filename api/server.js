const express = require('express');
const cors = require('cors');
const Anthropic = require('@anthropic-ai/sdk');

const app = express();

app.use(cors({
  origin: [
    /^https?:\/\/localhost(:\d+)?$/,
    /^https?:\/\/127\.0\.0\.1(:\d+)?$/,
    'https://jiseungchan.github.io',
  ],
}));
app.use(express.json({ limit: '20kb' }));

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

/* ── DuckDuckGo 웹 검색 ──────────────────────────────── */
async function searchWeb(query) {
  try {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
    const res = await fetch(url, {
      headers: { 'Accept': 'application/json', 'User-Agent': 'HanipNewsBot/1.0' },
      signal: AbortSignal.timeout(6000),
    });
    const data = await res.json();

    const results = [];
    if (data.AbstractText) {
      results.push({ title: data.Heading, content: data.AbstractText, url: data.AbstractURL });
    }
    (data.RelatedTopics || []).filter(t => t.Text).slice(0, 5).forEach(t => {
      results.push({ content: t.Text, url: t.FirstURL || '' });
    });
    (data.Results || []).slice(0, 3).forEach(r => {
      if (r.Text) results.push({ content: r.Text, url: r.FirstURL || '' });
    });

    return results.length
      ? results
      : [{ content: `"${query}"에 대한 즉시 검색 결과가 없습니다. 다른 키워드로 시도해보세요.` }];
  } catch (err) {
    return [{ content: `검색 중 오류: ${err.message}` }];
  }
}

/* ── 헬스체크 ─────────────────────────────────────────── */
app.get('/health', (_, res) => res.json({ status: 'ok', version: '1.0.0' }));

/* ── 채팅 엔드포인트 ────────────────────────────────────── */
app.post('/api/chat', async (req, res) => {
  const { messages, articleContext } = req.body;

  if (!Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: 'messages 배열이 필요합니다.' });
  }
  if (messages.length > 40) {
    return res.status(400).json({ error: '대화 기록이 너무 깁니다 (최대 40건).' });
  }

  const systemParts = [
    '당신은 "병규의 한입뉴스"의 AI 어시스턴트입니다.',
    '과학기술, AI, 경제·주식 뉴스 기사에 관한 독자의 질문에 답변합니다.',
    '기사에 없는 최신 정보나 배경 지식이 필요하면 search_web 도구로 웹 검색 후 답변을 보완하세요.',
    '답변은 간결하고 명확하게, 한국어로 작성하세요.',
    '전문 용어가 처음 등장할 때는 괄호 안에 간단히 설명하세요.',
  ];
  if (articleContext?.title) {
    systemParts.push(`\n현재 독자가 읽고 있는 기사: "${articleContext.title}"`);
  }
  if (articleContext?.summary) {
    systemParts.push(`기사 내용 일부:\n${articleContext.summary}`);
  }

  const tools = [{
    name: 'search_web',
    description: '웹에서 최신 정보나 배경 지식을 검색합니다. 기사에 없는 정보가 필요할 때 사용하세요.',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: '검색어 (한국어 또는 영어)' },
      },
      required: ['query'],
    },
  }];

  try {
    let currentMessages = messages;
    let iterations = 0;

    while (iterations++ < 6) {
      const response = await anthropic.messages.create({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1024,
        system: systemParts.join('\n'),
        tools,
        messages: currentMessages,
      });

      if (response.stop_reason === 'end_turn') {
        const text = response.content.find(c => c.type === 'text')?.text || '응답을 생성하지 못했습니다.';
        return res.json({ reply: text });
      }

      if (response.stop_reason === 'tool_use') {
        const toolCall = response.content.find(c => c.type === 'tool_use');
        if (!toolCall) break;

        const searchResult = await searchWeb(toolCall.input.query);
        currentMessages = [
          ...currentMessages,
          { role: 'assistant', content: response.content },
          {
            role: 'user',
            content: [{
              type: 'tool_result',
              tool_use_id: toolCall.id,
              content: JSON.stringify(searchResult, null, 2),
            }],
          },
        ];
        continue;
      }

      break;
    }

    res.status(500).json({ error: '응답 생성에 실패했습니다.' });
  } catch (err) {
    console.error('[Chat API Error]', err.message);
    res.status(err.status || 500).json({ error: err.message || '서버 오류' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`✅ 한입뉴스 AI API 서버 실행 중: http://localhost:${PORT}`);
  console.log(`   헬스체크: http://localhost:${PORT}/health`);
});
